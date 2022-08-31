'''
## Copy from http://github.com/build-trust/did/blob/main/did.go
// DID Method
// https://w3c.github.io/did-core/#method-specific-syntax
Method string

// The method-specific-id component of a DID
// method-specific-id = *idchar *( ":" *idchar )
ID string

// method-specific-id may be composed of multiple `:` separated idstrings
IDStrings []string

// DID URL
// did-url = did *( ";" param ) path-abempty [ "?" query ] [ "#" fragment ]
// did-url may contain multiple params, a path, query, and fragment
Params []Param

// DID Path, the portion of a DID reference that follows the first forward slash character.
// https://w3c.github.io/did-core/#path
Path string

// Path may be composed of multiple `/` separated segments
// path-abempty  = *( "/" segment )
PathSegments []string

// DID Query
// https://w3c.github.io/did-core/#query
// query = *( pchar / "/" / "?" )
Query string

// DID Fragment, the portion of a DID reference that follows the first hash sign character ("#")
// https://w3c.github.io/did-core/#fragment
Fragment string
'''
#DID={}

'''parse
input        string // input to the parser
currentIndex int    // index in the input which the parser is currently processing
out          *DID   // the output DID that the parser will assemble as it steps through its state machine
err          error  // an error in the parser state machine
'''
def IsURL(did): #did is a dict.
    return len(did)>0 and ( did.get("Method")!=None or  did.get("ID") !=None or  did.get("Params") !=None or did.get("Path") !=None)
def String(did): # did is a dict. return (String,error), String is did's string. if return (None,String) ,then String is error.
    buf ="did:"
    if did.get("Method") !=None:
        buf += did.get("Method")
    else:
        return None,"No method"
    if did.get("ID") !=None:
        buf += ":" + did.get("ID")
    elif did.get("IDStrings") !=None:
        if len(IDStrings)>0:
            buf += ":"+":".join(did.get("IDStrings"))
    else:
        return None,"No ID"
    if did.get("Params") !=None:
        if len(did.get("Params"))>0:
            for pa in did.get("Params"):
                buf += ";"+ pa
    if did.get("Path") !=None:
        buf +=  "/"+did.get("Path")
    elif did.get("PathSegments") !=None:
        if len(did.get("PathSegments"))>0:
            for ps in did.get("PathSegments"):
                buf += ";"+ ps
    if did.get("Query") !=None:
        buf += "?" + did.get("Query")
    if did.get("Fragment") !=None:
        buf += "#" + did.get("Fragment")
    return buf,None
    
def Parse(inpt ): # string inpt  ,return  DID,error,DID is dict,error is None then no error.
    if inpt is None:
        return None,"did string is None"
    DID={}
    error = None
    if len(inpt)<= 0 :
        return DID,"did string is empty"
    seg = inpt.split(":")
    if len(seg)< 3:
        error = "did string is error"
        if len(seg)== 2:
            DID["Method"]=seg[1]
            return DID,error
        else:
            return DID,error
    else:
        DID["Method"]=seg[1]
        idPathQuery = None
        idPath = None
        idParams = None
        # Step 1 get Fragment
        idFrag = seg[-1].split("#")  # 2 is error, for many ID:ID
        if len(idFrag)==2:
            idPathQuery = idFrag[0]
            DID["Fragment"] = idFrag[1]
        else:
            idPathQuery = seg[2]
        
        # Step 2 get Query
        idQuery = idPathQuery.split("?")
        if len(idQuery)==2:
            idPath = idQuery[0]
            DID["Query"] = idQuery[1]
        else:
            idPath = idPathQuery

        # Step 3 get Path
        idpath = idPath.split("/")
        if len(idpath)>=2:
            idParams  = idpath[0]
            DID["PathSegments"] = idpath[1:]
            DID["Path"] = "/".join(idpath[1:])            
        else:
            idParams = idPath
            
        # Step 4 get Params
        idpra = idParams.split(";")
        if len(idpra)>=2:
            if len(seg)== 3:
                DID["ID"]  = idpra[0]
            else: # >3                
                ids  = [idpra[0]]
                DID["IDStrings"]=ids.extend(seg[2:-1])
            DID["Params"] = idpra[1:]            
        else:
            print("len:",len(seg))
            if len(seg) == 3:
                DID["ID"]  = idpra[0]
            else: # >3                
                ids  = [idpra[0]]
                ids.extend(seg[2:-1])
                DID["IDStrings"]= ids.copy()
        #print(DID)    
        return DID,error

def ParseID(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        if DID.get("IDStrings")!= None:
            return DID.get("IDStrings")
        else:
           return DID.get("ID") 
def ParseMethod(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        return DID.get("Method")
def ParsePath(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        return DID.get("Path")
def ParseQuery(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        return DID.get("Query")

def ParseFragment(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        return DID.get("Fragment")
    
def ParseParams(inpt ):
    DID,error = Parse(inpt )
    if DID is None:
        return None
    else:
        return DID.get("Params")              
