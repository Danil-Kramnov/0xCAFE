"""
Base class for coding platforms
Will add other platforms later
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BasePlatform(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__.replace('Platform', '')
    
    @abstractmethod
    def fetch_daily_challenge(self) -> Optional[Dict[str, Any]]:
        """Grab today's challenge"""
        pass
    
    @abstractmethod
    def fetch_challenge_by_id(self, challenge_id: str) -> Optional[Dict[str, Any]]:
        """Get specific problem"""
        pass
    
    @abstractmethod
    def format_challenge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to our standard format"""
        pass