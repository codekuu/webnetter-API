#!/usr/bin/python3
import sys
import os

currentDir = os.path.dirname(__file__)
sys.path.insert(0, currentDir)

from webnetter import app as application
