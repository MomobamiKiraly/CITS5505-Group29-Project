# Test to check if the home page loads successfully
def test_home_ok(client):
    res = client.get('/')
    assert res.status_code == 200         # Ensure the response status code is 200 (OK)
    assert b"F1" in res.data              # Check if "F1" appears in the response data