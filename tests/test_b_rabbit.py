#!/usr/bin/env python

"""Tests for `b_rabbit` package."""

import pytest
import mock
from pytest_mock import mocker
from b_rabbit import BRabbit
import rabbitpy


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

# def test_publisher():
#     rabbitpy.Connection
