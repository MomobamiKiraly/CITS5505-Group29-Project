from app.models import User

def test_user_model_repr():
    user = User(username="testuser", email="test@example.com")
    assert "testuser" in repr(user)