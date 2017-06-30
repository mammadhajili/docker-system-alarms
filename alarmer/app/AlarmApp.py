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
        #etcd client connection
        self.client = etcd_client.client
        #mail connection
        #mail_host = config.config['mail']['host']
        #mail_port = config.config['mail']['port']
        #self.mail_sender = smtplib.SMTP(mail_host, mail_port)
        #self.mail_sender.ehlo()
        #self.mail_sender.starttls()
        #self.mail_sender.ehlo()
        self.sms_sender = config.config['sms']['url']
    def workOnce(self):
        response = self.client.read('/testing', recursive=True)
        queue = Queue()
        for alarm in response.children:

            key = alarm.key
            value = alarm.value

            alarm_json = json.loads(value)

            db_name = alarm_json['dbname']
            #TODO create a worker for every alarm that needs to be run

            __worker = worker.AlarmRunWorker(queue, db_name, alarm_json, key)
            queue.put(1)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            __worker.daemon = True
            __worker.start()
            __worker.join()



def main():

    app = AlarmApp()
    app.connect()
    app.workOnce()


if __name__ == '__main__':
    main()



