from requests.exceptions import RequestException
import requests
import json
import csv

def crawl_data(amazon_serp_url: str) -> str:
    SCRAPER = "amazon-serp"
    API_TOKEN = "<Crawlbase Normal requests token>"
    API_ENDPOINT = "https://api.crawlbase.com/"

    # Prepare the API request parameters
    params = {
        "token": API_TOKEN,
        "url": amazon_serp_url,    # Target Amazon search URL
        "scraper": SCRAPER 
    }

    # Make the API request to Crawlbase
    response = requests.get(API_ENDPOINT, params=params)
    
    # Raise an exception for bad HTTP status codes
    response.raise_for_status()

    # Return the JSON response as text
    return response.text

def save_to_csv(data, filename="data.csv"):
    try:
        # Extract products from the data
        products = data.get('body', {}).get('products', [])
        
        if not products:
            print("No products found in the data")
            return
        
        # Define the CSV columns based on the product structure
        fieldnames = [
            'name', 'rawPrice', 'currency', 'offer', 
            'customerReview', 'customerReviewCount', 'shippingMessage',
            'asin', 'image', 'url', 'isPrime', 'sponsoredAd', 'couponInfo'
        ]
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write each product (no header)
            for product in products:
                # Clean up the data for CSV (handle missing fields)
                cleaned_product = {}
                for field in fieldnames:
                    value = product.get(field, '')
                    # Convert boolean values to string
                    if isinstance(value, bool):
                        value = str(value)
                    # Handle list fields (like badgesInfo)
                    elif isinstance(value, list):
                        value = ', '.join(str(item) for item in value) if value else ''
                    cleaned_product[field] = value
                
                writer.writerow(cleaned_product)
        
        print(f"Successfully saved {len(products)} products to {filename}")
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    try:
        json_data = crawl_data("https://www.amazon.com/s?k=iPhone+16")
        parsed_json = json.loads(json_data)
        print(json.dumps(parsed_json, indent=2))
        
        # Save to CSV
        save_to_csv(parsed_json, "data.csv")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response:")
        print(crawl_data())
