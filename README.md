LeetCode Sync Agent
A Python-based tool to automate syncing LeetCode problems with a GitHub repository. Fetches Problem of the Day (POTD) or custom problems and organizes them in topic-wise folders (e.g., /Binary-Search, /Dynamic-Programming).
Features

Fetch LeetCode POTD automatically.
Add custom problems via web UI.
Organize problems in topic-wise folders in GitHub repo.
Track problems locally for revision in problems.json.
Markdown files with problem link, code, and explanation.

Setup

Clone the repo:git clone https://github.com/username/LeetCode-AI-Agent.git
cd LeetCode-AI-Agent


Install dependencies:pip install flask requests PyGithub python-dotenv


Create .env file:GITHUB_TOKEN=your_personal_access_token


Create a GitHub repo (e.g., LeetCodeGrind) and update REPO_NAME in scripts/github.py.
Run the app:python app.py


Open http://localhost:5000 in your browser.

Usage

Fetch POTD: Click "Fetch POTD" to auto-fill the form with the daily problem.
Add Problem: Fill the form with problem details, your code, and optional explanation, then click "Add to GitHub".
Revision: Check problems.json for saved problems and their file paths.

Folder Structure

app.py: Main Flask app for web UI.
templates/index.html: Web UI for adding problems.
scripts/leetcode.py: Logic for fetching LeetCode problems.
scripts/github.py: Logic for pushing to GitHub.
problems.json: Local storage for problem tracking.
.env: Environment variables.
README.md: Project documentation.

Future Improvements

Add CLI support for command-line usage.
Scrape LeetCode submitted solutions.
Implement revision scheduler with reminders.
Support multiple programming languages.

License
MIT