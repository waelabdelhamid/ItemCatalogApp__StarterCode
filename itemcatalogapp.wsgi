#!/usr/bin/python
import sys
sys.path.insert(0,"/var/www/FLASKAPPS/")
sys.stdout = sys.stderr
from itemcatalogapp import app as application
