# 🚀 Quick Start Guide

## Setup (2 minutes)

### 1. Install Dependencies
```bash
cd /Users/sepsepi/Desktop/HouseAi/deal-analyzer-agent
pip install -r requirements.txt
```

### 2. Verify API Keys
Your `.env` file is already configured with:
- ✅ RapidAPI Key (Realtor API)
- ✅ DeepSeek API Key

### 3. Start the Server
```bash
python app.py
```

### 4. Open the Frontend
Open your browser to: **http://localhost:5000**

---

## How to Use

### Chat Interface
1. Type any property address in the chatbox
2. AI will:
   - Extract the address
   - Fetch live property data from Realtor.com
   - Calculate investment metrics (ARV, ROI, profit)
   - Generate detailed analysis with DeepSeek AI
   - Provide assumptions about market, repairs, risks

### Example Queries

**Analyze specific property:**
```
Analyze 123 Main St, Austin, TX 78701
```

**Search for deals:**
```
Find fix-and-flip opportunities under $300k in Dallas, TX
```

**General questions:**
```
What makes a good real estate investment?
How do I calculate ARV?
```

---

## What You'll See

The AI will provide:

1. **Property Details**
   - Price, bedrooms, bathrooms, sqft, year built
   - Property type and status

2. **Investment Metrics**
   - ARV (After Repair Value)
   - Repair costs estimate
   - Maximum Allowable Offer (MAO)
   - Potential profit
   - ROI percentage
   - Deal rating (EXCELLENT/GOOD/MARGINAL/POOR)

3. **AI Analysis**
   - Market assumptions (neighborhood trends, buyer demand)
   - Repair reasoning (why light/medium/heavy rehab)
   - Risk factors (market volatility, competition)
   - Opportunities (appreciation potential, rental income)
   - Clear BUY/PASS/NEGOTIATE recommendation

---

## Demo Flow for Job Interview

**1. Introduction (30 sec)**
- "I built an AI automation that analyzes real estate deals using DeepSeek AI and live market data"

**2. Show the Interface (1 min)**
- Open http://localhost:5000
- Show the clean, professional chatbox design

**3. Live Demo (3-4 min)**
- Enter a real property address
- Watch it fetch live data
- Show the AI analysis with assumptions
- Try 2-3 different properties

**4. Explain the Automation (2 min)**
- "This could be integrated with n8n to:"
  - Auto-analyze new listings when they appear
  - Send email alerts for EXCELLENT deals
  - Push qualified leads to CRM
  - Generate daily market reports

**5. Show the Code (1 min)**
- Open `app.py` - show DeepSeek integration
- Open `functions/deal_calculator.py` - show investment math
- Explain how it uses function calling and AI reasoning

---

## Key Talking Points

✅ **AI Automation**
- Uses DeepSeek AI for intelligent analysis
- Automatically fetches live property data
- Makes reasoned assumptions about market conditions

✅ **Real Estate Expertise**
- Implements 70% rule for fix-and-flip
- Calculates ARV, MAO, ROI correctly
- Provides actionable recommendations

✅ **Production Ready**
- Clean architecture
- Error handling
- RESTful API design
- Responsive frontend

✅ **Scalable with n8n**
- Could trigger on new listings
- Auto-send reports via email/SMS
- Integrate with Airtable, Google Sheets, CRM
- Run 24/7 automated deal finding

---

## API Endpoints

### POST `/api/analyze`
Analyzes a property from user message
```json
{
  "message": "Analyze 123 Main St, Austin, TX"
}
```

Returns:
- Property data
- Investment metrics
- AI analysis with assumptions

### POST `/api/chat`
General real estate questions
```json
{
  "message": "What is ARV?"
}
```

---

## Technologies Used

- **Backend**: Flask (Python)
- **AI**: DeepSeek API (chat completions)
- **Data**: RapidAPI Realtor API
- **Frontend**: HTML, CSS, JavaScript
- **Calculations**: Custom investment math (70% rule, ROI, ARV)

---

## Next Steps (Future Enhancements)

1. **n8n Integration**
   - Webhook triggers for new listings
   - Automated email reports
   - CRM push for qualified deals

2. **Additional Features**
   - Rental property analysis (cash flow, cap rate)
   - Neighborhood comparisons
   - Market trend charts
   - Property photo analysis

3. **Database**
   - Save analyzed properties
   - Track deal history
   - Build investment portfolio

---

## Troubleshooting

**Server won't start?**
```bash
pip install -r requirements.txt
```

**API errors?**
- Check `.env` file has correct keys
- Verify RapidAPI subscription is active
- Check DeepSeek API key is valid

**No property data?**
- Use full address format: "Street, City, State"
- Try different properties
- Check RapidAPI quota (500 requests/month free)

---

**Ready to impress! 🚀**
