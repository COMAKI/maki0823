from flask import Flask, render_template, request, jsonify, url_for, redirect
import json;

def UTXOdummy(to, value):
    jsonV = { "prev": "000x",
              "value": value,
              "owner": to
            }
    return json.dumps(jsonV);


app = Flask(__name__)

@app.route('/')
def index():
    print('call Index')
    dum1 = json.loads(UTXOdummy('bob', 100));
    dum2 = json.loads(UTXOdummy('alice', 50));

    return render_template('overview.html', utxo=[dum1, dum2])

@app.route('/transfer')
def transfer():
    toWhom = request.args.get('receiver')
    money = request.args.get('value')
    print('ㅇㅇㅇㅇㅇ')
    print('거래:', toWhom, money)
    return redirect(url_for('index'))

app.run(host='127.0.0.1', port=88)