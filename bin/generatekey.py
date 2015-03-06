import rsa
import sys
import os

path = sys.path[0]
try:
    os.remove(path + "/../client/public.pem")
    os.remove(path + "/../key/private.pem")
except Exception, e:
    pass
finally:
    print("remove old key files")

(pubkey, privkey) = rsa.newkeys(1024)

pub = pubkey.save_pkcs1()
pubfile = open(path + "/../client/public.pem", "w+")
pubfile.write(pub)
pubfile.close()


priv = privkey.save_pkcs1()
privfile = open(path + "/../key/private.pem", "w+")
privfile.write(priv)
privfile.close()

