import requests

LEETCODE_API = "https://leetcode.com/graphql"

def fetch_leetcode_potd():
    query = """
    {
      activeDailyCodingChallengeQuestion {
        date
        link
        question {
          title
          difficulty
          topicTags {
            name
          }
        }
      }
    }
    """
    try:
        response = requests.post(LEETCODE_API, json={"query": query}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            question = data["data"]["activeDailyCodingChallengeQuestion"]
            return {
                "title": question["question"]["title"],
                "link": f"https://leetcode.com{question['link']}",
                "topics": [tag["name"] for tag in question["question"]["topicTags"]],
                "difficulty": question["question"]["difficulty"]
            }
        return None
    except Exception as e:
        print(f"Error fetching POTD: {e}")
        return None