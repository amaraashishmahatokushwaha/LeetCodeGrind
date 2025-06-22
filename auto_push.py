import time
from scripts.leetcode_scraper import fetch_recent_submission, get_problem_details
from scripts.github_utils import push_to_github
from datetime import datetime, timedelta
import json
import os

# Track last processed submission timestamp
LAST_SUBMISSION_FILE = "last_submission.json"

def load_last_submission():
    if os.path.exists(LAST_SUBMISSION_FILE):
        with open(LAST_SUBMISSION_FILE, "r") as f:
            return json.load(f).get("timestamp", 0)
    return 0

def save_last_submission(timestamp):
    with open(LAST_SUBMISSION_FILE, "w") as f:
        json.dump({"timestamp": timestamp}, f)

def auto_push():
    last_timestamp = load_last_submission()
    while True:
        print(f"Checking for new submissions at {datetime.now()}")
        submission = fetch_recent_submission()
        if submission and int(submission["timestamp"]) > last_timestamp:
            print(f"New submission found: {submission['title']}")
            title_slug = submission["link"].split("/problems/")[1].rstrip("/")
            problem_data = get_problem_details(title_slug)
            if problem_data:
                problem_data["link"] = submission["link"]
                push_to_github(problem_data, submission["code"], "")
                print(f"Pushed {submission['title']} to GitHub")
                save_last_submission(submission["timestamp"])
            else:
                print(f"Failed to fetch problem details for {submission['title']}")
        else:
            print("No new submissions")
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    auto_push()