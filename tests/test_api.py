def test_get_messages_requires_login(client):
    res = client.get('/get_messages/testuser')
    assert res.status_code == 302  # redirect to login
    
def test_chat_blocked_for_non_friend(client, app):
    import time
    from app.models import User, db

    timestamp = str(int(time.time()))
    email1 = f"a{timestamp}@test.com"
    email2 = f"b{timestamp}@test.com"

    with app.app_context():
        u1 = User(username="a" + timestamp, email=email1)
        u2 = User(username="b" + timestamp, email=email2)
        u1.set_password("123")
        u2.set_password("123")
        db.session.add_all([u1, u2])
        db.session.commit()
        u1_id = u1.id
        u2_username = u2.username

    # ✅ Simulate login for u1 (Flask-Login compatible)
    with client.session_transaction() as sess:
        sess['_user_id'] = str(u1_id)

    # Attempt to send a message to u2 (not mutual friend)
    res = client.post('/send_message', json={
        "receiver": u2_username,
        "message": "Hi!"
    })

    assert res.status_code == 403
    assert b"only chat with mutual friends" in res.data or b"can only chat" in res.data