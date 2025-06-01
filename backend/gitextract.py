import os
import requests
import json
from dotenv import load_dotenv
from git import Repo

from constants import GITHUB_REPO 
from constants import  BRANCH_NAME
from constants import LOCAL_PATH
from constants import DATA_DIR 

# === Load API Keys from .env ===
load_dotenv()
GITHUB_TOKEN = os.getenv("GH_TOKEN")


# === STEP 1: Clone Specific Branch ===
def clone_specific_branch():
    if not os.path.exists(LOCAL_PATH):
        print("[INFO] Cloning branch...")
        Repo.clone_from(
            f"https://github.com/{GITHUB_REPO}.git",
            LOCAL_PATH,
            branch=BRANCH_NAME
        )
    else:
        print("[INFO] Repo already exists.")

# === STEP 2: Fetch GitHub Metadata and Save in Data/
def fetch_and_save_metadata():
    os.makedirs(DATA_DIR, exist_ok=True)  # <-- Create folder if not exists
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    base_url = f"https://api.github.com/repos/{GITHUB_REPO}"

    def fetch_and_save(endpoint, filename):
        url = f"{base_url}/{endpoint}"
        print(f"[INFO] Fetching {endpoint}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        filepath = os.path.join(DATA_DIR, f"{filename}.json")  # <-- Save in Data/
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data[:10], f, indent=2)
        print(f"[INFO] Saved {filepath}")

    fetch_and_save("issues", "github_issues")
    fetch_and_save("pulls", "github_pulls")
    fetch_and_save("contributors", "github_contributors")

# === MAIN ===
if __name__ == "__main__":
    clone_specific_branch()
    fetch_and_save_metadata()
