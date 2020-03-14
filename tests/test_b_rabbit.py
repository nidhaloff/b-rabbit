#!/usr/bin/env python

"""Tests for `b_rabbit` package."""

import pytest
from b_rabbit.b_rabbit import BRabbit
#b_rabbit = BRabbit(host='localhost', port=5672)


#@pytest.fixture
def callback(body=None):
    # return body
    pass

def subscriber():
    pass
#     sub = b_rabbit.EventSubscriber(b_rabbit=b_rabbit,
#                                    routing_key='testing.test',
#                                    publisher_name='test',
#                                    event_listener=callback)
#     sub.subscribe_on_thread()


@pytest.fixture
def publisher():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # publisher = b_rabbit.EventPublisher(b_rabbit=b_rabbit, publisher_name='test')
    # published = publisher.publish(routing_key='testing.test',
    #                               payload='testing the BRabbit EventPublisher..',
    #                               important=False)
    # return published
    pass


def test_publish(publisher):
    """test require rabbitmq connection. run tests on localhost"""
    # assert publisher == True


# def test_subscribe(callback):
#     subscriber()
#     assert callback == 'testing the BRabbit EventPublisher..'
