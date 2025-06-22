import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
LEETCODE_API = "https://leetcode.com/graphql"

def fetch_recent_submission(username="amarnath098"):
    query = """
    query recentSubmissions($username: String!) {
      recentSubmissionList(username: $username, limit: 1) {
        title
        titleSlug
        timestamp
        statusDisplay
        lang
        code
      }
    }
    """
    headers = {
        "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "variables": {"username": username},
    }
    try:
        response = requests.post(LEETCODE_API, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            submissions = data["data"]["recentSubmissionList"]
            if submissions:
                submission = submissions[0]
                if submission["statusDisplay"] == "Accepted":
                    return {
                        "title": submission["title"],
                        "link": f"https://leetcode.com/problems/{submission['titleSlug']}",
                        "code": submission["code"],
                        "lang": submission["lang"],
                        "timestamp": submission["timestamp"],
                    }
        return None
    except Exception as e:
        print(f"Error fetching submission: {e}")
        return None

def get_problem_details(title_slug):
    query = """
    query problemDetails($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        difficulty
        topicTags { name }
      }
    }
    """
    headers = {
        "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
    }
    try:
        response = requests.post(LEETCODE_API, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            question = data["data"]["question"]
            return {
                "title": question["title"],
                "difficulty": question["difficulty"],
                "topics": [tag["name"] for tag in question["topicTags"]],
            }
        return None
    except Exception as e:
        print(f"Error fetching problem details: {e}")
        return None
