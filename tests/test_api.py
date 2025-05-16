def test_get_messages_requires_login(client):
    res = client.get('/get_messages/testuser')
    assert res.status_code == 302  # redirect to login