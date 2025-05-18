from typing import Any, Dict, List, Optional
import httpx
import os
import pathlib
import base64
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("drawing-explorer")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
def get_drawings_list() -> List[Dict[str, Any]]:
    """Get a list of available technical drawings with metadata.
    
    Returns:
        A list of dictionaries, each containing information about a drawing:
        - filename: The filename of the drawing
        - path: The full path to the drawing file
        - description: A brief description of the drawing
    """
    drawings_dir = pathlib.Path("./drawings")
    
    # Ensure the drawings directory exists
    if not drawings_dir.exists():
        return []
    
    drawings = []
    # Include both jpg and jpeg files
    for file_path in drawings_dir.glob("*.jp*g"):
        # Metadata with placeholder descriptions
        drawing_metadata = {
            "filename": file_path.name,
            "path": str(file_path),
            "description": get_drawing_description(file_path.name)
        }
        drawings.append(drawing_metadata)
    
    return drawings

def get_drawing_description(filename: str) -> str:
    """Return a placeholder description for a drawing based on filename.
    
    Args:
        filename: The name of the drawing file
        
    Returns:
        A description string for the drawing
    """
    descriptions = {
        "US1730270_gear_actuator.jpg": "Technical drawing of a gear actuator mechanism from US patent 1730270.",
        "Wright_brothers_patent_plans_1908.jpg": "Patent drawing of the Wright brothers' flying machine from 1908.",
        "peaucellier-lipkin-linkage.jpeg": "Drawing of the Peaucellier-Lipkin linkage, a mechanical device that converts circular motion to perfect straight-line motion."
    }
    
    return descriptions.get(filename, "No description available")

@mcp.tool()
def getDrawing(filename: str) -> Optional[Dict[str, Any]]:
    """Get a specific drawing by filename.
    
    Args:
        filename: The filename of the drawing to retrieve
        
    Returns:
        A dictionary containing the drawing data and metadata:
        - filename: The filename of the drawing
        - description: A brief description of the drawing
        - image_data: Base64-encoded image data
        
    If the drawing is not found, returns None.
    """
    drawings_dir = pathlib.Path("./drawings")
    file_path = drawings_dir / filename
    
    # Check if the file exists
    if not file_path.exists():
        return None
    
    # Read the image data and encode as base64
    with open(file_path, "rb") as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # Return the drawing data with metadata
    return {
        "filename": filename,
        "description": get_drawing_description(filename),
        "image_data": image_base64
    }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')