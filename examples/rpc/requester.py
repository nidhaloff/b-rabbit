from b_rabbit import BRabbit
import json


def taskResponseListener(body):
    print('Task Response received')
    print(str(body))


rabbit = BRabbit(host='localhost', port=5672)


taskRequesterSynchron = rabbit.TaskRequesterSynchron(b_rabbit=rabbit,
                                                     executor_name='WebsiteAutomationService',
                                                     routing_key='WebsiteAutomationService.createNewGeofence',
                                                     response_listener=taskResponseListener)


taskRequesterSynchron.request_task('mock from requester')


print('End')

rabbit.close_connection()
