#!/usr/bin/env python
# encoding: utf-8

import hmac
import time
import base64
import urllib
import hashlib
import random

from flask import Flask, render_template, jsonify


def get_signature(self, expire=600, auto_transcode=True,
                transcode_definition=1, watermark_definition=1,
                cover_by_snapshot_definition=10,
                sample_snapshot_definition=0):
    '''上传视频签名
    :param expire: 签名时效，单位秒
    :param auto_transcode: 上传视频后是否自动转码
    :param transcode_definition: 转码模板 id
    :param watermark_definition: 水印模板 id
    :param cover_by_snapshot_definition: 封面截图模板 id
    :param sample_snapshot_definition: 采样截图模板 id
    '''
    now = int(time.time())
    form_data = {
        'secretId': self.secret_id,
        'currentTimeStamp': now,
        'expireTime': now + expire,
        'random': random.randint(1, 1000000),
        # 默认转码模板，默认水印模板，默认封面图模板
    }
    if auto_transcode:
        form_data.update({
            'procedure': "QCVB_SimpleProcessFile({tscd}, {wtmk}, {cvst}, {spst})".format(
                tscd=transcode_definition, wtmk=watermark_definition,
                cvst=cover_by_snapshot_definition,
                spst=sample_snapshot_definition)
        })
    query_string = urllib.urlencode(form_data)
    sig_tmp = hmac.new(self.secret_key, query_string, hashlib.sha1)
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

