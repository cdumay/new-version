#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
from tat_pytools.common import TatManager


class ReleaseDisplay(TatManager):
    def run(self):
        # we disable logs
        logging.root.setLevel(logging.ERROR)
        if self.check_configuration() is True:
            data = self.tat_client.do_request(
                method="GET",
                path="/messages{topic}".format_map(self.tat_configuration),
                params=dict(
                    skip=0, limit=1, tag="release:{}".format(self.version)
                )
            ).get('messages', list())

            if len(data) > 0:
                print("Release: {}".format(self.version))
                replies = self.tat_client.do_request(
                    method="GET",
                    path="/messages{topic}".format_map(self.tat_configuration),
                    params=dict(
                        skip=0, inReplyOfIDRoot=data[0]["_id"]
                    )
                ).get('messages', list())
                for reply in replies:
                    print("- {}".format(reply["text"][1:]))


def main():
    ReleaseDisplay().run()
