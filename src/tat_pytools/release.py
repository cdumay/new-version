#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import re
from tat_pytools.common import TatManager


class ReleaseDisplay(TatManager):
    def run(self):
        # we disable logs
        logging.root.setLevel(logging.ERROR)
        if self.check_configuration() is True:
            releases = self.tat_client.do_request(
                method="GET",
                path="/messages{topic}".format_map(self.tat_configuration),
                params=dict(skip=0, limit=3, startTag="release:")
            ).get('messages', list())

            regexp = re.compile(r"#release:(.*?)$")
            for release in releases:
                print("Release: {} [{}]".format(
                    regexp.match(release["text"]).group(1),
                    release["labels"][0]["text"]
                ))
                replies = self.tat_client.do_request(
                    method="GET",
                    path="/messages{topic}".format_map(self.tat_configuration),
                    params=dict(
                        skip=0, inReplyOfIDRoot=release["_id"]
                    )
                ).get('messages', list())
                for reply in replies:
                    print("- {}".format(reply["text"][1:]))
                print("")


class CurrentReleaseDisplay(TatManager):
    def run(self):
        # we disable logs
        logging.root.setLevel(logging.ERROR)
        if self.check_configuration() is True:
            releases = self.tat_client.do_request(
                method="GET",
                path="/messages{topic}".format_map(self.tat_configuration),
                params=dict(
                    skip=0, limit=1, tag="release:{}".format(self.version)
                )
            ).get('messages', list())

            for release in releases:
                print("Release: {}".format(self.version))
                replies = self.tat_client.do_request(
                    method="GET",
                    path="/messages{topic}".format_map(self.tat_configuration),
                    params=dict(
                        skip=0, inReplyOfIDRoot=release["_id"]
                    )
                ).get('messages', list())
                for reply in replies:
                    print("- {}".format(reply["text"][1:]))
                print("")


def main():
    ReleaseDisplay().run()


def last():
    CurrentReleaseDisplay().run()
