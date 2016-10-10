********************************************************
TATwebui release updater with Jira commit message sample
********************************************************

Script to add new release in TAT and a commit message for jira tickets.

==============
Required files
==============

VERSION
=======

A plain file with the version number

.. code-block::

    0.1.0

TOPIC
=====

.. code-block:: json

    {
        "topic": "/myTopic",
        "tatwebui_url": "http://tat.example.com/ui/releaseview/list"
    }

=====
Usage
=====

.. code-block::

    # cd /my/python/lib/root
    # tat-new-version
    INFO    : New version is '0.1.1'
    INFO    : Starting new HTTPS connection (1): tat.example.com
    DEBUG   : "POST /tat/engine/message/myTopic HTTP/1.1" 201 466
    INFO    : Message created in /myTopic
    INFO    : JIRA-MSG updated
    INFO    : Version file updated
