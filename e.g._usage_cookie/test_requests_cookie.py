import requests
import pytest

class TestCookieUsingRequest(object):
    def test_get(self):
        response = requests.get('http://localhost:8080')
        assert response.status_code == 200
        assert response.cookies.get('root') == 'foo'

    @pytest.mark.xfail
    def test_allow_redirect(self):
        response = requests.get('http://localhost:8080/redirect')
        assert response.status_code == 200
        assert response.cookies.get('root') == 'foo'
        # ここで失敗する
        assert response.cookies.get('redirect') == 'bar'
        #=> AssertionError: assert None == 'bar'

    def test_forbid_redirect(self):
        response = requests.get('http://localhost:8080/redirect', allow_redirects=False)
        assert response.status_code == 303
        assert response.cookies.get('root') is None
        assert response.cookies.get('redirect') == 'bar'


class TestCookieUsingSessionObject(object):
    def test_get(self):
        session = requests.Session()
        response = session.get('http://localhost:8080')
        assert response.status_code == 200
        # responseとsessionの両方にCookieがセットされる
        assert response.cookies.get('root') == 'foo'
        assert session.cookies.get('root') == 'foo'

    def test_allow_redirect(self):
        session = requests.Session()
        response = session.get('http://localhost:8080/redirect')
        assert response.status_code == 200
        # Cookie「redirect」はsessionのみセットされる
        assert response.cookies.get('root') == 'foo'
        assert response.cookies.get('redirect') is None
        assert session.cookies.get('root') == 'foo'
        assert session.cookies.get('redirect') == 'bar'

    def test_forbid_redirect(self):
        session = requests.Session()
        response = session.get('http://localhost:8080/redirect', allow_redirects=False)
        assert response.status_code == 303
        # responseとsessionの両方にCookieがセットされる
        assert response.cookies.get('root') is None
        assert response.cookies.get('redirect') == 'bar'
        assert session.cookies.get('root') is None
        assert session.cookies.get('redirect') == 'bar'