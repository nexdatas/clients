#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2013 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \package test nexdatas
## \file DataSourceTest.py
# unittests for field Tags running Tango Server
#
import unittest
import os
import sys
import subprocess
import random
import struct
import numpy
from xml.dom import minidom


from ndts.DataSources import DataSource
from ndts.DataSources import PYTANGO_AVAILABLE as PYTANGO
from ndts.DataSources import DB_AVAILABLE as DB



try:
    import PyTango
    ## global variable if PyTango module installed
    PYTANGO_AVAILABLE = True
except ImportError, e:
    PYTANGO_AVAILABLE = False
    print "PYTANGO not available: %s" % e


## list of available databases
DB_AVAILABLE = []

try:
    import MySQLdb
    DB_AVAILABLE.append("MYSQL")
except ImportError, e:
    print "MYSQL not available: %s" % e
    
try:
    import psycopg2
    DB_AVAILABLE.append("PGSQL")
except ImportError, e:
    print "PGSQL not available: %s" % e

try:
    import cx_Oracle
    DB_AVAILABLE.append("ORACLE")
except ImportError, e:
    print "ORACLE not available: %s" % e

## if 64-bit machione
IS64BIT = (struct.calcsize("P") == 8)


## test fixture
class DataSourceTest(unittest.TestCase):

    ## constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

        self._tfname = "doc"
        self._fname = "test.h5"
        self._nxDoc = None
        self._eDoc = None        
        self._fattrs = {"short_name":"test","units":"m" }
        self._gname = "testDoc"
        self._gtype = "NXentry"


        self._bint = "int64" if IS64BIT else "int32"
        self._buint = "uint64" if IS64BIT else "uint32"
        self._bfloat = "float64" if IS64BIT else "float32"

        


    ## test starter
    # \brief Common set up
    def setUp(self):
        ## file handle
        print "\nsetting up..."        

    ## test closer
    # \brief Common tear down
    def tearDown(self):
        print "tearing down ..."

    ## Exception tester
    # \param exception expected exception
    # \param method called method      
    # \param args list with method arguments
    # \param kwargs dictionary with method arguments
    def myAssertRaise(self, exception, method, *args, **kwargs):
        try:
            error =  False
            method(*args, **kwargs)
        except exception, e:
            error = True
        self.assertEqual(error, True)

    ## constructor test
    # \brief It tests default settings
    def test_constructor_default(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.assertEqual(PYTANGO_AVAILABLE,PYTANGO)
        self.assertEqual(len(DB),len(DB_AVAILABLE))
        for db in range(len(DB)):
            self.assertEqual(DB[db],DB_AVAILABLE[db])
            



    ## setup test
    # \brief It tests default settings
    def test_setup(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.assertEqual(el.setup("<tag/>"), None)


    ## getData test
    # \brief It tests default settings
    def test_getData(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.assertEqual(el.getData(), None)


    ## isValid test
    # \brief It tests default settings
    def test_isValid(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.assertEqual(el.isValid(), True)



    ## __str__ test
    # \brief It tests default settings
    def test_str(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.assertEqual(el.__str__(), "unknown DataSource")


    ## getText test
    # \brief It tests default settings
    def test_getText_default(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)


        el = DataSource()
        self.assertTrue(isinstance(el, object))
        self.myAssertRaise(AttributeError,el._getText, None) 

        dom = minidom.parseString("<tag/>")
        node = dom.getElementsByTagName("tag")
        self.assertEqual(el._getText(node[0]).strip(),'') 

        text = "My test \n text"
        dom = minidom.parseString("<tag> %s</tag>" % text)
        node = dom.getElementsByTagName("tag")
        self.assertEqual(el._getText(node[0]).strip(),text) 


        text = "My test text"
        dom = minidom.parseString("<node> %s</node>" % text)
        node = dom.getElementsByTagName("node")
        self.assertEqual(el._getText(node[0]).strip(),text) 


        dom = minidom.parseString("<node></node>" )
        node = dom.getElementsByTagName("node")
        self.assertEqual(el._getText(node[0]).strip(),'') 


    
if __name__ == '__main__':
    unittest.main()