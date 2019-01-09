#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import sys

from tat_pytools.message import SendMessage


class CommitHook(SendMessage):
    def get_content(self):
        return open(sys.argv[1], 'r').read().strip()


def main():
    CommitHook().run()
