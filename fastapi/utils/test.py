from bs4 import BeautifulSoup
import requests

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.cse.com.bd",
    "Referer": "https://www.cse.com.bd/",
}


# Step 1: Load homepage to get a fresh CSRF token
home_url = "https://www.cse.com.bd/"
html = session.get(home_url).text
soup = BeautifulSoup(html, "html.parser")

csrf_token = soup.find("input", {"name": "csrf_cse_token"})["value"]
print("CSRF Token:", csrf_token)

# Step 2: Use it for the POST request
post_url = "https://www.cse.com.bd/home/graph_load/"
data = {"selected_index": "CSE30", "csrf_cse_token": csrf_token}

resp = session.post(post_url, headers=headers, data=data)
print(resp.text)