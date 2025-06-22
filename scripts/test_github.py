from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "amaraashishmahatokushwaha/LeetCodeGrind"

try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    print(f"Successfully connected to repo: {REPO_NAME}")
    print(f"Repo description: {repo.description or 'No description'}")
except Exception as e:
    print(f"Error connecting to repo: {e}")