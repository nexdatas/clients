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
# \package  ndtstools tools for ndts
## \file simpleClient.py
# first example of simple client

import sys, os
import time

import PyTango

## the main function
def main():
    if  len(sys.argv) < 2:
        print "usage: simpleClient.py  <XMLfile>  <H5file>  <tangoServer>"
        
    else:
        xmlf = sys.argv[1]
        if os.path.exists(xmlf):

            if len(sys.argv) > 2:
                
                fname = sys.argv[2]
                print fname
            else:
                sp = xmlf.split(".")
                print sp
                if sp[-1] == 'xml' :
                    fname = ''.join(sp[0:-1])
                else:
                    fname = xmlf
                fname = fname.strip() + ".h5"
            print "storing in ", fname 
    
            device = "p09/tdw/r228"
            if len(sys.argv) > 3:
                device = sys.argv[3]
            
            dpx = PyTango.DeviceProxy(device)
            dpx.set_timeout_millis(25000)
            dpx.Init()
            print " Connected to: ", device
    
            xml = open(xmlf, 'r').read()


            dpx.FileName = fname

            print "opening the H5 file"
            dpx.OpenFile()

            dpx.XMLSettings = xml
            dpx.JSONRecord = '{"decoders":{"MLIMA":"ndts.DecoderPool.VDEOdecoder"}}'

            print "opening the entry"
            dpx.OpenEntry()

            print "recording the H5 file"
            dpx.record('{"data": {"emittance_x": 0.1},  "triggers":["trigger1", "trigger2"]  }')
            
            print "sleeping for 1s"
            time.sleep(1)

            print "recording the H5 file"
            dpx.record('{"data": {"emittance_x": 0.3} }')


            print "sleeping for 1s"
            time.sleep(1)

            print "recording the H5 file"
            dpx.record('{"data": {"emittance_x": 0.6},  "triggers":["trigger1"]  }')
            

            print "sleeping for 1s"
            time.sleep(1)

            print "recording the H5 file"
            dpx.record('{"data": {"emittance_x": 0.5} }')

            print "sleeping for 1s"
            time.sleep(1)

            print "recording the H5 file"
            dpx.record('{"data": {"emittance_x": 0.1},  "triggers":["trigger2"]  }')
            


            print "closing the  entry"
            dpx.closeEntry()
            print "closing the H5 file"
            dpx.closeFile()


if __name__ == "__main__":
    main()
            
                
            
            

