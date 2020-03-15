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

b_rabbit is a RabbitMq Interface on top of rabbitpy to make implementing RabbitMQ messaging patterns easier. It is very useful especially
inside large projects, in which many boilerplate code must be written.
it uses a parent wrapper class that wrap all connections and classes definitions of different messaging patterns,
then using the patterns is pretty straightforward by creating instances from the parent class depending on the
pattern you want to use. it uses multithreading to asynchronously orchestrate between multiple subscription and RPCs.



* Free software: MIT license
* Documentation: https://b_rabbit.readthedocs.io.


Features
--------

- it implements all RabbitMQ messaging patterns from work queues to RPCs.
- provides an easy high level API (take a look at the examples)
- thread safe since it uses rabbitpy

Credits
-------
