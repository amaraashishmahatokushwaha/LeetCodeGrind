import os
import github
from dotenv import load_dotenv
from datetime import datetime
from github import Github

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "amaraashishmahatokushwaha/LeetCodeGrind"

# Initialize GitHub client
try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    print(f"Connected to repo: {REPO_NAME}")
except github.GithubException as e:
    print(f"Error initializing GitHub repo: {e}")
    raise

def create_markdown_content(problem_data, code, explanation=""):
    """
    Creates a markdown string with problem details, code, and explanation.

    Args:
        problem_data (dict): Dictionary containing problem details (title, link, difficulty, topics).
        code (str): The solution code.
        explanation (str, optional): Explanation of the solution. Defaults to "".

    Returns:
        str: Formatted markdown content.
    """
    return (
        f"# {problem_data['title']}\n"
        f"- **Link**: [{problem_data['title']}]({problem_data['link']})\n"
        f"- **Difficulty**: {problem_data['difficulty']}\n"
        f"- **Topics**: {', '.join(problem_data['topics'])}\n"
        f"- **Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"## Solution\n"
        f"```python\n{code}\n```\n\n"
        f"## Explanation\n\n{explanation or 'Add your explanation here'}\n"
    )


def push_to_github(problem_data, code, explanation):
    """
    Pushes a problem solution to the GitHub repository in a topic-wise folder.

    Args:
        problem_data (dict): Dictionary containing problem details.
        code (str): The solution code.
        explanation (str): Explanation of the solution.

    Raises:
        github.GithubException: If there is an error interacting with the GitHub API.
    """
    primary_topic = (
        problem_data["topics"][0].replace(" ", "-")
        if problem_data["topics"]
        else "Miscellaneous"
    )
    folder = f"{primary_topic}"
    file_name = f"{folder}/{problem_data['title'].replace(' ', '-')}.md"
    content = create_markdown_content(problem_data, code, explanation)

    try:
        print(f"Attempting to check if file exists: {file_name}")
        repo.get_contents(file_name)
        print(f"File exists, updating: {file_name}")
        repo.update_file(
            file_name,
            f"Update {problem_data['title']}",
            content,
            repo.get_contents(file_name).sha,
        )
        print(f"Successfully updated file: {file_name}")
    except github.GithubException as e:
        if e.status == 404:
            print(f"File not found, creating new file: {file_name}")
            try:
                repo.create_file(
                    file_name, f"Add {problem_data['title']}", content
                )
                print(f"Successfully created file: {file_name}")
            except github.GithubException as create_error:
                print(f"Error creating file {file_name}: {create_error}")
                raise
        else:
            print(f"Error checking file {file_name}: {e}")
            raise