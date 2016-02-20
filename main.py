import sys
import traceback
from cStringIO import StringIO
from flask import Flask, jsonify, request

app = Flask(__name__)


environments = {}

@app.route('/env/create', methods=['POST'])
def create():
    env_id = request.form['id']
    if env_id not in environments:
        environments[env_id] = {}
    return jsonify(envs=environments.keys())

@app.route('/env/delete', methods=['POST'])
def delete():
    env_id = request.form['id']
    if env_id in environments:
        del environments[env_id]
    return jsonify(envs=environments.keys())

@app.route('/env/get', methods=['POST'])
def getenv():
    env_id = request.form['id']
    if env_id in environments:
        return jsonfy(env=environments[env_id].keys())
    else:
        return jsonify(error='Environment does not exist!')


@app.route("/", methods=['GET'])
def greet():
    return 'This is your initial greeting!'

@app.route("/", methods=['POST'])
def kernel():
    env_id = request.form['id']
    if env_id not in environments:
        return jsonify(error='Environment does not exist!')
    code_lns = request.form['code'].split('\\n')
    #store stdout location
    old_stdout = sys.stdout
    #redirect stdout to string buffer
    sys.stdout = strstdout = StringIO()
    for line in code_lns:
        try:
            code = compile(line, '<string>', 'exec')
            exec code in environments[env_id]
        except:
            print(traceback.format_exc())
            error = True
    sys.stdout = old_stdout
    if error: return jsonify(error=strstdout.getvalue())
    else: return jsonify(message=strstdout.getvalue())


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
