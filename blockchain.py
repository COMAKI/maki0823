from bitcoin import *
from transaction2 import *
from block import Block
from flask import Flask, render_template, request, jsonify, Response
import webbrowser
import json

names = ['alice','bob','charlie','dominic']

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def gen_address(string):
    priv = sha256(string)
    pubk = privtopub(priv)
    addr = pubtoaddr(pubk)
    return addr, priv

class Blockchain():
    def __init__(self):
        self.chain = []
        self.genesis_block = Block(0)
        self.genesis_block.bits = 4 # 초기 난이도
        self.curr_reward = 50

        self.curr_block = self.genesis_block
        self.add_block()

        self.curr_block = Block(len(self.chain))

    def get_latest_block(self):
        if len(self.chain) == 0:
            return Block('-1')
        return self.chain[len(self.chain)-1]

    def get_curr_block(self):
        return self.curr_block

    def add_block(self):
        self.curr_block.prev_hash = self.get_latest_block().hash
        tx = Transaction()
        txout = TxOut()
        ## change miner : alice -> random
        tId = random.randint(0,len(names));
        print("miner is ", names[tId]);
        txout.to = gen_address(names[tId])[0]
        txout.value = self.curr_reward

        tx.add_output(txout)
        print("rewarding miner : " , txout)
        tx.gen_hash()
        self.curr_block.transactions.insert(0,tx)
        self.curr_block.gen_hash()

        print(" tx : ", tx)

        self.chain.append(self.curr_block)
        self.curr_block = Block(len(self.chain))

    def __str__(self):
        return str(self.chain)

class ChromeBrowser():
    def __init__(self, chrome_path, url):
        self.chrome_path = chrome_path
        self.url = url
        self.chrome = webbrowser.get(self.chrome_path)
        self.chrome.open(self.url)
    def __del__(self):
        shutdown_server()

altCoin = Blockchain()
idx = 1



