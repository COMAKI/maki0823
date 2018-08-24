from bitcoin import *

priv = sha256('turing')
pubk = privtopub(priv)
addr = pubtoaddr(pubk)
print(addr)

sign_of_msg = ecdsa_sign('json str of transaction', priv)
print(sign_of_msg)

result = ecdsa_verify('json str of transaction',sign_of_msg, pubk)
print(result)