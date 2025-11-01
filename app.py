"""
Flask backend for Real Estate Deal Analyzer with DeepSeek AI
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, DEEPSEEK_API_KEY, DEEPSEEK_API_BASE
from functions.realtor_api import get_property_details, extract_property_info
from functions.deal_calculator import estimate_repair_costs, analyze_deal

app = Flask(__name__, static_folder='frontend')
CORS(app)


def call_deepseek(messages, stream=False):
    """
    Call DeepSeek API for AI analysis

    Args:
        messages: List of message objects with role and content
        stream: Whether to stream the response

    Returns:
        AI response text
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "stream": stream,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            f"{DEEPSEEK_API_BASE}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"Error calling DeepSeek API: {str(e)}"


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_property():
    """
    Main endpoint to analyze a property
    Receives address, fetches data, and returns AI analysis
    """
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Step 1: Use DeepSeek to extract address from user message
        extract_prompt = [
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts property addresses from user messages. Extract ONLY the address in the format: Street, City, State. If no clear address is found, respond with 'NO_ADDRESS_FOUND'."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        address = call_deepseek(extract_prompt).strip()

        if "NO_ADDRESS_FOUND" in address:
            # No specific address, just have a conversation
            general_response = call_deepseek([
                {
                    "role": "system",
                    "content": "You are a real estate investment expert assistant. Help users with general real estate questions."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ])

            return jsonify({
                "type": "conversation",
                "message": general_response
            })

        # Step 2: Fetch property data from Realtor API
        print(f"Fetching property data for: {address}")
        property_result = get_property_details(address)

        if not property_result.get('success'):
            return jsonify({
                "type": "error",
                "message": f"Could not find property at '{address}'. Please provide a valid address."
            })

        # Step 3: Extract and format property info
        raw_property = property_result['property']
        property_info = extract_property_info(raw_property)

        # Step 4: Calculate repair estimates
        repair_estimate = estimate_repair_costs(property_info)

        # Step 5: Perform deal analysis
        deal_analysis = analyze_deal(property_info, repair_costs=repair_estimate['estimated_total'])

        # Step 6: Use DeepSeek to generate detailed analysis with assumptions
        analysis_prompt = [
            {
                "role": "system",
                "content": """You are an expert real estate investment analyst.

Your job is to analyze property data and provide detailed insights including:
1. Property overview with key details
2. Investment analysis (ARV, repair costs, ROI, profit potential)
3. Market assumptions and reasoning
4. Potential risks and opportunities
5. Clear recommendation (BUY/PASS/NEGOTIATE)

Be specific, use actual numbers, and explain your reasoning. Make reasonable assumptions about market conditions and mention them clearly."""
            },
            {
                "role": "user",
                "content": f"""Analyze this property investment opportunity:

USER QUERY: {user_message}

PROPERTY DATA:
{json.dumps(property_info, indent=2)}

CALCULATED METRICS:
{json.dumps(deal_analysis, indent=2)}

REPAIR ESTIMATE:
{json.dumps(repair_estimate, indent=2)}

Please provide a comprehensive analysis with:
1. Property summary
2. Investment metrics breakdown
3. Your assumptions (market trends, neighborhood, buyer demand, etc.)
4. Risk factors
5. Final recommendation

Format your response in a clear, professional manner."""
            }
        ]

        ai_analysis = call_deepseek(analysis_prompt)

        # Step 7: Return comprehensive response
        return jsonify({
            "type": "analysis",
            "property_data": property_info,
            "deal_analysis": deal_analysis,
            "repair_estimate": repair_estimate,
            "ai_analysis": ai_analysis,
            "address": address
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "type": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Simple chat endpoint for general questions
    """
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = call_deepseek([
            {
                "role": "system",
                "content": "You are a helpful real estate investment assistant. Answer questions about real estate investing, property analysis, and market trends."
            },
            {
                "role": "user",
                "content": user_message
            }
        ])

        return jsonify({
            "type": "chat",
            "message": response
        })

    except Exception as e:
        return jsonify({
            "type": "error",
            "message": f"Error: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏠 Real Estate Deal Analyzer - Starting Server")
    print("="*60)
    print("✅ DeepSeek AI: Enabled")
    print("✅ Realtor API: Enabled")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
