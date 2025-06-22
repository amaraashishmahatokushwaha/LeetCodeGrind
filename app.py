from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from scripts.leetcode import fetch_leetcode_potd
from scripts.github_utils import push_to_github  # Changed from github to github_utils

app = Flask(__name__)

# Load environment variables
load_dotenv()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/potd", methods=["GET"])
def get_potd():
    problem_data = fetch_leetcode_potd()
    if problem_data:
        return jsonify(problem_data)
    return jsonify({"error": "Failed to fetch POTD"}), 500

@app.route("/add", methods=["POST"])
def add_problem():
    data = request.json
    problem_data = {
        "title": data["title"],
        "link": data["link"],
        "topics": [t.strip() for t in data["topics"].split(",")],
        "difficulty": data["difficulty"]
    }
    code = data["code"]
    explanation = data.get("explanation", "")
    
    # Push to GitHub
    push_to_github(problem_data, code, explanation)
    
    # Save to local JSON for revision tracking
    with open("problems.json", "a") as f:
        json.dump({
            "title": problem_data["title"],
            "date": datetime.now().isoformat(),
            "file": f"{problem_data['topics'][0].replace(' ', '-')}/{problem_data['title'].replace(' ', '-')}.md"
        }, f)
        f.write("\n")
    
    return jsonify({"message": f"Pushed {problem_data['title']} to GitHub!"})

if __name__ == "__main__":
    app.run(debug=True)