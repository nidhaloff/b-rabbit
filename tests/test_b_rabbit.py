#!/usr/bin/env python

"""Tests for `b_rabbit` package."""

import pytest
import mock
from pytest_mock import mocker
from b_rabbit import BRabbit
import rabbitpy


def test_connection():
    with pytest.raises(Exception):
        BRabbit(host=1234, port='')

    rabbit = BRabbit('/')
    assert rabbit
    assert isinstance(rabbit, rabbitpy.Connection)
