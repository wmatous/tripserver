#!/usr/bin/python

class PathParser:

    def __init__(self, path = None):
        self.path = path
        self.components = path.split('/')
        del self.components[0]
    

