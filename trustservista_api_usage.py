import requests
import json
import os

#graph, trustlevel
#json output


API_ENDPOINT_SEARCH = "https://app.trustservista.com/api/rest/v2/search"
API_ENDPOINT_TEXT = "https://app.trustservista.com/api/rest/v2/text"
API_ENDPOINT_GRAPH = "https://app.trustservista.com/api/rest/v2/graph"
API_ENDPOINT_TRUST = "https://app.trustservista.com/api/rest/v2/trustlevel"
API_KEY = "d4f388d353b44266aa075e2c5cd2b48b"  
HEADERS = {
    "X-TRUS-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}

def graph():
    data = {
        "content": "EMPTY",
        "contentUri": "https://www.zdg.md/stiri/a-fost-adoptata-o-declaratiei-comuna-privind-colaborarea-dintre-consiliile-superioare-ale-magistraturii-din-r-moldova-si-romania/",
        "language": "eng"
    }
    response = requests.post(API_ENDPOINT_GRAPH, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

print(graph())
    
def trust():
   
    data = {
        "content": "EMPTY",
        "contentUri": "https://www.zdg.md/stiri/a-fost-adoptata-o-declaratiei-comuna-privind-colaborarea-dintre-consiliile-superioare-ale-magistraturii-din-r-moldova-si-romania/",
        "language": "eng"
    }
    response = requests.post(API_ENDPOINT_TRUST, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

filename = f"data.json"

data = {
    "graph": graph(),
    "trust": trust()
}

filename = f"data.json"

with open(filename, 'w') as f:
    json.dump(data, f, indent=4)

print(trust())