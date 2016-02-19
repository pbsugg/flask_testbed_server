import sys
import traceback
from cStringIO import StringIO
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def greet():
    return 'This is your initial greeting!'

@app.route("/", methods=['POST'])
def kernel():
    code_lns = request.form['code'].split('\\n')
    for line in code_lns: exec(line)
    return 'Success'

if __name__ == "__main__":
    app.run()
