import uuid
import pytest


def test_creation(event_publisher, rabbit):
    reference = rabbit.EventPublisher(
        b_rabbit=rabbit,
        publisher_name="event_publisher",
        exchange_type="topic",
        external=False,
    )
    assert reference.b_rabbit == event_publisher.b_rabbit
    assert reference.exchange_name == event_publisher.exchange_name
    assert reference.channel is not event_publisher.channel
    assert reference.exchange is not event_publisher.exchange


def test_creation_exception(rabbit):
    with pytest.raises(Exception):
        rabbit.EventPublisher(b_rabbit=None)


def test_publish_without_properties(rabbit, event_publisher):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload="test",
        important=False,
    )
    assert published is True


def test_invalid_properties(rabbit, event_publisher):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload="test",
        important=False,
        properties={"invalid": str(uuid.uuid4())},
    )
    assert published is None


def test_publish_with_properties(rabbit, event_publisher, properties):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload="test",
        important=False,
        properties=properties,
    )
    assert published is True


def test_publish_unicode_message(rabbit, event_publisher, properties):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload="🐰",
        important=False,
        properties=properties,
    )
    assert published is True


def test_publish_dict_message(rabbit, event_publisher, properties):
    published = event_publisher.publish(
        routing_key="testing.test",
        payload={"key1": True, "key2": "foo", "key3": str(uuid.uuid4())},
        important=False,
        properties=properties,
    )
    assert published is True
