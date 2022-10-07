import pytest
from b_rabbit import BRabbit


@pytest.fixture(scope="function")
def rabbit():
    return BRabbit()


@pytest.fixture(scope="function")
def event_publisher(rabbit):
    return rabbit.EventPublisher(
        b_rabbit=rabbit,
        publisher_name="event_publisher",
        exchange_type="topic",
        external=False,
    )


@pytest.fixture(scope="function")
def event_subscriber(rabbit):
    def _event_subscriber(rabbit, callback):
        return rabbit.EventSubscriber(
            b_rabbit=rabbit,
            routing_key="testing.test",
            publisher_name="event_publisher",
            exchange_type="topic",
            external=False,
            important_subscription=True,
            event_listener=callback,
        )

    return _event_subscriber


@pytest.fixture(scope="function")
def properties(rabbit):
    return BRabbit.Properties(correlation_id="test_id")
