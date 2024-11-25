import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from langchain_core.tools import tool, StructuredTool

import certifi
from dotenv import load_dotenv
import os
from typing import List, Literal, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup


def _fmp_request(endpoint: str, params: Dict[str, Any] = None, max_retries: int = 3) -> Dict[str, Any]:
    """Make a request to the FMP API with retry logic."""
    load_dotenv()
    try:
        fmp_api_key = os.getenv('FMP_API_KEY')
        base_url = "https://financialmodelingprep.com/api/v3"
    except Exception as e:
        print(f"No FMP_API_KEY found. You can get an API key at https://site.financialmodelingprep.com/: {e}")
        return {"error": f"Error loading FMP API Key: {e}"}
    
    if params is None:
        params = {}
    params['apikey'] = fmp_api_key
    url = f"{base_url}/{endpoint}?{urlencode(params)}"
    
    for attempt in range(max_retries):
        try:
            request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(request, cafile=certifi.where())
            data = response.read().decode("utf-8")

            if not data:
                print(f"Attempt {attempt + 1}: No data returned from API")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return {"error": "No data returned from API"}
            
            results = json.loads(data)
            if not results:
                print(f"Attempt {attempt + 1}: Empty response from API")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return {"error": "Empty response from API"}
            
            if isinstance(results, dict) and "Error Message" in results:
                print(f"API Error: {results['Error Message']}")
                return {"error": results["Error Message"]}
            
            return results
        except HTTPError as e:
            if e.code == 403:
                print("HTTP Error 403: API access forbidden. Please check your API key.")
                return {"error": "API access forbidden. Please check your API key."}
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
                return {"error": f"HTTP Error {e.code}: {e.reason}"}
        except URLError as e:
            print(f"URL Error: {e.reason}")
            return {"error": f"URL Error: {e.reason}"}
        except json.JSONDecodeError:
            print("Invalid JSON response from API")
            return {"error": "Invalid JSON response from API"}
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}
    
    print(f"No valid data after {max_retries} attempts")
    return {"error": f"No valid data after {max_retries} attempts"}

@tool
def generate_single_line_item_query(
    ticker: str,
    statement: Literal["income-statement", "balance-sheet-statement", "cash-flow-statement"] = "income-statement",
    period: Literal["annual", "quarter"] = "annual",
) -> List[dict]:
    """Generate a single line item query for a given ticker."""
    params = {"period": period}
    result = _fmp_request(f"{statement}/{ticker}", params)
    if "error" in result:
        return [result]
    return result

@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch the current stock price for a given symbol."""
    data = _fmp_request(f"quote-short/{symbol}")
    if "error" in data:
        return data
    return {'price': data[0]['price']} if data else {"error": "No price data available"}

@tool
def get_company_profile(symbol: str) -> dict:
    """Fetch the company profile for a given symbol."""
    data = _fmp_request(f"profile/{symbol}")
    if "error" in data:
        return data
    return data[0] if data else {"error": "No company profile data available"}

@tool
def get_financial_ratios(symbol: str, period: Literal["annual", "quarter"] = "annual") -> List[dict]:
    """Fetch financial ratios for a given symbol."""
    params = {"period": period}
    return _fmp_request(f"ratios/{symbol}", params)

@tool
def get_key_metrics(symbol: str, period: Literal["annual", "quarter"] = "annual") -> List[dict]:
    """Fetch key metrics for a given symbol."""
    params = {"period": period}
    return _fmp_request(f"key-metrics/{symbol}", params)

@tool
def get_market_cap(symbol: str) -> dict:
    """Fetch the current market cap for a given symbol."""
    data = _fmp_request(f"market-capitalization/{symbol}")
    return data[0] if data else {"error": "No market cap data available"}

@tool
def get_stock_screener(
    market_cap_more_than: Optional[int] = None,
    market_cap_lower_than: Optional[int] = None,
    price_more_than: Optional[float] = None,
    price_lower_than: Optional[float] = None,
    beta_more_than: Optional[float] = None,
    beta_lower_than: Optional[float] = None,
    volume_more_than: Optional[int] = None,
    volume_lower_than: Optional[int] = None,
    dividend_more_than: Optional[float] = None,
    dividend_lower_than: Optional[float] = None,
    is_etf: Optional[bool] = None,
    is_fund: Optional[bool] = None,
    is_actively_trading: Optional[bool] = None,
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    country: Optional[str] = None,
    exchange: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Fetch stocks based on screening criteria."""
    # Convert camelCase to snake_case using a dictionary comprehension
    params = {
        k: str(v).lower() if isinstance(v, bool) else v
        for k, v in locals().items()
        if v is not None and k != 'limit'
    }
    
    # Convert snake_case to camelCase for API parameters
    api_params = {
        ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(k.split('_'))): v
        for k, v in params.items()
    }
    api_params['limit'] = limit

    return _fmp_request("stock-screener", api_params)

@tool
def read_webpage(url: str) -> str:
    """Read text content from a given webpage URL."""
    try:
        print(f"Agent visiting webpage: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text[:50000]

    except requests.RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"Error processing the webpage: {str(e)}"
