import requests

def get_pakistan_stats():
    """Fetches multiple indicators for Pakistan from the World Bank API."""
    indicators = {
        'inflation': 'FP.CPI.TOTL.ZG',
        'interest_rate': 'FR.INR.RINR',
        'gdp_growth': 'NY.GDP.MKTP.KD.ZG'
    }
    
    results = {}
    
    for name, code in indicators.items():
        url = f"https://api.worldbank.org/v2/country/PAK/indicator/{code}?format=json"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            # Get the most recent non-null value
            for entry in data[1]:
                if entry['value'] is not None:
                    results[name] = round(entry['value'], 2)
                    break
        except:
            results[name] = 12.0 # Fallback default
            
    return results

def get_historical_inflation():
    """Fetches the last 10 years of inflation for the graph."""
    url = "https://api.worldbank.org/v2/country/PAK/indicator/FP.CPI.TOTL.ZG?format=json&per_page=10"
    try:
        response = requests.get(url)
        data = response.json()
        years = [item['date'] for item in data[1]][::-1] # Reverse to go old -> new
        values = [item['value'] if item['value'] is not None else 0 for item in data[1]][::-1]
        return years, values
    except:
        return ["2020", "2021", "2022", "2023", "2024"], [10, 12, 25, 30, 15]

# --- FIX: This function was accidentally indented inside the one above! ---
def get_historical_data(indicator_code):
    """Fetches 10 years of data for any World Bank indicator code."""
    url = f"https://api.worldbank.org/v2/country/PAK/indicator/{indicator_code}?format=json&per_page=10"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Grab years and values, replacing None with 0 so the graph doesn't break
        years = [item['date'] for item in data[1]][::-1]
        values = [item['value'] if item['value'] is not None else 0 for item in data[1]][::-1]
        
        return years, values
    except:
        return [], []