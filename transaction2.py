import hashlib, json
from bitcoin import *
class TxIn():
    def __init__(self):
        self.hash = None # 사용할 UTXO가 포함된 해시
        self.n = 0 # 위 트랙잰션 중에서 몇 번째 UTXO인지
        self.address = '' # UTXO의 수신주소
        self.value = '' # UTXO의 잔액
        self.sign = '' # 서명
        self.pubk = '' # 사용자의 공개키

    def __str__(self):
        return str(self.__dict__)

    def get_prev_sign(self):
        return hashlib.sha256(self.get_string(self.hash, self.n, self.address, self.value, self.pubk).encode()).hexdigest()

    def get_string(self,*args):
        if(len(args)<1): return
        to_str = ''
        for i in args:
            to_str += str(i)
        return to_str
    __repr__ = __str__

class TxOut():
    def __init__(self):
        self.to = '' # 받는 주소
        self.value = '' # 금액

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

class Transaction():
    def __init__(self):
        self.vin_sz = 0
        self.vout_sz = 0
        self.inputs = []
        self.outputs = []
        self.hash = None

    def can_spent(self):
        for input in self.inputs:
            pass

    def add_input(self,txin):
        self.inputs.append(txin)

    def add_output(self,txout):
        self.outputs.append(txout)

    def gen_hash(self):
        h = hashlib.sha256(str(str(self)+str(time.time())).encode()).hexdigest()
        self.hash = h

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

    def is_valid(self,priv):
        for txin in self.inputs:
            txin.sign = ecdsa_sign(str(txin.get_prev_sign()), priv)
            result = ecdsa_verify(str(txin.get_prev_sign()), txin.sign, txin.pubk)
            print('is_valid:',result)
            if result != True:
                return result
        return True

if __name__ == '__main__':
    pass
