import os
import requests
import sys

BING_SEARCH_V7_SUBSCRIPTION_KEY = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY1']

def bing_search(query):
    headers = {
        'Ocp-Apim-Subscription-Key': BING_SEARCH_V7_SUBSCRIPTION_KEY,
    }
    params = {
        'q': query,
    }
    response = requests.get('https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    results = []
    for result in search_results['webPages']['value']:
        results.append({
            'title': result['name'],
            'url': result['url']
        })
    return results

if __name__ == '__main__':
    print(bing_search(sys.argv[1]))
