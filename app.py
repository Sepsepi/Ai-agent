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
        # Step 1: Use DeepSeek to parse the request
        parse_prompt = [
            {
                "role": "system",
                "content": "Extract: city, state, max_price, count. Reply ONLY in JSON format: {\"city\":\"Austin\",\"state\":\"TX\",\"max_price\":500000,\"count\":3}. If no address found, reply: {\"error\":\"no_location\"}"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        parsed = call_deepseek(parse_prompt).strip()

        # Try to parse JSON response
        try:
            query_params = json.loads(parsed)
        except:
            # If JSON parsing fails, return error
            return jsonify({
                "type": "error",
                "message": "Please specify a city and state (e.g., 'Austin, TX' or 'properties in Dallas, TX under 300k')"
            })

        if query_params.get("error"):
            return jsonify({
                "type": "error",
                "message": "Please specify a city and state (e.g., 'Austin, TX' or '3 deals in Miami, FL under 500k')"
            })

        # Step 2: Fetch properties from Realtor API
        city = query_params.get("city", "")
        state = query_params.get("state", "")
        max_price = query_params.get("max_price", 1000000)
        count = min(query_params.get("count", 1), 3)  # Max 3 properties

        print(f"Fetching {count} properties in {city}, {state} under ${max_price}")

        from functions.realtor_api import get_comparable_properties
        comps_result = get_comparable_properties(city, state, max_price, limit=count)

        if not comps_result.get('success'):
            return jsonify({
                "type": "error",
                "message": f"Could not find properties in {city}, {state}"
            })

        # Step 3: Analyze each property
        properties = comps_result['comparables']
        results = []

        for raw_property in properties:
            property_info = extract_property_info(raw_property)
            repair_estimate = estimate_repair_costs(property_info)
            deal_analysis = analyze_deal(property_info, repair_costs=repair_estimate['estimated_total'])

            # Quick AI analysis for each
            analysis_prompt = [
                {
                    "role": "system",
                    "content": "Brief analysis: deal summary, key risks, recommendation. 3 sentences max."
                },
                {
                    "role": "user",
                    "content": f"${property_info.get('price'):,} | ARV: ${deal_analysis.get('arv'):,} | Repairs: ${deal_analysis.get('estimated_repairs'):,} | ROI: {deal_analysis.get('roi_percentage')}% | Rating: {deal_analysis.get('deal_rating')}"
                }
            ]

            ai_analysis = call_deepseek(analysis_prompt)

            results.append({
                "property_data": property_info,
                "deal_analysis": deal_analysis,
                "repair_estimate": repair_estimate,
                "ai_analysis": ai_analysis
            })

        # Return all results
        return jsonify({
            "type": "analysis",
            "properties": results,
            "count": len(results),
            "query": f"{count} properties in {city}, {state} under ${max_price:,}"
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
