from app.models import User

# Test to check the __repr__ method of the User model
def test_user_model_repr():
    user = User(username="testuser", email="test@example.com")
    assert "testuser" in repr(user)  # Ensure the username appears in the string representation