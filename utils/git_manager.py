"""
Git operations - commits and pushes
"""

from git import Repo
from pathlib import Path
from typing import Optional


class GitManager:
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.repo: Optional[Repo] = None
        self._init_repo()
    
    def _init_repo(self):
        """Get existing repo or create new one"""
        try:
            self.repo = Repo(self.repo_path)
        except:
            # not a git repo yet
            self.repo = Repo.init(self.repo_path)
            print("✅ Initialized git repo")
    
    def commit_challenge(self, file_paths: list, message: str) -> bool:
        """Commit files with message"""
        try:
            self.repo.index.add(file_paths)
            self.repo.index.commit(message)
            print(f"✅ {message}")
            return True
            
        except Exception as e:
            print(f"❌ Commit failed: {e}")
            return False
    
    def push_to_remote(self, remote_name: str = "origin", branch: str = "main") -> bool:
        """Push commits to github"""
        try:
            origin = self.repo.remote(name=remote_name)
            origin.push(branch)
            print(f"✅ Pushed to {remote_name}/{branch}")
            return True
        except Exception as e:
            print(f"❌ Push failed: {e}")
            print("   (might need to set up remote first)")
            return False