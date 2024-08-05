def test_page_analyzer(client):
    response = client.get('/')
    assert response.status_code == 200
