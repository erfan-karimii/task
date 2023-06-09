from celery import Celery
import os
import time
import random
import signal


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskapi.settings')
app = Celery('taskapi')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


class TimeoutException(Exception):
    pass

time_out = 60 # in second

@app.task()
def verify_user(user_id,price_stock,quantity_input,user_credit):
    signal.signal(signal.SIGALRM, timeout_handler)
    
    signal.alarm(time_out)

    time.sleep(random.randint(1,100))
    
    signal.alarm(0)

    if price_stock * quantity_input < user_credit:
        # TODO:
        #این جواب باید به صورت ایمیل یا پیامک به کاربر بارسال شود.
        result = {"Accept":""} 
    else:
        result = {"Deny":"not enough credit"}

    return result
        


def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out after 60 seconds")


