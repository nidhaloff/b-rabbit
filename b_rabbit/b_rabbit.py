"""Main module."""
import rabbitpy
import uuid
import threading
from typing import *
from json import dumps
import logging
from helpers.logs import create_logger

logger = create_logger(__name__)


def calc_execution_time(func):
    """calculate execution Time of a function"""

    from timeit import default_timer
    try:

        def wrapper(*args, **kwargs):

            before = default_timer()
            res = func(*args, **kwargs)
            after = default_timer()
            execution_time = after - before
            print("execution time of the Function {} is :=> {} seconds".format(func.__qualname__, execution_time))
            return res

        return wrapper

    except Exception as e:

        logger.exception(e.args, exc_info=True)


class BRabbit:
    connection = None
    _active_queues = []

    def __init__(self, host: str = 'localhost', port: int = 5672):

        """
		Wrapper class to store the connection to server globally.
		:param str host: Hostname of RabbitMQ Server
		:param int port: Port of RabbitMQ Server
		"""

        self.connection = rabbitpy.Connection('amqp://' + host + ':' + str(port))

    def close_connection(self):
        try:
            self._shutdown_gracefully()
            self.connection.close()
        except Exception as e:
            logger.exception(e.args)

    def add_active_queues(self, queue):
        try:
            self._active_queues.append(queue)
        except Exception as e:
            logger.exception(e.args)

    # @calc_execution_time
    def _shutdown_gracefully(self, delete=False):
        try:
            for activeQueue in self._active_queues:
                if delete:
                    activeQueue.delete()
        except Exception as e:
            logger.exception(e.args)

    class EventPublisher:
        """
			event publisher, which sends events to all subscribers.
			Internal and External Publishers are now together in one Implementation
		"""

        def __init__(self, b_rabbit, publisher_name: str, exchange_type: str = 'topic', external: bool = False):
            """
			Internal event publisher, which sends events to all subscribers.
			Parameters:
			:param str publisher_name: Name of publisher
			"""

            if not b_rabbit.connection:
                raise Exception('Create Instance of Class RabbitMqCommunicationInterface first')

            try:
                self.b_rabbit = b_rabbit
                with b_rabbit.connection.channel() as channel:

                    self.channel = channel
                    self.exchange_name = publisher_name + '_events' if not external else 'External' + publisher_name + '_events'
                    self.exchange = rabbitpy.Exchange(channel=channel,
                                                      name=self.exchange_name,
                                                      exchange_type=exchange_type,
                                                      durable=True)
                    self.exchange.declare()
                    logger.info('Exchange is declared with the name: {}'.format(self.exchange_name))

            except Exception as e:
                logger.debug(e)

        # @calc_execution_time
        def publish(self, routing_key: str, payload: str, important: bool = True):
            """
				Publish of internal event. All internal subscribers will receive it.
				Parameters:
				:param str routing_key: Routing key for event
				:param str payload: Payload of event
				:param str important: indicate whether the publishing important or not,
									if yes it will set the mandatory publishing Feature
			"""

            try:
                with self.b_rabbit.connection.channel() as channel:
                    channel.enable_publisher_confirms()
                    message = rabbitpy.Message(channel=channel, body_value=dumps(payload))

                    published = message.publish(exchange=self.exchange, routing_key=routing_key, mandatory=important)

                    if not published:

                        logger.warning(
                            'message sent from: {} but RabbitMQ indicates Message publishing failure'.format(self.exchange_name))
                    else:

                        logger.info('message sent from: {} and received successfully from RabbitMQ'.format(self.exchange_name))
                return published

            except rabbitpy.exceptions.MessageReturnedException as e:
                logger.error(
                    "Because of the Mandatory Publishing, a Consumer Queue must already be binded to the Exchange"
                    " to make sure that the published message will be sooner or later consumed and we will not lose it"
                    " so make sure that the subscriber Queue is already bounded to the Publisher  \n"
                    "More Description of the Exception => {}".format(e.args))

            except Exception as e:
                logger.debug(e.args, exc_info=False)

    class EventSubscriber:
        """
		Subscribe to events send by publisher
		"""

        # @calc_execution_time
        def __init__(self, b_rabbit, routing_key: str,
                     publisher_name: str, exchange_type: str = 'topic',
                     external: bool = False, important_subscription: bool = True, event_listener: Callable = None):
            """
				Subscribe to events send by publisher
				Parameters:
				:param str routing_key: Routing Key which was set for event by Publisher
				:param str publisher_name: Name of publisher
				:param str exchange_type: Type of exchange
				:param bool external: Is Publisher external?
				:param callable event_listener: User event listener (eventListener(body))
			"""

            if not b_rabbit.connection:
                raise Exception('Create Instance of Class RabbitMqCommunicationInterface first')

            self.b_rabbit = b_rabbit
            self.publisher_name = publisher_name
            with b_rabbit.connection.channel() as channel:
                self.exchange_name = 'External_' + publisher_name + '_events' if external else publisher_name + '_events'

                self.exchange = rabbitpy.Exchange(channel=channel,
                                                  name=self.exchange_name,
                                                  exchange_type=exchange_type,
                                                  durable=True)
                self.exchange.declare()
                logger.info(
                    'Exchange is declared Successfully from Subscriber: {} | with the name: {}'.format(__name__,self.exchange_name))

                subscriber_name = self.exchange_name + '_' + routing_key + '_' + self.__get_subscriber_name() + '_queue'

                logger.info('subscriber name: {}'.format(subscriber_name))
                queue = rabbitpy.Queue(channel,
                                       name=subscriber_name,
                                       durable=important_subscription,
                                       message_ttl=self.__msg_lifetime(),
                                       exclusive=False)
                queue.declare()

                # logger.info('{queue.name} was successfully declared from subscriber: {subscriber_name}')
                queue.bind(self.exchange_name, routing_key)
                self.queue_name = queue.name
                self.event_listener = event_listener

        def __subscribe(self):
            '''
				start waiting on events. You may do this in parallel.
			'''
            with self.b_rabbit.connection.channel() as channel:
                queue = rabbitpy.Queue(channel, self.queue_name)
                self.b_rabbit.add_active_queues(queue)

                for message in queue.consume():
                    message.pprint(True)
                    message.ack()
                    self.event_listener(message.body)

        def subscribe_on_thread(self, *thread_args, **thread_kwargs):
            """start Subscriber on an independent Thread"""

            subscriber_thread = threading.Thread(target=self.__subscribe, *thread_args, **thread_kwargs)
            subscriber_thread.start()
            if subscriber_thread.is_alive():
                logger.info("Subscriber is running on The Thread: {}".format(subscriber_thread.name))

        def __get_subscriber_name(self, in_docker=True):
            """get the subscriber name from host"""
            try:
                if not in_docker:
                    import os
                    name = os.path.dirname(os.path.abspath(__file__))  # get the whole Path of the Project Repository
                    # logger.debug(f'name of the current Subscriber: {name}')
                    return name.split('\\')[-2]  # return only the name of the Project (example: Statistics Service)
                else:
                    import socket
                    name = socket.gethostname()
                    # logger.debug(f'name of the current Subscriber: {name}')
                    return name
            except Exception as e:
                logger.exception(e)

        def __msg_lifetime(self, days: int = 7) -> int:
            """ function to determine how long should the message stay in the Queue.
				delete a Message in a Queue if it will not be consumed for a long Time
				:param days: message life in the Queue. default to one Week
			"""
            try:
                return days * 24 * 60 * 60 * 1000  # convert those days to Milliseconds
            except Exception as e:
                logger.exception(e.args)

    class TaskExecutor:

        corr_id = None
        channel = None

        '''
		TaskExecutor registers on Task which is triggered by TaskRequester.
		'''

        def __init__(self, b_rabbit, executor_name: str, routing_key: str, task_listener):
            """
				TaskExecutor registers on Task which is triggered by TaskRequester.
				:param str executor_name: Name of Executor
				:param str routing_key: Routing Key of task
				:param callable task_listener: User task listener which is called
			"""
            assert type(executor_name) is str, "executor name should be a string"
            assert type(routing_key) is str, "routing key should be a string"

            if not b_rabbit.connection:
                raise Exception('Create Instance of Class BRabbit first')

            self.exchange_name, self.routing_key = executor_name + '_tasks', routing_key
            self.b_rabbit, self.task_listener = b_rabbit, task_listener
            self.executor_name, self.exchange_name = executor_name, self.exchange_name

        def __register_on_task(self, queue_name=''):
            """
				Registers task. This might be called in parallel.
				:param queue_name: task queue that will receive the request. default value set to random uuid queue
			"""

            with self.b_rabbit.connection.channel() as channel:

                task_queue = rabbitpy.Queue(channel, name=queue_name, durable=True, exclusive=True)
                task_queue.declare()
                task_queue.bind(self.exchange_name, self.routing_key)
                self.b_rabbit.add_active_queues(task_queue)

                for message in task_queue.consume():

                    self.channel = channel
                    self.corr_id, self.replyTo = message.properties['correlation_id'], message.properties['reply_to']
                    self.msg, self.deliveryTag = message, message.delivery_tag
                    message.ack()

                    try:
                        self.task_listener(self, message.body)

                    except Exception as e:
                        logger.critical('Error in Custom Implementation of TaskExecuter')
                        logger.debug(e.args, exc_info=False)

        # @calc_execution_time
        def send_return(self, payload: str):
            """
				Send return to TaskRequester which contains the results of task.
				:param str payload: payload of task response
			"""
            assert type(payload) is str, "payload must be a string or convertible to JSON"

            response = rabbitpy.Message(self.channel,
                                        body_value=payload,
                                        properties={'correlation_id': self.corr_id})

            response.publish(exchange='', routing_key=self.replyTo)

        def run_task_on_thread(self, *thread_args, **thread_kwargs):
            """start task Executor on an independent Thread"""

            task_thread = threading.Thread(target=self.__register_on_task, *thread_args, **thread_kwargs)
            task_thread.start()
            if task_thread.is_alive():
                logger.debug("Task Executor is running on The Thread: {}".format(task_thread.name))

    class TaskRequesterSynchron:
        '''
		TaskRequesterSynchron requests tasks synchronously.
		'''
        corr_id = None

        def __init__(self, b_rabbit, executor_name: str, routing_key: str, response_listener):

            """
				TaskRequesterSynchron requests tasks synchronously.
				:param str executor_name: Name of Executor
				:param str routing_key: Routing Key of task which is set by Executor
				:param callable response_listener: User response listener which is called
			"""
            assert type(executor_name) is str, "executor_name argument must be a string"
            assert type(routing_key) is str, "routing_key argument must be a string"

            if not b_rabbit.connection:
                raise Exception('Create Instance of Class RabbitMqCommunicationInterface first')

            self.b_rabbit, self.corr_id, self.executor_name = b_rabbit, str(uuid.uuid4()), executor_name

            with b_rabbit.connection.channel() as channel:
                self.channel, self.routing_key = channel, routing_key
                self.exchange_name, self.response_listener = executor_name + '_tasks', response_listener
                self.exchange = rabbitpy.Exchange(channel=channel,
                                                  exchange_type='direct',
                                                  name=self.exchange_name,
                                                  durable=True)

                self.exchange.declare()
                logger.debug(
                    'Exchange: {} was successfully declared from task Requester: {}'.format('self.exchange_name', 'executor_name'))

        def request_task(self, payload: str, queue_name=''):
            """
				Do request task from executer.
				:param str payload: payload of task Request
				:param str queue_name: name of the callback queue to consume the response
			"""

            assert type(payload) is str, "payload must be of type string"

            with self.b_rabbit.connection.channel() as channel:

                callback_queue = rabbitpy.Queue(channel, name=queue_name, durable=True, exclusive=True)
                callback_queue.declare()
                # logger.info(
                #     f'{callback_queue.name} was successfully declared from task Requester: {self.executor_name}')

                request = rabbitpy.Message(channel,
                                           body_value=payload,
                                           properties={'reply_to': callback_queue.name,
                                                       'correlation_id': self.corr_id})

                request.publish(exchange=self.exchange, routing_key=self.routing_key)
                self.b_rabbit.add_active_queues(callback_queue)

                for message in callback_queue.consume(prefetch=1):
                    message.ack()

                    # check if correlation id fits to the call you did
                    if self.corr_id == message.properties['correlation_id']:
                        self.response_listener(message.body)

    class TaskRequesterAsynchron:
        """
			TaskRequesterSynchron requests tasks asynchon.
		"""

        def __init__(self, b_rabbit, executor_name: str, routing_key: str, response_listener):
            """
			TaskRequesterSynchron requests tasks asynchon.
			:param str executor_name: Name of Executor
			:param str routing_key: routing Key of task which is set by Executor
			:param callable response_listener: User response listener which is called
			"""
            assert type(executor_name) is str, "executor_name must be a string"
            assert type(routing_key) is str, "routing_key must be a string"

            if not b_rabbit.connection:
                raise Exception('Create Instance of Class RabbitMqCommunicationInterface first')

            self.task_requester = b_rabbit.TaskRequesterSynchron(b_rabbit,
                                                                 executerName=executor_name,
                                                                 routingKey=routing_key,
                                                                 responseListener=response_listener)

        def request_task(self, payload: str):
            """
				Do request task from executor.
				:param str payload: Data needed for task execution.
			"""

            assert type(payload) is str, "payload of the request_task method must be of type string"
            thread = threading.Thread(target=lambda: self.task_requester.request_task(payload=payload))
            thread.start()
