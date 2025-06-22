from github import Github
import os
from dotenv import load_dotenv
from datetime import datetime
import github.GithubException

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "amaraashishmahatokushwaha/LeetCodeGrind"  # Your repo

# Initialize GitHub client
try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    print(f"Connected to repo: {REPO_NAME}")
except github.GithubException as e:
    print(f"Error initializing GitHub repo: {e}")
    raise

def create_markdown_content(problem_data, code, explanation=""):
    return f"""
# {problem_data['title']}
- **Link**: [{problem_data['title']}]({problem_data['link']})
- **Difficulty**: {problem_data['difficulty']}
- **Topics**: {', '.join(problem_data['topics'])}
- **Date**: {datetime.now().strftime('%Y-%m-%d')}

## Solution
```python
{code}
```

## Explanation
{explanation or "Add your explanation here"}
"""

def push_to_github(problem_data, code, explanation):
    primary_topic = problem_data["topics"][0].replace(" ", "-") if problem_data["topics"] else "Miscellaneous"
    folder = f"{primary_topic}"
    file_name = f"{folder}/{problem_data['title'].replace(' ', '-')}.md"
    content = create_markdown_content(problem_data, code, explanation)
    
    try:
        # Check if file exists
        repo.get_contents(file_name)
        repo.update_file(file_name, f"Update {problem_data['title']}", content, repo.get_contents(file_name).sha)
        print(f"Updated file: {file_name}")
    except github.GithubException as e:
        if e.status == 404:
            # Create file if it or folder doesn't exist
            try:
                repo.create_file(file_name, f"Add {problem_data['title']}", content)
                print(f"Created file: {file_name}")
            except Exception as e:
                print(f"Error creating file {file_name}: {e}")
                raise
        else:
            print(f"Error updating file {file_name}: {e}")
            raise