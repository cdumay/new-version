#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import os, sys, logging, json
from distutils.version import StrictVersion
from cdumay_rest_client.client import RESTClient

logging.basicConfig(format="%(levelname)-8s: %(message)s", level=logging.DEBUG)


class VersionUpgrade(object):
    def __init__(self, config="~/.tatcli/config.json"):
        self.root = os.curdir
        self.file_version = os.path.join(self.root, "VERSION")
        self.file_topic = os.path.join(self.root, "TOPIC")
        self.file_config = os.path.expanduser(config)
        self._config = None
        self._tat_config = None
        self._tat_client = None
        self.project = os.path.basename(os.path.realpath(os.curdir))
        self._new_version = None

    def check_configuration(self):
        result = True
        if self.configuration:
            for key in ('url', "username", "password"):
                if key not in self.configuration:
                    logging.error(
                        "Missing configuration value for {}".format(key)
                    )
                    result = False
        else:
            logging.error("TAT is not configured, nothing to do")
            result = False
        return result

    @property
    def new_version(self):
        if self._new_version is None:
            self._new_version = self.get_next_version()

        return self._new_version

    @property
    def configuration(self):
        if self._config is None:
            if os.path.exists(self.file_config):
                try:
                    self._config = json.load(open(self.file_config, 'r'))
                except Exception as exc:
                    logging.warning(exc)
                    self._config = dict()
            else:
                self._config = dict()
        return self._config

    @property
    def tat_configuration(self):
        if self._tat_config is None:
            if os.path.exists(self.file_topic):
                try:
                    self._tat_config = json.load(open(self.file_topic, 'r'))
                except Exception as exc:
                    logging.warning(exc)
                    self._tat_config = dict()
            else:
                self._tat_config = dict()
        return self._tat_config

    @property
    def tat_client(self):
        if self._tat_client is None:
            self._tat_client = RESTClient(
                server=self.configuration['url'],
                headers={
                    "Tat_username": self.configuration["username"],
                    "Tat_password": self.configuration["password"],
                    "Content-type": "application/json",
                }
            )

        return self._tat_client

    @staticmethod
    def _critical(message):
        logging.critical(message)
        sys.exit(1)

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
