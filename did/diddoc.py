'''example1:
{
  "@context": "https://www.w3.org/ns/did/v1",
  "id": "did:example:123456789abcdefghi",
  "controller": "did:example:bcehfew7h32f32h7af3",
}
'''
'''all content:
Property	Required?	Value constraints
id	        yes	A string that conforms to the rules in .
alsoKnownAs	no	A set of strings that conform to the rules of [[RFC3986]] for URIs.
controller	no	A string or a set of strings that conform to the rules in .
verificationMethod	no	A set of Verification Method maps that conform to the rules in .
authentication	no	A set of either Verification Method maps that conform to the rules in ) or strings that conform to the rules in .
assertionMethod	no
keyAgreement	no
capabilityInvocation	no
capabilityDelegation	no
service	                no	A set of Service Endpoint maps that conform to the rules in .
'''
'''Verification Method properties
Property	Required?	Value constraints
id	        yes	A string that conforms to the rules in .
controller	yes	A string that conforms to the rules in .
type	        yes	A string.
publicKeyJwk	no	A map representing a JSON Web Key that conforms to [[RFC7517]]. See definition of publicKeyJwk for additional constraints.
publicKeyMultibase	no	A string that conforms to a [[?MULTIBASE]] encoded public key.
'''
'''authentication:
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "id": "did:example:123456789abcdefghi",
  
  "authentication": [
    
    "did:example:123456789abcdefghi#keys-1",  
    
    {
      "id": "did:example:123456789abcdefghi#keys-2",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:example:123456789abcdefghi",
      "publicKeyMultibase": "zH3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    }
  ],
  
}
'''
# for all DIDs Document:
# arg DIDDoc is a DIDs Document.
def getDid(DIDDoc): # return did string
    return DIDDoc.get("id")

def getController(DIDDoc): # return controller string or set
    return DIDDoc.get("controller")

def getContext(DIDDoc): # return context string or set
    return DIDDoc.get("@context")

def getProperty(DIDDoc,propertyName): # arg propertyName is the name of the Property, return  Property string or set
    return DIDDoc.get(propertyName)

# for VerificationMethod Property:
def getVerificationMethodDid(DIDDoc): # return did set,error return None
    vlist = DIDDoc.get("verificationMethod")
    if vlist!=None:
        return [v.get("id") for v in vlist]
    else:
        return None
def getVerificationMethodController(DIDDoc): # return controller set,error return None
    vlist = DIDDoc.get("verificationMethod")
    if vlist!=None:
        return [v.get("controller") for v in vlist]
    else:
        return None

def getVerificationMethodType(DIDDoc): # return type set,error return None
    vlist = DIDDoc.get("verificationMethod")
    if vlist!=None:
        return [v.get("type") for v in vlist]
    else:
        return None

def getVerificationMethodPublicKeyMultibase(DIDDoc): # return publicKeyMultibase set,error return None
    vlist = DIDDoc.get("verificationMethod")
    if vlist!=None:
        return [v.get("publicKeyMultibase") for v in vlist]
    else:
        return None

# for authentication Property:
def getAuthenticationodDid(DIDDoc): # return authentication did string,error return None
    authlist = DIDDoc.get("authentication")
    if authlist!=None:
        return authlist[0]
    else:
        return None    
def getAuthenticationodType(DIDDoc): # return authentication type string,error return None
    authlist = DIDDoc.get("authentication")
    if authlist!=None:
        return authlist[1].get("type")
    else:
        return None     
def getAuthenticationodController(DIDDoc): # return authentication Controller string,error return None
    authlist = DIDDoc.get("authentication")
    if authlist!=None:
        return authlist[1].get("controller")
    else:
        return None      
def getAuthenticationodPublicKeyMultibase(DIDDoc): # return authentication publicKeyMultibase string,error return None
    authlist = DIDDoc.get("authentication")
    if authlist!=None:
        return authlist[1].get("publicKeyMultibase")
    else:
        return None   
