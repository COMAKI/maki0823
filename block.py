import time
import hashlib
import json
import copy

class Block:
    def __init__(self, index, prev_hash=None):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.mrkl_root = None
        self.bits = 3
        self.nonce = 0
        self.hash = None
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def gen_mrkl_root(self):
        pass
        # tx_prev, tx_next = ''
        # mrkl_nodes = copy.deepcopy(self.transactions)
        # while len(mrkl_nodes) > 1:
        #     mrkl_branch = []
        #     if txi == 0 :
        #         tx_prev = transaction.hash
        #         continue
        #     tx_next = transaction.hash
        #     if txi%2 == 0 and txi != 0:
        #         mrkl_branch.append(hashlib.sha256(str(tx_prev)+str(tx_next)).hexdigest())


    def gen_hash(self):
        while True:
            h = hashlib.sha256(str(self).encode()).hexdigest()
            self.nonce +=1
            if h[:self.bits] == '0' * self.bits:
                self.hash = h
                break

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

if __name__=='__main__':
    b = Block(0)
    # print(b)
    b.bits = 4
    itime = time.time()
    b.gen_hash()
    print(b)
    ftime = time.time()
    print(ftime-itime)
