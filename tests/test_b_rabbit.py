#!/usr/bin/env python

"""Tests for `b_rabbit` package."""

import pytest
import mock
import time
from pytest_mock import mocker
from b_rabbit import BRabbit
import rabbitpy

MSG = 'mock'
REQUEST_MSG = 'request_msg'
RESPONSE_MSG = 'response_msg'


@pytest.fixture
def rabbit():
    return BRabbit()


def test_connection():
    with pytest.raises(Exception):
        BRabbit(host=1234, port='')


def test_rabbitmq_connection(rabbit):
    assert rabbit
    assert isinstance(rabbit, BRabbit)
    assert isinstance(rabbit.connection, rabbitpy.Connection)


def test_publisher(rabbit):
    publisher = rabbit.EventPublisher(b_rabbit=rabbit,
                                      publisher_name='test',
                                      exchange_type='topic',
                                      external=False)
    published = publisher.publish(routing_key='testing.test', payload=MSG, important=False)
    assert published is True


def test_subscriber(rabbit):
    def callback(msg):
        assert msg == MSG

    subscriber = rabbit.EventSubscriber(b_rabbit=rabbit,
                                        routing_key='testing.test',
                                        publisher_name='test',
                                        exchange_type='topic',
                                        external=False,
                                        important_subscription=True,
                                        event_listener=callback)
    subscriber.subscribe_on_thread()
    rabbit.close_connection()


def test_requester(rabbit):
    def callback(msg):
        assert msg == RESPONSE_MSG

    requester = rabbit.TaskRequesterSynchron(b_rabbit=rabbit,
                                             executor_name='requester',
                                             routing_key='requester.request',
                                             response_listener=callback)
    requester.request_task(payload=REQUEST_MSG)
    rabbit.close_connection()


def test_responser(rabbit):
    def serve(server, msg):
        assert msg == REQUEST_MSG
        time.sleep(3)
        server.send_return(payload=RESPONSE_MSG)

    responser = rabbit.TaskExecutor(b_rabbit=rabbit,
                                    executor_name='requester',
                                    routing_key='requester.request',
                                    task_listener=serve)
    responser.run_task_on_thread()
    with pytest.raises(Exception):
        time.sleep(10)
        rabbit.close_connection()
