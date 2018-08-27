from flask import Flask, render_template, request, jsonify, url_for, redirect
from blockchain import *
import json

def UTXOdummy(to, value):
    jsonV = { "prev": "000x",
              "value": value,
              "owner": to
            }
    return json.dumps(jsonV);


app = Flask(__name__)

@app.route('/')
def index(arg = {}):
    print('call Index'),
    utxos = {}
    for name in names:
        utxos[name] = getUTXOs(name)
    print(utxos)
    return render_template('overview.html', result=utxos , arg = arg)

@app.route('/transfer')
def transfer():
    toWhom = request.args.get('receiver')
    money = request.args.get('value')
    print('ㅇㅇㅇㅇㅇ')
    print('거래:', toWhom, money)
    return redirect(url_for('index'))

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/hello')
def hello():
    output_json = "{'a':"+str(altCoin)+"}"
    print(output_json)
    return jsonify(output_json)

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def getUTXOs(name):
    list = []
    chain = altCoin.chain  # Blockchain['getChaina
    priv = sha256(name)
    pubk = privtopub(priv)
    addr = pubtoaddr(pubk)

    for block in chain:
        for tx in block.transactions:
            for elm in tx.inputs:
                list = [x for x in list if not (x['txhash'] == elm.hash and x['n'] == elm.n)]
            for idx, elm in enumerate(tx.outputs):
                if elm.to == addr:
                    dict0 = {}
                    dict0['to'] = elm.to
                    dict0['txhash'] = tx.hash
                    dict0['n'] = idx
                    dict0['value'] = elm.value
                    dict0['pubk'] = pubk
                    list.append(dict0)

    return list


@app.route('/getutxos')
def get(arg={}):
    a = {}
    for name in names:
        a[name] = getUTXOs(name)
    ## change redirect -> must check arg is valuable
    return index(arg)
    # return redirect(url_for('index', values=arg))

@app.route('/login')
def login():

    return

'''
result = {
    'alice': [
        {
            txhash = egaw2332tg3ga3t3
            n = 2
            value = 100
        },
        {

        },
    ],
    'bob' : [

    ]
}
'''


@app.route('/tx')
def tx():
    from_ = request.args.get('from')
    val = int(request.args.get('value'))
    to = request.args.get('to')

    list = getUTXOs(from_)
    result = {'tx':'fail','txout':'None'}


    todeletes = []

    for a in list:
        for b in altCoin.get_curr_block().transactions:
            for c in b.inputs:
                if c.hash==a['txhash'] and c.n==a['n']:
                    todeletes.append(a)

    for a in todeletes:
        list.remove(a)


    print("length of a : " +str(len(list)))

    sum = 0
    for idx, elm in enumerate(list):
        sum += elm['value']
        if sum >= val:
            list = list[:idx + 1]
            break;

    tx = Transaction()

    for elm in list:
        txin = TxIn()
        txin.address = elm['to']
        txin.value = elm['value']
        txin.n = elm['n']
        txin.hash = elm['txhash']
        txin.pubk = elm['pubk']

        tx.add_input(txin)

    txout = TxOut()
    txout.to = gen_address(to)[0]
    txout.value = val
    tx.add_output(txout)

    if sum > val:
        txout = TxOut()
        txout.to = gen_address(from_)[0]
        txout.value = sum - val
        tx.add_output(txout)
        result['tx'] = 'success'
    if sum == val:
        result['tx'] = 'success'

    if not tx.is_valid(gen_address(from_)[1]): result['tx'] = 'fail'
    tx.gen_hash()
    altCoin.get_curr_block().add_transaction(tx)
    result['txout'] = json.dumps(str(altCoin.get_curr_block().transactions))
    return get(result)

ismining = False
@app.route('/mine')
def is_mining():
    global ismining
    if ismining:
        return redirect('')
    else:
        ismining = True
        altCoin.add_block()
        ismining = False
        ## recall 은 redirect로 호출 : @app.route('/')
        return redirect('')

url = 'localhost'
# Windows
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


chrome = ChromeBrowser(chrome_path, url)
app.run(host=url, port=8080)