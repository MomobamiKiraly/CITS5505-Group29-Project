# Test to check if the home page loads successfully
def test_home_ok(client):
    res = client.get('/')
    assert res.status_code == 200         # Ensure the response status code is 200 (OK)
    assert b"F1" in res.data              # Check if "F1" appears in the response data
    
def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data  # Check if the response contains 'Login' indicating a redirect to the login page