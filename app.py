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
            json=payload,
            timeout=15  # 15 second timeout
        )
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.Timeout:
        return "DeepSeek API timeout - please try again"
    except Exception as e:
        return f"Error calling DeepSeek API: {str(e)}"


@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('frontend', path)


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
        # Step 1: Extract city/state from user message (simple string parsing, no AI needed)
        # Just use the message directly - the API will search by city
        address = user_message.strip()

        # If message is too vague, ask for clarification
        if len(address) < 3:
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

        # Step 6: Use DeepSeek to generate brief analysis (shortened prompt for speed)
        analysis_prompt = [
            {
                "role": "system",
                "content": "You are a real estate analyst. Analyze the property data and provide: deal summary, market assumptions, risks, and recommendation (BUY/PASS/NEGOTIATE). Be concise."
            },
            {
                "role": "user",
                "content": f"""Property: {property_info.get('address')}
Price: ${property_info.get('price'):,}
ARV: ${deal_analysis.get('arv'):,}
Repairs: ${deal_analysis.get('estimated_repairs'):,}
ROI: {deal_analysis.get('roi_percentage')}%
Rating: {deal_analysis.get('deal_rating')}

Analyze this deal briefly."""
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
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "type": "error",
            "message": f"Server error: {str(e)}"
        }), 200  # Return 200 so frontend gets JSON


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
