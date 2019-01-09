#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import logging
import re

import os
import sys

from tat_pytools.common import TatManager


class SendMessage(TatManager):
    def tat_reply(self, parent_id, content):
        self.tat_client.do_request(
            method="POST",
            path="/message{topic}".format_map(self.tat_configuration),
            data={
                "text": content, "idReference": parent_id, "action": "reply"
            }
        )
        logging.info(
            "[tat {topic}] Changelog sent to TAT".format_map(
                self.tat_configuration
            )
        )

    def get_tat_message_id(self):
        if os.path.exists(self.file_topic):
            messages = self.tat_client.do_request(
                "GET",
                path="/messages{topic}".format_map(self.tat_configuration),
                params=dict(limit=1, tag="release:{}".format(self.version))
            ).get('messages', list())

            if messages in (None, list()):
                self._critical("Release doesn't exists in TAT")
            else:
                return messages[0]['_id']
        else:
            self._critical("No TOPIC file found")

    def get_content(self):
        return sys.argv[1]

    def run(self):
        if os.path.exists(self.file_version) is False:
            self._critical("No 'VERSION' file found in current dir")

        if self.check_configuration() is False:
            self._critical("Invalid TAT configuration")

        commit_msg = self.get_content()
        if commit_msg in ("", None):
            self._critical("Empty commit message")

        if commit_msg.startswith("devel"):
            logging.info(
                "[tat {topic}] Develop message, disabled TAT send".format_map(
                    self.tat_configuration
                )
            )
        else:
            tat_text = "#{}".format(commit_msg)
            match = re.match(r".*#([A-Z]+-[\d]+).*", tat_text)
            if match:
                jira = match.group(1)
                tat_text = tat_text.replace(jira, "jiraWorld:%s" % jira)
            self.tat_reply(self.get_tat_message_id(), tat_text)


def main():
    SendMessage().run()
