"""
LeetCode API wrapper
Fetches problems via their graphql endpoint
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime
from .base import BasePlatform


class LeetCodePlatform(BasePlatform):
    
    API_URL = "https://leetcode.com/graphql"
    BASE_URL = "https://leetcode.com"
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        })
    
    def fetch_daily_challenge(self) -> Optional[Dict[str, Any]]:
        """Get today's daily problem"""
        
        # leetcode uses graphql, so we need this whole query
        query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    questionId
                    title
                    titleSlug
                    difficulty
                    content
                    topicTags {
                        name
                    }
                    codeSnippets {
                        lang
                        langSlug
                        code
                    }
                    sampleTestCase
                    exampleTestcases
                }
            }
        }
        """
        
        try:
            response = self.session.post(self.API_URL, json={"query": query})
            response.raise_for_status()
            data = response.json()
            
            # leetcode wraps everything in nested dicts
            if "data" in data and data["data"]["activeDailyCodingChallengeQuestion"]:
                return self.format_challenge(
                    data["data"]["activeDailyCodingChallengeQuestion"]
                )
            return None
            
        except Exception as e:
            print(f"Failed to fetch daily: {e}")
            return None
    
    def fetch_challenge_by_id(self, title_slug: str) -> Optional[Dict[str, Any]]:
        """Fetch specific problem by title slug (e.g., 'two-sum')"""
        
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                difficulty
                content
                topicTags {
                    name
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                sampleTestCase
                exampleTestcases
            }
        }
        """
        
        try:
            response = self.session.post(
                self.API_URL,
                json={
                    "query": query,
                    "variables": {"titleSlug": title_slug}
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if "data" in data and data["data"]["question"]:
                # fake the daily challenge format
                return self.format_challenge({
                    "question": data["data"]["question"],
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "link": f"/problems/{title_slug}/"
                })
            return None
            
        except Exception as e:
            print(f"Failed to fetch '{title_slug}': {e}")
            return None
    
    def format_challenge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert leetcode's format to our standard format"""
        question = data["question"]
        
        # find python3 code template
        python_snippet = ""
        for snippet in question.get("codeSnippets", []):
            if snippet["langSlug"] == "python3":
                python_snippet = snippet["code"]
                break
        
        return {
            "platform": "leetcode",
            "id": question["questionId"],
            "title": question["title"],
            "title_slug": question["titleSlug"],
            "difficulty": question["difficulty"],
            "url": f"{self.BASE_URL}{data['link']}",
            "date": data["date"],
            "description": question["content"],
            "topics": [tag["name"] for tag in question.get("topicTags", [])],
            "code_template": python_snippet,
            "test_cases": question.get("sampleTestCase", ""),
            "example_tests": question.get("exampleTestcases", "")
        }