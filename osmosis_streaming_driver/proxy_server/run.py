import websocket, multiprocessing, os, warnings
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask import Flask, Response, request
from flask_cors import cross_origin
from osmosis_streaming_driver.proxy_server.token_store import TokenStore

PROXY_SERVER_PORT = 3580 if 'PROXY_SERVER_PORT' not in os.environ else os.environ['PROXY_SERVER_PORT']
PROXY_SERVER_HOST = 'localhost'
if 'PROXY_SERVER_HOSTNAME' in os.environ:
    PROXY_SERVER_HOST = os.environ['PROXY_SERVER_HOSTNAME']
else:
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        PROXY_SERVER_HOST = s.getsockname()[0]
    except Exception as e:
        warnings.warn('Error while trying to obtain IP address of this host. %s' % str(e))

app = Flask(__name__)
store = TokenStore()


def _validate_stream_async(stream_url, q):
    try:
        ws = websocket.create_connection(stream_url)
        ws.close()
    except Exception as e:
        print(e)
        q.put((False, "Unable to connect to stream. Details: '%s'" % str(e)))
    else:
        q.put((True, ""))


def _validate_stream(stream_url, timeout_sec=5):
    q = multiprocessing.Queue()
    process = multiprocessing.Process(target=_validate_stream_async, args=(stream_url, q))
    process.start()
    process.join(timeout_sec)
    if process.is_alive():
        process.terminate()
        return False, "Timeout while trying to connect to '%s'" % stream_url
    success, err_message = q.get()
    return success, err_message


@app.route('/token')
def get_token():
    stream_url = request.args.get('stream_url', type=str)
    expires_at_str = request.args.get('expires_at', type=str)

    if stream_url is None:
        return "You need to provide the URL of your stream.", 400
    if expires_at_str is None:
        return "You need to provide the expiration date.", 400

    try:
        expires_at = parse(expires_at_str)
    except:
        return f'Expect ISO format expiring date, got {expires_at_str}', 400

    test_status, error_message = _validate_stream(stream_url)
    if not test_status:
        return error_message, 500

    return store.register(stream_url, expires_at)


@app.route('/proxy')
@cross_origin()
def proxy_wss():
    token = request.args.get('token', type=str)
    if token is None:
        return "You need to provide a valid token to start proxying.", 400
    stream_url, expiration = store.get_token_attributes(token)
    if stream_url is None:
        return "Token '%s' is invalid. Please provide a valid token." % str(token), 401

    ws = websocket.create_connection(stream_url)

    def generate(webs):
        while expiration > datetime.now():
            yield webs.recv()
        webs.close()
    return Response(generate(ws), mimetype='text/plain')


@app.route('/info')
def info():
    return store.dump(), 200


def start():
    app.run('0.0.0.0', port=PROXY_SERVER_PORT)


def get_test_client():
    return app.test_client()


if __name__ == '__main__':
    start()
