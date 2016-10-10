**************************************************
TATwebui release tools for python libs development
**************************************************

This python library is a bundle of scripts to facilitate python library
development. It provide:

* **tat-new-version**: a binary to create a new release.
* **commit-msg**: a git hook to send commit messages in TAT.

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

===============
tat-new-version
===============

.. code-block::

    # cd /my/python/lib/root
    # tat-new-version
    INFO    : New version is '0.1.1'
    INFO    : Starting new HTTPS connection (1): tat.example.com
    DEBUG   : "POST /tat/engine/message/myTopic HTTP/1.1" 201 466
    INFO    : Message created in /myTopic
    INFO    : JIRA-MSG updated
    INFO    : Version file updated

==========
commit-msg
==========

To install just link `commit-msg` into your projet git hook folder::

    # cd /my/python/lib/root
    # ln -s /where/is/commit-msg .git/hooks


.. code-block::

    # cd /my/python/lib/root
    # git commit -am 'feat: This is a test'

.. note::

    To disable TAT send, just prefix your commit message with **devel**

You can link jira ticket using a *#<TicketName>* to generate a jira link:

.. code-block::

    # git commit -am 'feat: This is a test (#TICKET-ID)'