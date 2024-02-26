import os,hashlib
import base58 # import jws #  import ecdsa
from nacl.signing import SigningKey
from nacl.secret import SecretBox

class KeyStore():
    '''Use password create key:privateKey and ID'''
    #__privateKey
    #ID
    def  __init__(self,pwd=None):
        if pwd is None:
            pwd = "DID#MQTTcfm"
        load = self.loadKey(pwd)
        if not load:
            self.__privateKey = None
            self.ID = None
    def getKeyStore(self,pwd=None):
        if pwd is None:
            pwd = "DID#MQTTcfm"
        load = self.loadKey(pwd)
        if load:
            return load
        self.new(pwd)
        return True
    def new(self,pwd=None,bytesPrivateKey=None):        
        if bytesPrivateKey:
            privateKey = SigningKey(bytesPrivateKey) #重新创建私钥，第一个参数是我们要处理的hex
            self.__privateKey = privateKey
            vk = privateKey.verify_key  #verifying_key 在私钥的基础上生成公钥
            bsvk = bytes(vk)
            #self.__base58int = int.from_bytes(bsvk,'big')
            b58id = base58.b58encode(bsvk)
            self.ID =b58id.decode() #string base58 public key
        else:
            sk = SigningKey.generate() #最短的调用，然后再重新创建私钥
            bsk = bytes(sk)
            #b58bsk = base58.b58encode(bsk)
            #self.__base58bsk = b58bsk
            privateKey = SigningKey(bsk) #重新创建私钥，第一个参数是我们要处理的hex
            self.__privateKey = privateKey
            vk = privateKey.verify_key  #verifying_key 在私钥的基础上生成公钥
            bsvk = bytes(vk)
            #self.__base58int = int.from_bytes(bsvk,'big')
            b58id = base58.b58encode(bsvk)
            self.ID =b58id.decode() #string base58 public key
        if pwd is None:
            pwd = "DID#MQTTcfm"
        self.__saveKey(pwd)
    def __saveKey(self,pwd=None): #pwd is string
        #step 1:filename and pwd 
        if pwd is None:
            pwd = "DID#MQTTcfm"
        name = self.__md5hex(pwd)            
        filename = name+".dat"
        if os.path.exists("dids"):
            filename = os.path.join("dids",filename)
        elif os.path.exists("cfg"):
            filename = os.path.join("cfg",filename)
        #step 2 make pwd secret Object
        bpwd = self.__sha256(pwd)
        box = SecretBox(bpwd)  # box can decrypt and encrypt
        #step 3 make private key bytes
        bsk = bytes(self.__privateKey)
        #step 4
        ensk = box.encrypt(bsk)
        b58sk = base58.b58encode(ensk)
        str58sk = b58sk.decode()
        with open(filename,'wt') as f:
            f.write(str58sk)
        
    def loadKey(self,pwd=None):
        #step 1
        if pwd is None:
            pwd = "DID#MQTTcfm"
        name = self.__md5hex(pwd)
        filename = name+".dat"
        if os.path.exists("dids"):
            filename = os.path.join("dids",filename)
        elif os.path.exists("cfg"):
            filename = os.path.join("cfg",filename)
        if not os.path.exists(filename):
            return False
        #step 2
        str58sk = None
        with open(filename,'rt') as f:
            str58sk = f.read() # str58sk
        if  str58sk:
            if len(str58sk)>0:
                b58sk = str58sk.encode()
                ensk = base58.b58decode(b58sk)
                bpwd = self.__sha256(pwd)
                box = SecretBox(bpwd)
                bsk = box.decrypt(ensk)
                privateKey = SigningKey(bsk) #重新创建私钥，第一个参数是我们要处理的hex
                self.__privateKey = privateKey
                vk = privateKey.verify_key  #verifying_key 在私钥的基础上生成公钥
                bsvk = bytes(vk)
                b58id = base58.b58encode(bsvk)
                self.ID =b58id.decode() #string base58 public key
                return True
        return False
    def getBase58id(self): #return String
        return self.ID
    def getPublicKeyInt(self):
        if self.__privateKey:
            vk=self.__privateKey.verify_key
            bsvk = bytes(vk)         
            return int.from_bytes(bsvk,'big')
        else:
            return None
    def __getBase58PrivateKey(self): #->str
        if self.__privateKey:
            bsk = bytes(self.__privateKey)
            b58sk = base58.b58encode(bsk) #bytes base58 privateKey
            return b58sk.decode() #string base58 privateKey
        else:
            return None
        
    def verify(self,signature,msg):
        if self.__privateKey:
            pk=self.__privateKey.verify_key
            return pk.verify(signature,msg)
        else:
            return None
    
    def sign(self,msg):
        if self.__privateKey:
            return self.__privateKey.sign(smsg)
        else:
            return None
    def __md5hex(self,pwd):
        m5=hashlib.md5(b"Chen_Fu_Ming")
        m5.update(pwd.encode())
        return m5.hexdigest()
    def __sha256(self,pwd):                    
        h256=hashlib.sha256(b"Chen_Fu_Ming")
        h256.update(pwd.encode())
        return h256.digest()
        
if __name__ == "__main__":
    from did import DID
    from diddoc import Document
    did = DID()
    s = str(did)
    print("1:",s,did.getDID())
    did = DID("did:mqtt:123456789ABCDEF#key-1")
    s = str(did)
    print("2:",s,did.getDID())
    did = DID(DID={"ID":"123456789ABCDEF","Method":"mqtt"})
    s = str(did)
    print("3:",s,did.getDID())
    did = DID("did#key-1")
    s = str(did)
    print("4:",s,did.getDID())        
        
