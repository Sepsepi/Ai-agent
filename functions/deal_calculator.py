"""
Real Estate Investment Deal Calculator
Calculates key metrics for fix-and-flip and rental properties
"""

from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    DEFAULT_HOLDING_PERIOD,
    DEFAULT_FINANCING_RATE,
    DEFAULT_CLOSING_COSTS_PERCENT,
    DEFAULT_PROFIT_MARGIN_TARGET,
    ARV_MULTIPLIER
)


def calculate_arv_from_comps(comparable_properties: List[Dict]) -> float:
    """
    Calculate After Repair Value (ARV) based on comparable properties

    Args:
        comparable_properties: List of comparable property data

    Returns:
        Estimated ARV (average of comps)
    """
    if not comparable_properties:
        return 0

    prices = [comp.get("list_price", 0) for comp in comparable_properties if comp.get("list_price")]

    if not prices:
        return 0

    return sum(prices) / len(prices)


def estimate_repair_costs(property_info: Dict) -> Dict:
    """
    Estimate repair costs based on property details

    Args:
        property_info: Property information dictionary

    Returns:
        Dictionary with repair cost estimates
    """
    sqft = property_info.get("sqft", 0)
    year_built = property_info.get("year_built", 2020)

    # Default per sqft repair costs
    # Light: $10-15/sqft, Medium: $25-35/sqft, Heavy: $50-75/sqft
    current_year = 2025
    age = current_year - int(year_built) if isinstance(year_built, (int, str)) and str(year_built).isdigit() else 0

    if age < 10:
        repair_level = "light"
        cost_per_sqft = 12.50
    elif age < 30:
        repair_level = "medium"
        cost_per_sqft = 30
    else:
        repair_level = "heavy"
        cost_per_sqft = 62.50

    estimated_repairs = sqft * cost_per_sqft

    return {
        "repair_level": repair_level,
        "cost_per_sqft": cost_per_sqft,
        "estimated_total": round(estimated_repairs, 2),
        "breakdown": {
            "light": round(sqft * 12.50, 2),
            "medium": round(sqft * 30, 2),
            "heavy": round(sqft * 62.50, 2)
        }
    }


def calculate_max_allowable_offer(arv: float, repair_costs: float, target_profit_percent: float = DEFAULT_PROFIT_MARGIN_TARGET) -> Dict:
    """
    Calculate Maximum Allowable Offer (MAO) using the 70% rule

    Args:
        arv: After Repair Value
        repair_costs: Estimated repair costs
        target_profit_percent: Target profit margin (default 20%)

    Returns:
        Dictionary with MAO calculation details
    """
    # 70% Rule: MAO = (ARV × 0.70) - Repair Costs
    traditional_mao = (arv * ARV_MULTIPLIER) - repair_costs

    # Alternative: Target profit method
    # MAO = ARV - Repair Costs - Target Profit - Holding Costs
    target_profit = arv * target_profit_percent
    estimated_holding_costs = arv * 0.02  # 2% of ARV for holding costs
    profit_based_mao = arv - repair_costs - target_profit - estimated_holding_costs

    return {
        "traditional_mao": round(traditional_mao, 2),
        "profit_based_mao": round(profit_based_mao, 2),
        "recommended_mao": round(min(traditional_mao, profit_based_mao), 2),
        "arv": round(arv, 2),
        "repair_costs": round(repair_costs, 2),
        "target_profit": round(target_profit, 2),
        "estimated_holding_costs": round(estimated_holding_costs, 2)
    }


