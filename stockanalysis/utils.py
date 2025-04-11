from bs4 import BeautifulSoup
import requests

def scrap_stock_data(symbol,exchange):
    if exchange == 'NASDAQ':
        url = f"https://finance.yahoo.com/quote/{symbol}"
    elif exchange == 'NSE':
        url=f"https://finance.yahoo.com/quote/{symbol}.NS/"
    
    headers = {"User-Agent": "Mozilla/5.0"}  # Important to avoid getting blocked
    

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # previous price
            current_price_tag = soup.find("span", {"data-testid": "qsp-price"})
            current_price = current_price_tag.text if current_price_tag else "Price not found"
            
            # Price changed
            price_change_tag = soup.find("span", {"data-testid": "qsp-price-change"})
            price_changed = price_change_tag.text if price_change_tag else "Price change not found"
            
            # Percentage changed
            percent_change_tag = soup.find("span", {"data-testid": "qsp-price-change-percent"})
            percent_changed = percent_change_tag.text if percent_change_tag else "Percent change not found"
            
            # 52 Week range 
            week_52_range = soup.find("fin-streamer", {"data-field": "fiftyTwoWeekRange"}).text
            week_52_low,week_52_high=week_52_range.split(' - ')
            
            
            # Market Cap
            market_cap = soup.find("fin-streamer", {"data-field": "marketCap"}).text
            
            # Pe Ratio
            pe_ratio=soup.find("fin-streamer", {"data-field": "trailingPE"}).text

            # Dividend Yield 
            dividend_yield_tag = soup.find("span", {"title": "Forward Dividend & Yield"})
            dividend_yield = dividend_yield_tag.find_next_sibling("span").text.strip() if dividend_yield_tag else "Not found"

            
            # previous close 
            previous_close_tag = soup.find("fin-streamer", {"data-field": "regularMarketPreviousClose"})
            previous_close = previous_close_tag.text if previous_close_tag else "Previous Close not found"
    
            stock_response={
                'current_price':current_price,
                'previous_close':previous_close,
                'price_changed':price_changed,
                'percentage_changed':percent_changed,
                'week_52_high':week_52_high,
                'week_52_low':week_52_low,
                'market_cap':market_cap,
                'pe_ratio':pe_ratio,
                'dividend_yield':dividend_yield,
            }
            return stock_response
        
    except Exception as e:
        #print(f"Error scraping the data:{e}")
        return None


