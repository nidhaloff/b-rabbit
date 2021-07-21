from b_rabbit import BRabbit


def event_listener(msg):
    print('Event received')
    print("Message body is: " + msg.body)
    print("Message properties are: " + str(msg.properties))


rabbit = BRabbit(host='localhost', port=5672)
subscriber = rabbit.EventSubscriber(
                                    b_rabbit=rabbit,
                                    routing_key='publisher.pub',
                                    publisher_name='publisher',
                                    external=False,
                                    event_listener=event_listener)


subscriber.subscribe_on_thread()
