#!/usr/bin/env python
# encoding: utf-8

import hmac
import time
import base64
import urllib
import hashlib
import random

from flask import Flask, render_template, jsonify


def get_signarute(secret_id, secret_key, expire=3600*24):
    now = int(time.time())
    data = {
        'secretId': secret_id,
        'expireTime': now+expire,
        'currentTimeStamp': now,
        'random': random.randint(1, 1000000),
        'procedure': "QCVB_SimpleProcessFile(1,1,1,1)"
    }
    query_string = urllib.urlencode(data)
    sig_tmp = hmac.new(secret_key, query_string, hashlib.sha1)
    sign = base64.b64encode(sig_tmp.digest() + query_string).strip()
    return sign


app = Flask(__name__)


@app.after_request
def after_request(resp):
    resp.headers["Access-Control-Allow-Methods"] = "POST,GET"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sig')
def sig():
    secret_id = "xxxxx"
    secret_key = "xxxxx"
    return jsonify({
        'returnData': {'signature': get_signarute(secret_id, secret_key)},
        'returnMsg': 'return successfully!',
        'returnValue': 0
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8888)

