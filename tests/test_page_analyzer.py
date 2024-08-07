from page_analyzer import is_valid_url


def test_validator():
    assert is_valid_url("http://www.google.com")
    assert is_valid_url("http://www.yahoo.com")
    assert is_valid_url("http://facebook.com")
    assert not is_valid_url("http://111")


def test_page_analyzer(client):
    response = client.get('/')
    assert response.status_code == 200
