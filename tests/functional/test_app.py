
def test_home(client):
    response = client.get("/")
    assert b"<title>Home</title>" in response.data

