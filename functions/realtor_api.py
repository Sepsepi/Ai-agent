"""
Realtor API wrapper for fetching property data
"""

import requests
from typing import Dict, List, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, RAPIDAPI_BASE_URL


def get_property_details(address: str) -> Dict:
    """
    Fetch property details from Realtor API by address

    Args:
        address: Full property address (e.g., "123 Main St, Austin, TX")

    Returns:
        Dictionary containing property details
    """
    url = f"{RAPIDAPI_BASE_URL}/properties/v3/list"

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }

    # Parse address - extract city if possible
    payload = {
        "limit": 1,
        "offset": 0,
        "status": ["for_sale", "ready_to_build"],
        "sort": {"direction": "desc", "field": "list_date"}
    }

    # Try to extract postal code from address
    parts = address.split(',')
    if len(parts) >= 2:
        city = parts[-2].strip()
        state = parts[-1].strip().split()[0] if len(parts) > 2 else ""
        payload["city"] = city
        if state:
            payload["state_code"] = state

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and data["data"].get("home_search"):
            properties = data["data"]["home_search"].get("results", [])
            if properties:
                return {
                    "success": True,
                    "property": properties[0],
                    "raw_data": data
                }

        return {
            "success": False,
            "error": "No property found at this address"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API Error: {str(e)}"
        }


def get_comparable_properties(city: str, state: str, max_price: int, min_price: int = 0, limit: int = 5) -> Dict:
    """
    Fetch comparable properties (comps) in the same area

    Args:
        city: City name
        state: State code (e.g., "TX")
        max_price: Maximum price for comparables
        min_price: Minimum price for comparables
        limit: Number of comps to return

    Returns:
        Dictionary containing comparable properties
    """
    url = f"{RAPIDAPI_BASE_URL}/properties/v3/list"

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }

    payload = {
        "limit": limit,
        "offset": 0,
        "city": city,
        "state_code": state,
        "status": ["for_sale", "sold"],
        "sort": {"direction": "desc", "field": "list_date"},
        "list_price": {"min": min_price, "max": max_price}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and data["data"].get("home_search"):
            properties = data["data"]["home_search"].get("results", [])
            return {
                "success": True,
                "comparables": properties,
                "count": len(properties)
            }

        return {
            "success": False,
            "error": "No comparable properties found"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API Error: {str(e)}"
        }


def extract_property_info(property_data: Dict) -> Dict:
    """
    Extract relevant information from raw property data

    Args:
        property_data: Raw property data from API

    Returns:
        Cleaned and formatted property information
    """
    description = property_data.get("description", {})
    location = property_data.get("location", {})

    return {
        "address": location.get("address", {}).get("line", "N/A"),
        "city": location.get("address", {}).get("city", "N/A"),
        "state": location.get("address", {}).get("state_code", "N/A"),
        "zip_code": location.get("address", {}).get("postal_code", "N/A"),
        "price": property_data.get("list_price", 0),
        "bedrooms": description.get("beds", 0),
        "bathrooms": description.get("baths", 0),
        "sqft": description.get("sqft", 0),
        "lot_sqft": description.get("lot_sqft", 0),
        "year_built": description.get("year_built", "N/A"),
        "property_type": description.get("type", "N/A"),
        "status": property_data.get("status", "N/A"),
        "days_on_market": property_data.get("list_date", "N/A"),
        "description_text": description.get("text", ""),
    }
