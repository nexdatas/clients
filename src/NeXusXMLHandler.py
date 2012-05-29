#!/usr/bin/env python
"""@package docstring
@file NexusXMLHandler.py
An example of SAX Nexus parser
"""
                                                                      
import pni.nx.h5 as nx

from numpy  import * 
from xml import sax

import sys,os
from H5Elements import *

from ThreadPool import *

# A map of NEXUS : pninx types 
mt={"NX_FLOAT32":"float32","NX_FLOAT64":"float64","NX_FLOAT":"float64","NX_NUMBER":"float64","NX_INT":"int64","NX_INT64":"int64","NX_INT32":"int32","NX_UINT64":"uint64","NX_UINT32":"uint32","NX_DATE_TIME":"string","NX_CHAR":"string","NX_BOOLEAN":"int32"}

# A map of tag attribute types 
dA={"signal":"NX_INT","axis":"NX_INT","primary":"NX_INT32","offset":"NX_INT","stride":"NX_INT","vector":"NX_FLOATVECTOR",
       "file_time":"NX_DATE_TIME","file_update_time":"NX_DATE_TIME","restricted":"NX_INT","ignoreExtraGroups":"NX_BOOLEAN",
    "ignoreExtraFields":"NX_BOOLEAN","ignoreExtraAttributes":"NX_BOOLEAN","minOccus":"NX_INT","maxOccus":"NX_INT"
    }


    
