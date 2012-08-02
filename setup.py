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
## \file setup.py
# ndts installer 
import os

## ndts version
__version__="0.0.1"

## reading a file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

## metadata for distutils
SETUPDATA=dict(
    name = "nexdatas",
    version = __version__,
    author = "Jan Kotanski, Eugen Wintersberger , Halil Pasic",
    author_email = "jankotan@gmail.com, eugen.wintersberger@gmail.com, halil.pasic@gmail.com",
    description = ("Nexus Data writer implemented as a Tango Server"),
    license = "GNU GENERAL PUBLIC LICENSE v3",
    keywords = "writer Tango server nexus data",
    url = "http://code.google.com/p/nexdatas/",
    packages=['ndts'],
#    package_data={'ndts': ['TDS']},
    long_description= read('README'),
)

## metadata for setuptools
SETUPTOOLSDATA= dict(
    include_package_data = True,
    install_requires = [
        'numpy>=1.5.0',
        'PyTango>=7.2.2',
        'libpninx-python>=0.1.2'
        ],
)

## the main function
def main():
    try:
        import setuptools
        SETUPDATA.update(SETUPTOOLSDATA)
        setuptools.setup(**SETUPDATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**SETUPDATA)
        

if __name__ == '__main__':
    main()

