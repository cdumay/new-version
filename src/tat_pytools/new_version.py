#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import os, logging
from distutils.version import StrictVersion
from tat_pytools.common import TatManager


class VersionUpgrade(TatManager):
    @property
    def new_version(self):
        if self._new_version is None:
            self._new_version = self.get_next_version()

        return self._new_version

    def get_next_version(self):
        version = list(StrictVersion(
            open(self.file_version, 'r').read().strip()).version)
        version[2] += 1
        return "{}.{}.{}".format(*version)

    def wrote_version(self):
        open(self.file_version, 'w').write(self.new_version)
        logging.info("Version file updated")
        return self.new_version

    def update_jira_msg(self, _id):
        if "tatwebui_url" in self.tat_configuration:
            open(os.path.join(self.root, "JIRA-MSG"), "w").write(
                "available in {} [{}|{}{}?idMessage={}]".format(
                    self.project, self.new_version,
                    self.tat_configuration['tatwebui_url'],
                    self.tat_configuration['topic'],
                    _id
                )
            )
            logging.info("JIRA-MSG updated")

    def send_to_tat(self):
        if os.path.exists(self.file_topic):
            data = self.tat_client.do_request(
                method="POST",
                path="/message{topic}".format_map(self.tat_configuration),
                data={
                    "text": "#release:{}".format(self.new_version),
                    "labels": [{"text": "develop", "color": "#cccccc"}]
                }
            )
            logging.info(data["info"])
            self.update_jira_msg(data['message']['_id'])
        else:
            logging.error("No TOPIC file found")

    def run(self):
        if os.path.exists(self.file_version) is False:
            self._critical("No 'VERSION' file found in current dir")

        logging.info("New version is '{}'".format(self.new_version))

        if self.check_configuration() is True:
            self.send_to_tat()
        self.wrote_version()


def main():
    VersionUpgrade().run()
