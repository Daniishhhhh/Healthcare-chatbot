from datetime import datetime, timedelta

from app.core.session_manager import SessionManager


def test_session_creation_and_language_setting():
    manager = SessionManager()

    session = manager.get_session("user-1")
    assert session["language"] is None
    assert session["onboarded"] is False

    manager.set_language("user-1", "hi")
    assert manager.get_language("user-1") == "hi"
    assert manager.is_onboarded("user-1") is True


def test_activity_and_emergency_tracking():
    manager = SessionManager()

    manager.update_activity("user-2")
    manager.update_activity("user-2")
    manager.mark_emergency("user-2")

    session = manager.get_session("user-2")
    assert session["total_queries"] == 2
    assert session["emergency_queries"] == 1


def test_conversation_history_retains_last_ten_entries():
    manager = SessionManager()

    for idx in range(12):
        manager.add_to_history("user-3", f"message {idx}", f"response {idx}")

    history = manager.get_session("user-3")["conversation_history"]
    assert len(history) == 10
    assert history[0]["user_message"] == "message 2"
    assert history[-1]["bot_response"] == "response 11"


def test_stats_and_cleanup_of_old_sessions():
    manager = SessionManager()

    manager.set_language("fresh-user", "en")
    manager.update_activity("fresh-user")

    stale_session = manager.get_session("stale-user")
    stale_session["language"] = "hi"
    stale_session["last_activity"] = datetime.now() - timedelta(days=10)

    stats_before = manager.get_stats()
    assert stats_before["total_sessions"] == 2
    assert stats_before["language_distribution"]["en"] == 1

    removed = manager.cleanup_old_sessions(days=7)
    assert removed == 1
    assert "stale-user" not in manager.sessions

    stats_after = manager.get_stats()
    assert stats_after["total_sessions"] == 1
    assert stats_after["most_popular_language"] == "en"
