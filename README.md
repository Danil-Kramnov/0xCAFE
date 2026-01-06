# 0xCAFE

**Code before coffee.** A CLI tool to fetch, track, and manage daily LeetCode challenges.

## Features

- Auto-fetch daily LeetCode challenges
- Organized directory structure with problem descriptions and solution templates
- Local test runner
- Git integration with automatic commits
- Progress tracking and statistics
- Browser integration for LeetCode submissions

## Installation

```bash
# Clone and setup
git clone https://github.com/Danil-Kramnov/0xCAFE.git
cd 0xCAFE

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml`:

```yaml
user:
  name: "Your Name"
  github_username: "your-username"

leetcode:
  enabled: true
  difficulty: ["Easy", "Medium", "Hard"]

git:
  auto_commit: true

paths:
  challenges_dir: "./challenges"
```

## Commands

```bash
# Fetch today's daily challenge
python main.py fetch

# Fetch a specific problem
python main.py get <problem-slug>

# Open challenge in browser
python main.py browse <challenge-path>

# Test your solution
python main.py test <challenge-path>

# Mark as solved and commit
python main.py solve <challenge-path> [--push]

# View statistics
python main.py status
```
