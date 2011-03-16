#!/bin/env python
# -*- coding: utf-8 -*- vim: set ts=4 et sw=4 fdm=indent :
import os, simplejson, sys

class MCollectiveActionNoEnv(Exception):
    pass
class MCollectiveActionFileError(Exception):
    pass

class MCollectiveAction(object):
    def __init__(self, *args, **kwargs):
        try:
            self.infile = os.environ['MCOLLECTIVE_REQUEST_FILE']
        except KeyError:
            raise MCollectiveActionNoEnv("No MCOLLECTIVE_REQUEST_FILE environment variable")
        try:
            self.outfile = os.environ['MCOLLECTIVE_REPLY_FILE']
        except KeyError:
            raise MCollectiveActionNoEnv("No MCOLLECTIVE_REPLY_FILE environment variable")

        self.request = {}
        self.reply = {}

        self.load()

    def load(self):
        if not self.infile:
            return False
        try:
            infile = open(self.infile, 'r')
            self.request = simplejson.load(infile)
            infile.close()
        except IOError, e:
            raise MCollectiveActionFileError("Could not read request file `%s`: %s" % (self.infile, e))
        except simplejson.JSONDecodeError, e:
            infile.close()
            raise MCollectiveActionFileError("Could not parse JSON data in file `%s`: %s", (self.infile, e))

    def send(self):
        if not getattr(self, 'outfile', None): # if exception was raised during or before setting self.outfile
            return False
        try:
            outfile = open(self.outfile, 'w')
            simplejson.dump(self.reply, outfile)
            outfile.close()
        except IOError, e:
            raise MCollectiveActionFileError("Could not write reply file `%s`: %s" % (self.outfile, e))

    def fail(self):
        sys.exit(1)

    def __del__(self):
        self.send()
