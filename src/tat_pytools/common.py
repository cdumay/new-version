#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import os, sys, logging, json
from cdumay_rest_client.client import RESTClient


class TatManager(object):
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
        self._version = None

    @property
    def version(self):
        if self._version is None:
            self._version = open(self.file_version, 'r').read().strip()
        return self._version
    
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

    def run(self):
        self._critical("Not implemented")
