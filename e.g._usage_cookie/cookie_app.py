from bottle import run, get, redirect, response

@get('/')
def get_root():
    response.set_cookie('root', 'foo')
    return 'Hello world'

@get('/redirect')
def get_redirect():
    response.set_cookie('redirect', 'bar')
    redirect('/')

if __name__ == "__main__":
    run(host='localhost', debug=True, reloader=True)