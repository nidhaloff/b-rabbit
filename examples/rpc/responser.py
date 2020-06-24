from b_rabbit import BRabbit
import time

rabbit = BRabbit(host='localhost', port=5672)


def taskListener(server, body):
    print('Task Request received')
    print(str(body))
    time.sleep(5)
    server.send_return(payload="return this value to requester")


taskExecuter = rabbit.TaskExecutor(b_rabbit=rabbit,
                                   executor_name='WebsiteAutomationService',
                                   routing_key='WebsiteAutomationService.createNewGeofence',
                                   task_listener=taskListener)

taskExecuter.run_task_on_thread()
