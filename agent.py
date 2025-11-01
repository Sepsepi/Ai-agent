"""
Real Estate Deal Analyzer Agent using OpenAI Assistants API
"""

import json
from openai import OpenAI
from config import OPENAI_API_KEY
from functions.realtor_api import get_property_details, get_comparable_properties, extract_property_info
from functions.deal_calculator import (
    calculate_arv_from_comps,
    estimate_repair_costs,
    analyze_deal,
    format_deal_analysis_report
)


# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# Define function schemas for the agent
FUNCTION_SCHEMAS = [
    {
        "name": "get_property_details",
        "description": "Fetch detailed property information from Realtor.com by address. Use this to get current listing price, bedrooms, bathrooms, square footage, and other property details.",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "Full property address including street, city, and state (e.g., '123 Main St, Austin, TX')"
                }
            },
            "required": ["address"]
        }
    },
    {
        "name": "get_comparable_properties",
        "description": "Find comparable properties (comps) in the same area to estimate After Repair Value (ARV). Returns similar properties that have sold or are listed.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name"
                },
                "state": {
                    "type": "string",
                    "description": "State code (e.g., 'TX', 'CA')"
                },
                "max_price": {
                    "type": "integer",
                    "description": "Maximum price for comparables"
                },
                "min_price": {
                    "type": "integer",
                    "description": "Minimum price for comparables (default: 0)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of comparable properties to return (default: 5)"
                }
            },
            "required": ["city", "state", "max_price"]
        }
    },
    {
        "name": "estimate_repair_costs",
        "description": "Estimate repair costs for a property based on age, size, and condition. Returns light/medium/heavy repair estimates.",
        "parameters": {
            "type": "object",
            "properties": {
                "property_info": {
                    "type": "object",
                    "description": "Property information dictionary containing sqft, year_built, etc."
                }
            },
            "required": ["property_info"]
        }
    },
    {
        "name": "analyze_deal",
        "description": "Perform complete investment analysis including ARV, MAO (Maximum Allowable Offer), ROI, and deal rating. This is the main function that provides the final investment recommendation.",
        "parameters": {
            "type": "object",
            "properties": {
                "property_info": {
                    "type": "object",
                    "description": "Property information dictionary"
                },
                "arv": {
                    "type": "number",
                    "description": "After Repair Value (optional, will estimate if not provided)"
                },
                "repair_costs": {
                    "type": "number",
                    "description": "Total repair costs (optional, will estimate if not provided)"
                }
            },
            "required": ["property_info"]
        }
    }
]


# Map function names to actual functions
FUNCTION_MAP = {
    "get_property_details": get_property_details,
    "get_comparable_properties": get_comparable_properties,
    "estimate_repair_costs": estimate_repair_costs,
    "analyze_deal": analyze_deal
}


def create_deal_analyzer_agent():
    """
    Create the Real Estate Deal Analyzer Assistant

    Returns:
        Assistant object
    """
    assistant = client.beta.assistants.create(
        name="Real Estate Deal Analyzer",
        instructions="""You are an expert real estate investment analyst specializing in fix-and-flip deals.

Your role is to help investors evaluate properties by:
1. Fetching property details from Realtor.com
2. Finding comparable properties to estimate ARV (After Repair Value)
3. Estimating repair costs based on property age and condition
4. Calculating key metrics: MAO (Maximum Allowable Offer), ROI, potential profit
5. Providing clear buy/pass recommendations

WORKFLOW:
When a user provides a property address, follow these steps:
1. Use get_property_details() to fetch the property information
2. Extract city and state from the property
3. Use get_comparable_properties() to find comps and calculate ARV
4. Use estimate_repair_costs() to estimate renovation costs
5. Use analyze_deal() to generate the complete investment analysis
6. Present the analysis clearly with specific numbers and a recommendation

IMPORTANT:
- Always calculate ARV from actual comps, not just estimates
- Consider the 70% rule: MAO = (ARV × 0.70) - Repair Costs
- Flag deals where list price > MAO as risky or poor investments
- Be specific with numbers - investors need concrete data
- Explain your reasoning for repair cost estimates

Output format should be professional and include:
- Property details
- ARV calculation from comps
- Repair cost estimate with reasoning
- Maximum Allowable Offer (MAO)
- ROI and profit potential
- Clear BUY/PASS recommendation""",
        model="gpt-4o",
        tools=[{"type": "function", "function": schema} for schema in FUNCTION_SCHEMAS]
    )

    return assistant


def execute_function_call(function_name: str, arguments: str):
    """
    Execute a function call from the agent

    Args:
        function_name: Name of the function to call
        arguments: JSON string of function arguments

    Returns:
        Function result as JSON string
    """
    try:
        args = json.loads(arguments)
        function = FUNCTION_MAP.get(function_name)

        if not function:
            return json.dumps({"error": f"Function {function_name} not found"})

        result = function(**args)
        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})


def run_deal_analysis(assistant_id: str, user_message: str):
    """
    Run a deal analysis conversation with the agent

    Args:
        assistant_id: The assistant ID
        user_message: User's input (e.g., property address)

    Returns:
        Agent's response
    """
    # Create a thread
    thread = client.beta.threads.create()

    # Add user message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Wait for completion and handle function calls
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run_status.status == "completed":
            break

        elif run_status.status == "requires_action":
            # Handle function calls
            tool_outputs = []

            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\n🔧 Executing: {function_name}")

                output = execute_function_call(function_name, arguments)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output
                })

            # Submit function outputs
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run_status.status in ["failed", "cancelled", "expired"]:
            print(f"❌ Run failed with status: {run_status.status}")
            return None

        # Wait a bit before checking again
        import time
        time.sleep(1)

    # Get the assistant's messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Return the latest assistant message
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value

    return None


if __name__ == "__main__":
    print("🏠 Creating Real Estate Deal Analyzer Agent...\n")

    # Create the assistant
    assistant = create_deal_analyzer_agent()
    print(f"✅ Assistant created with ID: {assistant.id}\n")
    print("📝 Save this ID to reuse the assistant later!\n")

    # Example usage
    print("="*60)
    print("EXAMPLE: Analyze a property")
    print("="*60)

    # Get user input
    property_address = input("\nEnter property address (or press Enter for demo): ").strip()

    if not property_address:
        property_address = "Analyze properties under $300,000 in Austin, TX for fix-and-flip potential"

    print(f"\n🔍 Analyzing: {property_address}\n")

    # Run analysis
    response = run_deal_analysis(assistant.id, property_address)

    if response:
        print("\n" + "="*60)
        print("ANALYSIS RESULT")
        print("="*60)
        print(response)
    else:
        print("\n❌ Analysis failed")
