import os
from dotenv import load_dotenv
from transformers import AutoTokenizer
from git import Repo

from constants import GITHUB_REPO 
from constants import  BRANCH_NAME
from constants import LOCAL_PATH



# === Load Environment Variables ===
load_dotenv()
GITHUB_TOKEN = os.getenv("GH_TOKEN")


# === Load HuggingFace Tokenizer (LLaMA 2 is a good approximation for LLaMA 4) ===
tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-hf")

# === Clone the Specific Branch of the GitHub Repo ===
def clone_specific_branch():
    if not os.path.exists(LOCAL_PATH):
        print("[INFO] Cloning branch...")
        Repo.clone_from(
            f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git",
            LOCAL_PATH,
            branch=BRANCH_NAME
        )
    else:
        print("[INFO] Repo already exists.")

# === Count Total Tokens from Code Files ===
def get_repo_token_count(repo_path: str, extensions=(".py", ".js", ".ts", ".md", ".json")) -> int:
    total_text = ""

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        total_text += f.read() + "\n"
                except Exception as e:
                    print(f"[WARN] Skipping {file_path}: {e}")

    tokens = tokenizer.encode(total_text, add_special_tokens=False)
    return len(tokens)

# === Main ===
if __name__ == "__main__":
    clone_specific_branch()
    token_count = get_repo_token_count(LOCAL_PATH)
    print(f"🔢 Total token count: {token_count}")
