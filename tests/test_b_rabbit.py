#!/usr/bin/env python

"""Tests for `b_rabbit` package."""

import pytest
import mock
from pytest_mock import mocker
from b_rabbit import BRabbit


def test_connection():
    with pytest.raises(RuntimeError):
        BRabbit(host=1234, port='')


def test_something():
    rabbit = BRabbit()
# def test_connection(mocker):
#     mocker.patch.object(BRabbit)
#     BRabbit.EventPublisher.publish = 120
#     manager.method_under_test()
#     manager.sub_method.assert_called_with('somestring', 1, 120)
