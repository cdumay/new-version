#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import os

from tat_pytools.common import TatManager


class AnnonceMessage(TatManager):
    def tat_add_message(self):
        if os.path.exists(self.file_topic):
            self.tat_client.do_request(
                method="POST",
                path="/message{topic_run}".format_map(self.tat_configuration),
                data={
                    "text": "#new-release {} {} is ready to prod".format(
                        self.project, self.version
                    ),
                }
            )

    def run(self):
        if os.path.exists(self.file_version) is False:
            self._critical("No 'VERSION' file found in current dir")

        if self.check_configuration() is False:
            self._critical("Invalid TAT configuration")

        self.tat_add_message()


def main():
    AnnonceMessage().run()