class NexusXMLHandler(sax.ContentHandler):
    """A SAX2 parser  """
    def __init__(self,fname):
        """ Constructor """
        sax.ContentHandler.__init__(self)
        ## A map of NXclass : name
        self.groupTypes={"":""}
        ## An H5 file name
        self.fname=fname
        self.nxFile=None
        ## A stack with open tag elements
        self.stack=[]
        self.tagOpenCmd={'group':self.createGroup, 'field':self.createField, 'attribute':self.addAttribute,
                         'link':self.createLink, 'doc':self.createDoc, 'definition':self.createDefinition, 
                         'symbols':self.createSymbols, 'symbol':self.createSymbol, 
                         'dimensions':self.createDimensions, 
                         'dim':self.createDim, 'enumeration':self.createEnumeration, 'item':self.createItem, 
                         'datasource':self.createDSource,'record':self.createRecord }

        self.tagCloseCmd={'field':self.storeFieldContent, 'attribute':self.storeAttributeContent, 
                          'doc':self.addDoc, 'symbol':self.addSymbol}

        self.symbols={}


        self.initPool=ThreadPool()
        self.stepPool=ThreadPool()
        self.finalPool=ThreadPool()

        self.poolMap={'INIT':self.initPool,'STEP':self.stepPool,'FINAL':self.finalPool}

        
    def nWS(text):
        """  cleans whitespaces  """
        return ' '.join(text.split())
        
    def lastObject(self):
        """  returns an object from the last stack elements """
        return self.stack[-1].fObject

    def last(self):
        """  returns the last stack elements """
        return self.stack[-1]

    def beforeLast(self):
        """  returns the last stack elements """
        return self.stack[-2]

    def typesToNames(self,text):
        """  converts NXclass types to names in a path string"""
        sp= text.split("/")
        print "TTN:", sp 
        res="/"
        for gr in sp[:-1]:
            sgr=gr.split(":")
            print sgr
            if len(sgr)>1 :
                res="/".join([res,sgr[1]])
            else:
                res="/".join([res,self.groupTypes[sgr[0]]])
        res=res+"/"+sp[-1]
        print "TTN:", res 

        return res

    def createDoc(self, name, attrs):
        self.stack.append(EDoc(name,attrs))

    def createSymbols(self, name, attrs):
        self.stack.append(Element(name,attrs))

    def createSymbol(self, name, attrs):
        self.stack.append(Element(name,attrs))

    def createEnumeration(self, name, attrs):
        self.stack.append(Element(name,attrs))

    def createItem(self, name, attrs):
        self.stack.append(Element(name,attrs))

    def createRecord(self, name, attrs):
        if "type" in attrs.keys():
            self.last().type=attrs["type"]
        if "name" in attrs.keys():
            self.last().type=attrs["name"]

        self.stack.append(Element(name,attrs))
        

    def createDSource(self, name, attrs):
        if "type" in attrs.keys():
            if attrs["type"] == "DB" :
                self.last().source=DBaseSource(name,attrs)
                if "dbname" in attrs.keys():
                    self.last().source.dbname=attrs["dbname"]
                if "query" in attrs.keys():
                    self.last().source.query=attrs["query"]
            elif attrs["type"] == "TANGO" :
                self.last().source=TangoSource(name,attrs)
                if "device" in attrs.keys():
                    self.last().source.device=attrs["device"]
            elif attrs["type"] == "CLIENT" :
                self.last().source=ClientSource(name,attrs)
            elif attrs["type"] == "SARDANA" :
                self.last().source=SardanaSource(name,attrs)
                if "door" in attrs.keys():
                    self.last().source.device=attrs["door"]
            else:
                print "Unknown data source"
                self.last().source=DataSource(name,attrs)
        else:
            print "Unknown data source"
            self.last().source=DataSource(name,attrs)
                    
            
        self.stack.append(self.last().source)


        if "strategy" in attrs.keys():
            self.last().strategy=attrs["strategy"]

        if "hostname" in attrs.keys():
            self.last().hostname=attrs["hostname"]

        if "port" in attrs.keys():
            self.last().port=attrs["port"]



        
    def addDoc(self,name):
        self.beforeLast().doc=self.beforeLast().doc + "".join(self.last().content)            
        print "Added doc\n", self.beforeLast().doc

    def addSymbol(self,name):
        if "name" in self.last().attrs.keys():
            self.symbols[self.last().attrs["name"]]=self.last().doc

    def createDimensions(self, name, attrs):
        if "rank" in attrs.keys():
            self.last().rank=attrs["rank"]
        self.stack.append(EDimensions(name,attrs))

    def createDim(self, name, attrs):
        if ("index"  in attrs.keys()) and  ("value"  in attrs.keys()) :
            self.beforeLast().lengths[attrs["index"]]=attrs["value"]
        self.stack.append(EDim(name,attrs))
        ## @todo add support for ref, refindex and incr 
       
    def createDefinition(self, name, attrs):
        self.nxFile=nx.create_file(self.fname,overwrite=True)
        ## A stack with open tag elements
        self.stack=[EFile(self.nxFile,"NXfile",attrs)]
        

    def createGroup(self, name, attrs):
        """  creates the group in the H5 file """
        if ("type" in attrs.keys()) and ("name" in attrs.keys()):
            g=self.lastObject().create_group(attrs["name"].encode(),attrs["type"].encode())
            self.groupTypes[attrs["type"]]=attrs["name"]
        elif "type" in attrs.keys():
            g=self.lastObject().create_group(attrs["type"][2:].encode(),attrs["type"].encode())
            self.groupTypes[attrs["type"]]=attrs["type"][2:]
        else:
            raise "The group type not defined !!!"
        self.stack.append(EGroup(g,name,attrs))
        for key in attrs.keys() :
            if key not in ["name","type"]:
                if key in dA.keys():
                    (self.lastObject().attr(key.encode(),mt[dA[key]].encode())).value=attrs[key].encode()
                else:
                    (self.lastObject().attr(key.encode(),"string")).value=attrs[key].encode()
            

    def createField(self, name, attrs):
        """  creates the field in the H5 file """
        if ("type" in attrs.keys()) and ("name" in attrs.keys()):
            print attrs["name"],    mt[attrs["type"]]
            f=self.lastObject().create_field(attrs["name"].encode(),mt[attrs["type"]].encode())
        elif "name" in attrs.keys():
            f=self.lastObject().create_field(attrs["name"].encode(),"string".encode())
        else:
            print "No name !!!"
        self.stack.append(EField(f,name,attrs))
        for key in attrs.keys():
            if key not in ["name"]:
                (self.lastObject().attr(key.encode(),"string")).value=attrs[key].encode()

    def createLink(self, name, attrs):
        """  creates the link in the H5 file """
        if ("name" in attrs.keys()) and ("target" in attrs.keys()):
            print "linking ",self.lastObject() ,attrs["name"].encode()
            l=(self.lastObject()).link((self.typesToNames(attrs["target"])).encode(),attrs["name"].encode())
            print self.typesToNames(attrs["target"])
        else:
            print "No name or type!!!"
            return
        self.stack.append(ELink(l,name,attrs))
        for key in attrs.keys():
            print "Attrs:", key.encode(), attrs[key].encode()


    def addAttribute(self,name,attrs):
        """  adds the Attribute in the H5 file """
        if "name" in attrs.keys():
            nm= attrs["name"]
            if "type" in attrs.keys():
                tp=attrs["type"]
            else:
                tp="NX_CHAR"
            at=self.lastObject().attr(nm.encode(),mt[tp].encode())
            self.stack.append(FElement(at,name,attrs))

            
    def characters(self, ch):
        """  adds the tag content """
        self.last().content.append(ch)

    def storeFieldContent(self,name):
        print "Storing field"
        if self.last().source and self.last().source.isValid() :
            strategy=self.last().source.strategy
            if strategy in self.poolMap.keys():
                self.poolMap[strategy].append(self.last())
        else:
            print "invalid dataSource"
        
    def storeAttributeContent(self,name):
        print "Storing Attributes:", "".join(self.last().content)
        if "name" in self.last().tAttrs.keys(): 
            if  self.last().tAttrs["name"] == "URL":
                self.last().fObject.value=("".join(self.last().content)).encode()
            elif "type" in self.last().tAttrs.keys():
                if self.last().tAttrs["type"]== "NX_CHAR":
                    self.last().fObject.value=("".join(self.last().content)).encode()
            else:        
                self.last().fObject.value=("".join(self.last().content)).encode()


    def startElement(self, name, attrs):
        """  parses an opening tag"""
        self.content=""
        if name in self.tagOpenCmd:
            print "Calling: ", name, attrs.keys()
            self.tagOpenCmd[name](name, attrs)
        else:
            print 'Unsupported tag:', name, attrs.keys()


    def endElement(self, name):
        """  parses an closing tag"""
        print 'End of element:', name , "last:" ,  self.last().tName
        if self.last().tName == name :
            if name in self.tagCloseCmd:
                print "Closing: ", name
                self.tagCloseCmd[name](name)
            print 'Content:' , "".join(self.last().content)    
            print "poping"
            self.stack.pop()

    def getNXFile(self):
        return self.nxFile            

    def closeFile(self):
        """  closes the H5 file """
        if self.nxFile:
            print "nxClosing"
            self.nxFile.close()


if __name__ == "__main__":

    if  len(sys.argv) <3:
        print "usage: simpleXMLtoh5.py  <XMLinput>  <h5output>"
        
    else:
        fi=sys.argv[1]
        if os.path.exists(fi):
            fo=sys.argv[2]

        # Create a parser object
            parser = sax.make_parser()
            
            handler = NexusXMLHandler(fo)
            parser.setContentHandler( handler )

            parser.parse(open(fi))
            handler.closeFile()
    