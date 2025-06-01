import requests

REPO = "microsoft/vscode-cosmosdb"
API_URL = f"https://api.github.com/repos/{REPO}/contributors"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    # Optional: Add your token for more requests
    # "Authorization": "token YOUR_GITHUB_TOKEN"
}

def fetch_contributors():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to fetch contributors:", response.json())
        return

    contributors = response.json()
    for contributor in contributors:
        print(f"👤 Username: {contributor['login']}")
        print(f"🖼️ Avatar URL: {contributor['avatar_url']}")
        print(f"🔗 Profile: {contributor['html_url']}")
        print("----")

fetch_contributors()