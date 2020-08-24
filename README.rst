========
b_rabbit
========


.. image:: https://img.shields.io/pypi/v/b_rabbit.svg
        :target: https://pypi.python.org/pypi/b_rabbit

.. image:: https://img.shields.io/travis/nidhaloff/b_rabbit.svg
        :target: https://travis-ci.com/nidhaloff/b_rabbit

.. image:: https://readthedocs.org/projects/b_rabbit/badge/?version=latest
        :target: https://b_rabbit.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/pyversions/b-rabbit
        :alt: PyPI - Python Version
        :target: https://b_rabbit.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/wheel/b-rabbit
        :alt: PyPI - Wheel
        :target: https://pypi.python.org/pypi/b_rabbit

.. image:: https://img.shields.io/pypi/status/b-rabbit
        :alt: PyPI - Status
        :target: https://pypi.python.org/pypi/b_rabbit

.. image:: https://pepy.tech/badge/b-rabbit
    :target: https://pepy.tech/project/b-rabbit

.. image:: https://pepy.tech/badge/b-rabbit/month
    :target: https://pepy.tech/project/b-rabbit/month

.. image:: https://img.shields.io/github/last-commit/nidhaloff/b-rabbit
        :alt: GitHub last commit
        :target: https://pypi.python.org/pypi/b_rabbit

.. image:: https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FNidhalBaccouri
        :alt: Twitter URL
        :target: https://twitter.com/NidhalBaccouri




RabbitMQ without headache.
---------------------------

b_rabbit is a RabbitMq Interface on top of rabbitpy to make implementing RabbitMQ messaging patterns easier. It is very useful especially
inside large projects, in which many boilerplate code must be written.
it uses a parent wrapper class that wrap all connections and classes definitions of different messaging patterns,
then using the patterns is pretty straightforward by creating instances from the parent class depending on the
pattern you want to use. it uses multithreading to asynchronously orchestrate between multiple subscription and RPCs.



* Free software: MIT license
* Documentation: https://b_rabbit.readthedocs.io.

Features
--------

- it implements all RabbitMQ messaging patterns.
- provides an easy high level API (take a look at the examples)
- thread safe since it uses rabbitpy
- implementation of the publish-subscribe pattern
- implementation of the Remote procedure call pattern
- safe message delivery

When you should use it
----------------------
- if you are having problems with other non thread safe libraries (like I did)
- if you want to develop fast by using a high level API
- if you don't want to write much code and save much time
- if you want to use multithreading
- if you want to get started with RabbitMQ

Why you should use it
----------------------
- High level of abstraction
- Simple syntax and readability improvement
- Scalablity (since it uses multiple channels but only one connection)
- Asynchronous fast messaging
- Code reusability

Quick Usage
------------

import the library:

.. code-block:: python


    from b_rabbit import BRabbit

create a parent instance which provide a global rabbitMQ connection

.. code-block:: python

    rabbit = BRabbit(host='localhost', port=5672)

now, just one liner to publish a message:

.. code-block:: python

    publisher = rabbit.EventPublisher(b_rabbit=rabbit,
                                      publisher_name='pub').publish(routing_key='testing.test',
                                                                    payload='Hello from publisher')



or if you want to subscribe and listen to a certain topic:

.. code-block:: python

     def callback(msg):
        # do something with the received msg from the publisher
        print(f"msg received: {msg}")

    # subscribe and run a listener in a thread

    subscriber = rabbit.EventSubscriber(
                                    b_rabbit=rabbit,
                                    routing_key='testing.test',
                                    publisher_name='pub',
                                    event_listener=callback).subscribe_on_thread()

Advanced Usage using RPC
--------------------------

- task requester

.. code-block:: python

    from b_rabbit import BRabbit


    def taskResponseListener(body):
        print('Task Response received')
        print(str(body))


    rabbit = BRabbit(host='localhost', port=5672)
    taskRequesterSynchron = rabbit.TaskRequesterSynchron(b_rabbit=rabbit,
                                                         executor_name='test',
                                                         routing_key='testing.test',
                                                         response_listener=taskResponseListener)

    taskRequesterSynchron.request_task('msg from requester')
    rabbit.close_connection()

- task responser (server)

.. code-block:: python

    from b_rabbit import BRabbit
    import time

    rabbit = BRabbit(host='localhost', port=5672)


    def taskListener(server, body):
        print('Task Request received')
        print(str(body))
        time.sleep(5)
        server.send_return(payload="return this value to requester")


    taskExecuter = rabbit.TaskExecutor(b_rabbit=rabbit,
                                       executor_name='test',
                                       routing_key='testing.test',
                                       task_listener=taskListener).run_task_on_thread()


Further
--------

Take a look in the examples folder for more. b_rabbit implements also the remote procedure call (RPC) pattern


