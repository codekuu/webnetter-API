#!/usr/bin/python3
import sys
import os

here = os.path.dirname(__file__)
sys.path.insert(0, here)

from webnetter import app as application
