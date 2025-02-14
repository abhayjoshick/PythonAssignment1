import requests
import time
import logging

logging.basicConfig(filename="uptime_monitor.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

URLS = [
    "http://www.example.com/nonexistentpage",
    "http://httpstat.us/404",
    "http://httpstat.us/500",
    "https://www.google.com/"
]

def checkStatus(url):
    try:
        response = requests.get(url, timeout=5)
        statusCode = response.status_code
        reason = response.reason
        
        print(f"Checking URL: {url}")
        print(f"Status Code: {statusCode} {reason}")
        
        if 400 <= statusCode < 500:
            print(f"ALERT: 4xx error encountered for URL: {url}")
            logging.warning(f"4xx error encountered: {url} - {statusCode} {reason}")
        elif 500 <= statusCode < 600:
            print(f"ALERT: 5xx error encountered for URL: {url}")
            logging.error(f"5xx error encountered: {url} - {statusCode} {reason}")
        else:
            print("The website is UP and running.")
            logging.info(f"Website OK: {url} - {statusCode} {reason}")
        
    except requests.RequestException as e:
        print(f"ERROR: Could not reach {url}. {e}")
        logging.error(f"Request failed: {url} - {e}")

def monitorUrls(interval=10, maxRetries=5):
    retry_intervals = {url: interval for url in URLS}  
    
    while True:
        for url in URLS:
            checkStatus(url)
        
            last_status = logging.getLogger().handlers[0].baseFilename
            if "4xx" in last_status or "5xx" in last_status:
                retry_intervals[url] = min(retry_intervals[url] * 2, interval * maxRetries)
            else:
                retry_intervals[url] = interval
            
            time.sleep(retry_intervals[url])
        
if __name__ == "__main__":
    monitorUrls()
