========
b_rabbit
========


.. image:: https://img.shields.io/pypi/v/b_rabbit.svg
        :target: https://pypi.python.org/pypi/b_rabbit

.. image:: https://img.shields.io/travis/nidhaloff/b_rabbit.svg
        :target: https://travis-ci.com/nidhaloff/b_rabbit

.. image:: https://readthedocs.org/projects/b-rabbit/badge/?version=latest
        :target: https://b_rabbit.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




An abstract interface for RabbitMQ communication.

RabbitMq Interface to make using RabbitMQ Message broker easier to implement and maintain especially inside a SOA Projects.
it provides a high level API on top of rabbitpy to abstract the implementation of publish-subscribe and RPCs

It uses Multithreading to assign a single Thread to every Task and reduce the headache of writing boilerplate code.

Take a look at the examples.


* Free software: MIT license
* Documentation: https://b_rabbit.readthedocs.io.


Features
--------

- b_rabbit implements all messaging pattern from working queues, publish-subscribe to remote procedure calls.
- high level API that provide asynchronous messaging.

Contribution
-------
- Contributors and new ideas & suggestions are always welcome
