"""
Handles creating challenge folders and files
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class FileManager:
    
    def __init__(self, base_dir: str = "./challenges"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_challenge_directory(self, platform: str, date: str, title_slug: str) -> Path:
        """Create folder for challenge: challenges/leetcode/2025-01-06-two-sum/"""
        dir_path = self.base_dir / platform / f"{date}-{title_slug}"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def create_readme(self, challenge_dir: Path, challenge: Dict[str, Any]) -> Path:
        """Create README with problem description"""
        readme_path = challenge_dir / "README.md"
        
        # clean up html from description
        description = self._clean_html(challenge["description"])
        
        content = f"""# {challenge['title']}

**Difficulty:** {challenge['difficulty']}  
**Platform:** LeetCode  
**URL:** {challenge['url']}

## Topics
{', '.join(challenge['topics'])}

## Description

{description}

## Test Cases
```
{challenge['test_cases']}
```

## Progress
- Started: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- Status: In Progress
"""
        
        readme_path.write_text(content, encoding='utf-8')
        return readme_path
    
    def create_solution_file(self, challenge_dir: Path, challenge: Dict[str, Any]) -> Path:
        """Create solution.py with template"""
        solution_path = challenge_dir / "solution.py"
        
        content = f'''"""
{challenge['title']}
{challenge['url']}
"""

{challenge['code_template']}


def run_tests():
    """Test your solution here"""
    # TODO: add test cases
    pass


if __name__ == "__main__":
    run_tests()
'''
        
        solution_path.write_text(content, encoding='utf-8')
        return solution_path
    
    def _clean_html(self, html_content: str) -> str:
        """Basic html cleanup - removes tags but keeps structure"""
        import html
        
        # decode html entities
        text = html.unescape(html_content)
        
        # basic tag cleanup
        text = re.sub(r'<p>', '\n', text)
        text = re.sub(r'</p>', '\n', text)
        text = re.sub(r'<strong>', '**', text)
        text = re.sub(r'</strong>', '**', text)
        text = re.sub(r'<em>', '*', text)
        text = re.sub(r'</em>', '*', text)
        text = re.sub(r'<code>', '`', text)
        text = re.sub(r'</code>', '`', text)
        text = re.sub(r'<pre>', '\n```\n', text)
        text = re.sub(r'</pre>', '\n```\n', text)
        text = re.sub(r'<ul>', '\n', text)
        text = re.sub(r'</ul>', '\n', text)
        text = re.sub(r'<li>', '- ', text)
        text = re.sub(r'</li>', '\n', text)
        
        # remove remaining tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # cleanup whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()