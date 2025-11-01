# 🏠 Real Estate Deal Analyzer Agent

An AI-powered automation tool that analyzes real estate investment opportunities using **DeepSeek AI** and live property data from **Realtor.com API**.

> **Built for:** AI Automation Specialist Demo - Real Estate Investing Sector

## 🎯 What It Does

This agent automates the entire deal analysis process for fix-and-flip real estate investments:

1. **Fetches Live Property Data** - Gets current listings from Realtor.com
2. **Finds Comparable Sales** - Pulls comps to calculate ARV (After Repair Value)
3. **Estimates Repair Costs** - Analyzes property age/condition for renovation estimates
4. **Calculates Investment Metrics** - Computes MAO, ROI, potential profit
5. **Provides Recommendations** - Clear BUY/PASS guidance based on the 70% rule

## 🚀 Quick Start (Ready in 30 seconds!)

### Prerequisites
- Python 3.8+
- ✅ API keys are **already configured** in `.env`

### Installation & Launch

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open browser to http://localhost:5000
```

**That's it!** The chat interface will open where you can analyze properties.

### Alternative: Command Line Demo
```bash
python demo.py  # Interactive CLI version
python agent.py # OpenAI Assistants API version
```

## 📊 Example Output

```
DEAL ANALYSIS REPORT
============================================================

PROPERTY DETAILS
----------------
Address: 123 Main St, Austin, TX 78701
Current List Price: $285,000.00

VALUATION
---------
After Repair Value (ARV): $380,000.00
Estimated Repairs (medium): $45,000.00
Maximum Allowable Offer (MAO): $221,000.00

INVESTMENT ANALYSIS
-------------------
Total Investment Required: $335,400.00
Potential Profit: $44,600.00
Return on Investment (ROI): 13.30%

DEAL RATING: MARGINAL
============================================================

RECOMMENDATION
--------------
Risky - only proceed if you can negotiate significantly
```

## 🔧 How It Works

### Architecture

```
User Input (Property Address in Chat)
        ↓
Flask Backend (app.py)
        ↓
┌──────────────────────────────────┐
│   DeepSeek AI extracts address   │
└──────────────────────────────────┘
        ↓
┌──────────────────────────────────┐
│  Fetch Live Property Data        │
│  from Realtor API (RapidAPI)     │
└──────────────────────────────────┘
        ↓
┌──────────────────────────────────┐
│  Calculate Investment Metrics:   │
│  • ARV (from comps)              │
│  • Repair costs (age-based)      │
│  • MAO (70% rule)                │
│  • ROI & Profit                  │
└──────────────────────────────────┘
        ↓
┌──────────────────────────────────┐
│  DeepSeek AI generates:          │
│  • Detailed analysis             │
│  • Market assumptions            │
│  • Risk assessment               │
│  • BUY/PASS recommendation       │
└──────────────────────────────────┘
        ↓
Beautiful Chat UI with Property Card
```

### Key Features

- **Live Market Data**: Real-time property listings from Realtor.com
- **Smart ARV Calculation**: Based on actual comparable sales
- **Automated Repair Estimates**: Age and condition-based cost modeling
- **70% Rule Validation**: Industry-standard investment analysis
- **Deal Rating System**: EXCELLENT/GOOD/MARGINAL/POOR classifications

## 💡 Demo Ideas for Job Interview

### What This Demonstrates

✅ **AI Automation Skills**
- OpenAI Assistants API integration
- Function calling implementation
- Multi-step autonomous workflows

✅ **Real Estate Domain Knowledge**
- Understanding of ARV, MAO, ROI
- Fix-and-flip investment strategies
- Market analysis fundamentals

✅ **API Integration**
- RapidAPI/Realtor.com data fetching
- Error handling and data validation
- Rate limiting considerations

✅ **Production-Ready Code**
- Clean architecture with separation of concerns
- Configuration management
- Error handling and logging

### Expansion Ideas

You can enhance this demo with:

1. **n8n Integration** - Trigger analysis via webhook when new listings appear
2. **Email Reports** - Auto-send analysis to investors
3. **CRM Integration** - Push qualified deals to Airtable/Google Sheets
4. **SMS Alerts** - Notify when EXCELLENT deals are found
5. **Multi-property Analysis** - Batch analyze entire neighborhoods

## 📝 Files Overview

```
deal-analyzer-agent/
├── agent.py                 # Main OpenAI Assistant logic
├── demo.py                  # Interactive demo interface
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── functions/
│   ├── realtor_api.py      # Realtor.com API wrapper
│   └── deal_calculator.py  # Investment calculations
└── README.md               # This file
```

## 🎥 Demo Script

**For your interview, follow this flow:**

1. **Intro** (30 seconds)
   - "I built an AI agent that automates real estate deal analysis"
   - Show this README

2. **Live Demo** (2-3 minutes)
   - Run `python demo.py`
   - Analyze 2-3 real properties
   - Show the output and explain metrics

3. **Code Walkthrough** (2 minutes)
   - Show `agent.py` - explain OpenAI function calling
   - Show `deal_calculator.py` - explain 70% rule
   - Show how it could integrate with n8n

4. **Value Proposition** (1 minute)
   - "Saves investors 30-60 minutes per property"
   - "Analyzes 100+ properties in the time it takes to manually review 1"
   - "Could be automated with n8n to run 24/7"

## 🔑 Key Metrics This Calculates

- **ARV** (After Repair Value): What the property will be worth after renovations
- **MAO** (Maximum Allowable Offer): Highest price to pay and still profit
- **ROI** (Return on Investment): Percentage return on total investment
- **Repair Costs**: Estimated renovation expenses
- **Profit Margin**: Expected profit after all costs

## 📚 Resources

- [OpenAI Assistants API Docs](https://platform.openai.com/docs/assistants)
- [RapidAPI Realtor API](https://rapidapi.com/datascraper/api/realty-in-us)
- [Fix-and-Flip 70% Rule Explained](https://www.investopedia.com/articles/mortgages-real-estate/08/house-flip.asp)

## 🤝 Interview Talking Points

- "This demonstrates my ability to build AI automations that solve real business problems"
- "I chose real estate because it's directly relevant to your use case"
- "The agent uses function calling to autonomously fetch data and make calculations"
- "With n8n, this could run automatically whenever new listings appear"
- "I can extend this to handle rental property analysis, market reports, etc."

---

Built with ❤️ for real estate investors
