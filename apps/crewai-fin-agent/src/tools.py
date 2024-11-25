from crewai.tools import BaseTool
from typing import Type, List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
import certifi
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

# Helper function remains the same
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

class LineItemQueryInput(BaseModel):
    """Input schema for generating single line item queries."""
    ticker: str = Field(..., description="The stock ticker symbol")
    statement: Literal["income-statement", "balance-sheet-statement", "cash-flow-statement"] = Field(
        default="income-statement",
        description="Type of financial statement to query"
    )
    period: Literal["annual", "quarter"] = Field(
        default="annual",
        description="Period of the financial statement"
    )

class SingleLineItemQueryTool(BaseTool):
    name: str = "Generate Single Line Item Query"
    description: str = "Generate a single line item query for a given ticker's financial statements"
    args_schema: Type[BaseModel] = LineItemQueryInput

    def _run(self, ticker: str, statement: str = "income-statement", period: str = "annual") -> List[dict]:
        params = {"period": period}
        result = _fmp_request(f"{statement}/{ticker}", params)
        if "error" in result:
            return [result]
        return result

class StockPriceInput(BaseModel):
    """Input schema for stock price queries."""
    symbol: str = Field(..., description="The stock ticker symbol")

class StockPriceTool(BaseTool):
    name: str = "Get Stock Price"
    description: str = "Fetch the current stock price for a given symbol"
    args_schema: Type[BaseModel] = StockPriceInput

    def _run(self, symbol: str) -> dict:
        data = _fmp_request(f"quote-short/{symbol}")
        if "error" in data:
            return data
        return {'price': data[0]['price']} if data else {"error": "No price data available"}

class CompanyProfileInput(BaseModel):
    """Input schema for company profile queries."""
    symbol: str = Field(..., description="The stock ticker symbol")

class CompanyProfileTool(BaseTool):
    name: str = "Get Company Profile"
    description: str = "Fetch detailed company profile information for a given symbol"
    args_schema: Type[BaseModel] = CompanyProfileInput

    def _run(self, symbol: str) -> dict:
        data = _fmp_request(f"profile/{symbol}")
        if "error" in data:
            return data
        return data[0] if data else {"error": "No company profile data available"}

class FinancialRatiosInput(BaseModel):
    """Input schema for financial ratios queries."""
    symbol: str = Field(..., description="The stock ticker symbol")
    period: Literal["annual", "quarter"] = Field(
        default="annual",
        description="Period of the financial ratios"
    )

class FinancialRatiosTool(BaseTool):
    name: str = "Get Financial Ratios"
    description: str = "Fetch financial ratios for a given symbol"
    args_schema: Type[BaseModel] = FinancialRatiosInput

    def _run(self, symbol: str, period: str = "annual") -> List[dict]:
        params = {"period": period}
        return _fmp_request(f"ratios/{symbol}", params)

class MarketCapInput(BaseModel):
    """Input schema for market cap queries."""
    symbol: str = Field(..., description="The stock ticker symbol")

class MarketCapTool(BaseTool):
    name: str = "Get Market Cap"
    description: str = "Fetch the current market cap for a given symbol"
    args_schema: Type[BaseModel] = MarketCapInput

    def _run(self, symbol: str) -> dict:
        data = _fmp_request(f"market-capitalization/{symbol}")
        return data[0] if data else {"error": "No market cap data available"}

class KeyMetricsInput(BaseModel):
    """Input schema for key metrics queries."""
    symbol: str = Field(..., description="The stock ticker symbol")
    period: Literal["annual", "quarter"] = Field(
        default="annual",
        description="Period of the key metrics"
    )

class KeyMetricsTool(BaseTool):
    name: str = "Get Key Metrics"
    description: str = "Fetch key metrics for a given symbol"
    args_schema: Type[BaseModel] = KeyMetricsInput

    def _run(self, symbol: str, period: str = "annual") -> List[dict]:
        params = {"period": period}
        return _fmp_request(f"key-metrics/{symbol}", params)

class StockScreenerInput(BaseModel):
    """Input schema for stock screener."""
    market_cap_more_than: Optional[int] = Field(None, description="Minimum market cap")
    market_cap_lower_than: Optional[int] = Field(None, description="Maximum market cap")
    price_more_than: Optional[float] = Field(None, description="Minimum price")
    price_lower_than: Optional[float] = Field(None, description="Maximum price")
    beta_more_than: Optional[float] = Field(None, description="Minimum beta")
    beta_lower_than: Optional[float] = Field(None, description="Maximum beta")
    volume_more_than: Optional[int] = Field(None, description="Minimum volume")
    volume_lower_than: Optional[int] = Field(None, description="Maximum volume")
    dividend_more_than: Optional[float] = Field(None, description="Minimum dividend")
    dividend_lower_than: Optional[float] = Field(None, description="Maximum dividend")
    is_etf: Optional[bool] = Field(None, description="Filter for ETFs")
    is_fund: Optional[bool] = Field(None, description="Filter for funds")
    is_actively_trading: Optional[bool] = Field(None, description="Filter for actively trading stocks")
    sector: Optional[str] = Field(None, description="Filter by sector")
    industry: Optional[str] = Field(None, description="Filter by industry")
    country: Optional[str] = Field(None, description="Filter by country")
    exchange: Optional[str] = Field(None, description="Filter by exchange")
    limit: int = Field(default=10, description="Maximum number of results to return")

class StockScreenerTool(BaseTool):
    name: str = "Stock Screener"
    description: str = "Screen stocks based on various financial and market criteria"
    args_schema: Type[BaseModel] = StockScreenerInput

    def _run(
        self,
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
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        
        # Convert boolean values to strings
        for key in ['is_etf', 'is_fund', 'is_actively_trading']:
            if key in params:
                params[key] = str(params[key]).lower()

        return _fmp_request("stock-screener", params) 
    

class WebpageReadingInput(BaseModel):
    """Input schema for web scraping."""
    url: str = Field(..., description="The URL of the website to scrape")

class WebpageReadingTool(BaseTool):
    name: str = "Web Scraping"
    description: str = "Read a given website and extract the text content"
    args_schema: Type[BaseModel] = WebpageReadingInput

    def _run(self, url: str) -> str:
        try:
            # Send GET request with a user agent to avoid blocking
            print(f"Agent visiting webpage: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract text content
            text = soup.get_text(separator='\n', strip=True)

            # Clean up text (remove excessive newlines and spaces)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text[:50000]  # Limit response size to 50k characters

        except requests.RequestException as e:
            return f"Error fetching the webpage: {str(e)}"
        except Exception as e:
            return f"Error processing the webpage: {str(e)}"