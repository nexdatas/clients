#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012 Jan Kotanski
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
## \file runtest.py
# the unittest runner
#
import unittest
import os

from ndts import TangoDataWriter 
from ndts.TangoDataWriter  import TangoDataWriter 


# test fixture
class TangoDataWriterTest(unittest.TestCase):

    def setUp(self):
        print "setting up..."
        self._tdw = TangoDataWriter("tangodatawritertest.h5")
        self._tdw.openNXFile()

    def tearDown(self):
        print "tearing down ..."
        try:
            self._tdw.closeNXFile()
        finally:
            os.remove("tangodatawritertest.h5")


    def test_creation(self):
        print "Run: TangoDataWriterTest.test_creation() "
        fname = "test.h5"
        try:
            tdw = TangoDataWriter(fname)
            self.assertTrue(tdw.fileName == fname)
            self.assertTrue(tdw.xmlSettings == "")
            self.assertTrue(tdw.json == "{}")
            self.assertTrue(tdw.getNXFile() is None)
            self.assertTrue(tdw.numThreads > 0)
            self.assertTrue(isinstance(tdw.numThreads,(int, long)))
            
            tdw.openNXFile()
            self.assertTrue(tdw.getNXFile() is not None)
            self.assertTrue(tdw.getNXFile().valid)
            self.assertFalse(tdw.getNXFile().readonly)
            
            tdw.closeNXFile()
            
            self.assertTrue(tdw.getNXFile() is None)
        finally:
            os.remove(fname)