def analyze_deal(property_info: Dict, arv: float = None, repair_costs: float = None) -> Dict:
    """
    Complete deal analysis for a property

    Args:
        property_info: Property information dictionary
        arv: After Repair Value (optional, will estimate if not provided)
        repair_costs: Repair costs (optional, will estimate if not provided)

    Returns:
        Complete deal analysis with all metrics
    """
    current_price = property_info.get("price", 0)

    # Estimate repair costs if not provided
    if repair_costs is None:
        repair_estimate = estimate_repair_costs(property_info)
        repair_costs = repair_estimate["estimated_total"]
    else:
        repair_estimate = {"estimated_total": repair_costs, "repair_level": "user_provided"}

    # Use provided ARV or estimate at 115% of current price (conservative)
    if arv is None:
        arv = current_price * 1.15

    # Calculate MAO
    mao_calc = calculate_max_allowable_offer(arv, repair_costs)

    # Calculate potential profit
    total_cost = current_price + repair_costs + mao_calc["estimated_holding_costs"]
    potential_profit = arv - total_cost
    roi = (potential_profit / total_cost * 100) if total_cost > 0 else 0

    # Determine deal quality
    if current_price <= mao_calc["recommended_mao"]:
        deal_rating = "EXCELLENT"
        recommendation = "Strong buy - property is below MAO"
    elif current_price <= mao_calc["recommended_mao"] * 1.05:
        deal_rating = "GOOD"
        recommendation = "Negotiate - close to MAO, try to lower price"
    elif current_price <= mao_calc["recommended_mao"] * 1.15:
        deal_rating = "MARGINAL"
        recommendation = "Risky - only proceed if you can negotiate significantly"
    else:
        deal_rating = "POOR"
        recommendation = "Pass - property is overpriced for investment"

    return {
        "property_address": property_info.get("address", "N/A"),
        "current_list_price": current_price,
        "arv": round(arv, 2),
        "estimated_repairs": round(repair_costs, 2),
        "repair_level": repair_estimate.get("repair_level", "unknown"),
        "max_allowable_offer": mao_calc["recommended_mao"],
        "total_investment": round(total_cost, 2),
        "potential_profit": round(potential_profit, 2),
        "roi_percentage": round(roi, 2),
        "deal_rating": deal_rating,
        "recommendation": recommendation,
        "detailed_breakdown": {
            "purchase_price": current_price,
            "repair_costs": round(repair_costs, 2),
            "holding_costs": mao_calc["estimated_holding_costs"],
            "selling_costs": round(arv * 0.08, 2),  # 8% for selling costs
            "total_costs": round(total_cost, 2),
            "arv": round(arv, 2),
            "net_profit": round(potential_profit, 2)
        }
    }


def format_deal_analysis_report(analysis: Dict) -> str:
    """
    Format deal analysis into a readable report

    Args:
        analysis: Deal analysis dictionary

    Returns:
        Formatted string report
    """
    report = f"""
{'='*60}
DEAL ANALYSIS REPORT
{'='*60}

PROPERTY DETAILS
----------------
Address: {analysis['property_address']}
Current List Price: ${analysis['current_list_price']:,.2f}

VALUATION
---------
After Repair Value (ARV): ${analysis['arv']:,.2f}
Estimated Repairs ({analysis['repair_level']}): ${analysis['estimated_repairs']:,.2f}
Maximum Allowable Offer (MAO): ${analysis['max_allowable_offer']:,.2f}

INVESTMENT ANALYSIS
-------------------
Total Investment Required: ${analysis['total_investment']:,.2f}
Potential Profit: ${analysis['potential_profit']:,.2f}
Return on Investment (ROI): {analysis['roi_percentage']:.2f}%

DEAL RATING: {analysis['deal_rating']}
{'='*60}

RECOMMENDATION
--------------
{analysis['recommendation']}

COST BREAKDOWN
--------------
Purchase Price:     ${analysis['detailed_breakdown']['purchase_price']:,.2f}
Repair Costs:       ${analysis['detailed_breakdown']['repair_costs']:,.2f}
Holding Costs:      ${analysis['detailed_breakdown']['holding_costs']:,.2f}
Selling Costs (8%): ${analysis['detailed_breakdown']['selling_costs']:,.2f}
                    {'─'*40}
Total Costs:        ${analysis['detailed_breakdown']['total_costs']:,.2f}
ARV:                ${analysis['detailed_breakdown']['arv']:,.2f}
                    {'─'*40}
Net Profit:         ${analysis['detailed_breakdown']['net_profit']:,.2f}

{'='*60}
"""
    return report
