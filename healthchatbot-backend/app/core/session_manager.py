# app/core/session_manager.py
"""
User Session Management
Handles user language preferences and conversation state
"""
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manage user sessions and preferences"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def get_session(self, user_id: str) -> Dict[str, Any]:
        """Get or create user session"""
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                "language": None,
                "onboarded": False,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "conversation_history": [],
                "preferences": {},
                "total_queries": 0,
                "emergency_queries": 0
            }
            logger.info(f"👤 Created new session for {user_id}")
        return self.sessions[user_id]
    
    def set_language(self, user_id: str, language: str):
        """Set user's preferred language"""
        session = self.get_session(user_id)
        session["language"] = language
        session["onboarded"] = True
        session["last_activity"] = datetime.now()
        logger.info(f"🌍 Language set to {language} for {user_id}")
    
    def get_language(self, user_id: str) -> Optional[str]:
        """Get user's preferred language"""
        return self.get_session(user_id).get("language")
    
    def is_onboarded(self, user_id: str) -> bool:
        """Check if user completed onboarding"""
        return self.get_session(user_id).get("onboarded", False)
    
    def update_activity(self, user_id: str):
        """Update last activity timestamp"""
        session = self.get_session(user_id)
        session["last_activity"] = datetime.now()
        session["total_queries"] = session.get("total_queries", 0) + 1
    
    def mark_emergency(self, user_id: str):
        """Mark that user had emergency query"""
        session = self.get_session(user_id)
        session["emergency_queries"] = session.get("emergency_queries", 0) + 1
        logger.warning(f"🚨 Emergency query recorded for {user_id}")
    
    def add_to_history(self, user_id: str, message: str, response: str):
        """Add conversation to history"""
        session = self.get_session(user_id)
        session["conversation_history"].append({
            "timestamp": datetime.now(),
            "user_message": message,
            "bot_response": response[:100] + "..." if len(response) > 100 else response
        })
        
        # Keep only last 10 conversations
        if len(session["conversation_history"]) > 10:
            session["conversation_history"] = session["conversation_history"][-10:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive session statistics"""
        total_sessions = len(self.sessions)
        active_sessions = sum(1 for s in self.sessions.values() if s.get("onboarded", False))
        
        language_stats = {}
        total_queries = 0
        emergency_queries = 0
        
        for session in self.sessions.values():
            lang = session.get("language", "unknown")
            language_stats[lang] = language_stats.get(lang, 0) + 1
            total_queries += session.get("total_queries", 0)
            emergency_queries += session.get("emergency_queries", 0)
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_queries": total_queries,
            "emergency_queries": emergency_queries,
            "language_distribution": language_stats,
            "most_popular_language": max(language_stats.items(), key=lambda x: x[1])[0] if language_stats else "none"
        }
    
    def cleanup_old_sessions(self, days: int = 7):
        """Cleanup sessions older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        old_sessions = [
            user_id for user_id, session in self.sessions.items()
            if session["last_activity"].timestamp() < cutoff_time
        ]
        
        for user_id in old_sessions:
            del self.sessions[user_id]
        
        logger.info(f"🧹 Cleaned up {len(old_sessions)} old sessions")
        return len(old_sessions)

# Global instance
session_manager = SessionManager()
