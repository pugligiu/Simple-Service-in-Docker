import time
import redis
import hashlib as hs
from flask import Flask, request, jsonify, abort


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cache = redis.Redis(host='redis', port=6379)


def save_message(sha, mess):
    retries = 5
    while True:
        try:
            cache.set(sha, mess)
            break
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def find_message(sha):
    retries = 5
    while True:
        try:
            return cache.get(sha)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/messages', methods=['POST'])
def set_message():
    j = request.json
    if(j and ('charset' not in request.mimetype_params or request.mimetype_params['charset'].lower()=='utf-8')):
        mess = j["message"]
        try:
            sha = hs.sha256(mess.encode('utf-8')).hexdigest()
            save_message(sha, mess)
        except:
            abort(500, {'err_msg': 'Server Error'})
        kv = {"digest": sha}
        return jsonify(kv)
    return abort(400, {'errors': {'err_msg': 'Bad Request'}})

@app.route('/messages/<sha>', methods=['GET'])
def get_message(sha):
    try:
        sha.encode('ascii')
    except Exception:
        abort(404)
    try:
        mess = find_message(sha)
    except:
        abort(500, {'err_msg': 'Server Error'})
    if(mess):
        kv = {"message": mess.decode('utf-8')}
        return jsonify(kv)
    else:
        abort(404)


@app.errorhandler(404)
def unauthorized(error):
    response = jsonify({'err_msg': 'Message not found'})
    response.status_code = 404
    return response

@app.errorhandler(500)
def unauthorized(error):
    response = jsonify({'err_msg': 'Server Error'})
    response.status_code = 500
    return response

@app.errorhandler(400)
def unauthorized(error):
    response = jsonify({'err_msg': 'Bad Request'})
    response.status_code = 400
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
