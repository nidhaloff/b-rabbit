from b_rabbit import BRabbit


rabbit = BRabbit(
                host='localhost',
                port=5672
)

publisher = BRabbit.EventPublisher(b_rabbit=rabbit, publisher_name='publisher', external=False)
publisher.publish(routing_key='publisher.pub',
                  payload='Hello from publisher',
                  important=False)

print('End')
