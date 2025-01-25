
import requests
import json
import os
from datetime import datetime

API_KEY = "d4f388d353b44266aa075e2c5cd2b48b"
HEADERS = {
    "X-TRUS-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}

API_ENDPOINT_GRAPH = "https://app.trustservista.com/api/rest/v2/graph"
API_ENDPOINT_TRUST = "https://app.trustservista.com/api/rest/v2/trustlevel"


def analyze():
    user_url = 'https://www.bbc.com/news/articles/cdd9zpj13q9o'

    api_data = {
        "content": "EMPTY",
        "contentUri": user_url,
        "language": "eng"
    }

  
    graph_response = requests.post(API_ENDPOINT_GRAPH, headers=HEADERS, data=json.dumps(api_data))
    trust_response = requests.post(API_ENDPOINT_TRUST, headers=HEADERS, data=json.dumps(api_data))

    results = {
        "timestamp": datetime.now().isoformat(),
        "url": user_url,
        "graph": graph_response.json() if graph_response.status_code == 200 else {"error": graph_response.text},
        "trust": trust_response.json() if trust_response.status_code == 200 else {"error": trust_response.text}
    }

    print(results)
   
    filename = f"data.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

  
    

if __name__ == '__main__':
    analyze()