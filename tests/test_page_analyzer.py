from page_analyzer.app import index


def test_page_analyzer():
    res = index()
    assert res == 'Hello World!'
