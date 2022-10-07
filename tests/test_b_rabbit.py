import pytest
from b_rabbit import BRabbit
import rabbitpy


def test_connection():
    with pytest.raises(Exception):
        BRabbit(host=1234, port="")


def test_rabbitmq_connection(rabbit):
    assert isinstance(rabbit, BRabbit)
    assert isinstance(rabbit.connection, rabbitpy.Connection)


def test_publisher(event_publisher, properties):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload="test",
        important=False,
        properties=properties,
    )
    assert published is True


def test_subscriber(event_subscriber, rabbit):
    def callback(msg):
        assert msg.body.decode("utf-8") == "test"
        assert msg.properties["correlation_id"] == "test_id"

    subscriber = event_subscriber(rabbit, callback)
    subscriber.subscribe_on_thread()
    rabbit.close_connection()
