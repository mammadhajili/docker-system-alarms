import json
import smtplib
from queue import Queue
import config
import database
import worker
import etcd_client
app = None    

class AlarmApp:

    client = None
    mail_sender = None
    sms_sender = None

    def connect(self):
        self.client = etcd_client.client
        self.sms_sender = config.config['sms']['url']
    def workOnce(self):
        response = self.client.read('/testing', recursive=True)
        queue = Queue()
        for alarm in response.children:

            key = alarm.key
            value = alarm.value

            alarm_json = json.loads(value)

            db_name = alarm_json['dbname']

            __worker = worker.AlarmRunWorker(queue, db_name, alarm_json, key)
            queue.put(1)
            __worker.daemon = True
            __worker.start()
            __worker.join()



def main():

    app = AlarmApp()
    app.connect()
    app.workOnce()


if __name__ == '__main__':
    main()



