from b_rabbit import BRabbit


def event_listener(body):
    print('Event received')
    print(str(body))


rabbit = BRabbit(
                host='localhost',
                port=5672
)

publisher = BRabbit.EventPublisher(b_rabbit=rabbit, publisher_name='publisher', external=False)
subscriber = rabbit.EventSubscriber(
                                    b_rabbit=rabbit,
                                    routing_key='publisher.pub',
                                    publisher_name='publisher',
                                    external=False,
                                    event_listener=event_listener)


subscriber.subscribe_on_thread()
publisher.publish(routing_key='publisher.pub',
                  payload='Hello from publisher',
                  important=False)

print('End')
