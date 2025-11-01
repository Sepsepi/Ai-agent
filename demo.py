"""
Simple demo interface for Real Estate Deal Analyzer Agent
"""

from agent import create_deal_analyzer_agent, run_deal_analysis
import sys


def main():
    print("\n" + "="*60)
    print("🏠 REAL ESTATE DEAL ANALYZER AGENT - DEMO")
    print("="*60)
    print("\nThis AI agent analyzes real estate investment opportunities")
    print("using live data from Realtor.com\n")

    # Create or load assistant
    print("🔧 Initializing AI Agent...")

    # You can save the assistant_id and reuse it
    # For demo, we create a new one each time
    assistant = create_deal_analyzer_agent()
    assistant_id = assistant.id

    print(f"✅ Agent ready! (ID: {assistant_id})\n")

    print("="*60)
    print("DEMO EXAMPLES - Try these:")
    print("="*60)
    print("1. Analyze 123 Main St, Austin, TX")
    print("2. Find fix-and-flip deals under $250k in Miami, FL")
    print("3. What's the ARV for properties near downtown Dallas?")
    print("="*60 + "\n")

    while True:
        user_input = input("📍 Enter property address or question (or 'quit' to exit): ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using the Deal Analyzer Agent!\n")
            break

        if not user_input:
            print("⚠️  Please enter a property address or question\n")
            continue

        print(f"\n🔍 Analyzing: {user_input}")
        print("⏳ This may take 10-30 seconds...\n")

        # Run the analysis
        response = run_deal_analysis(assistant_id, user_input)

        if response:
            print("\n" + "="*60)
            print("📊 ANALYSIS RESULT")
            print("="*60)
            print(response)
            print("="*60 + "\n")
        else:
            print("\n❌ Analysis failed. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        sys.exit(1)
