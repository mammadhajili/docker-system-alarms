from queue import Queue
import datetime
import csv
from threading import Thread
import database
import etcd_client

class AlarmRunWorker(Thread):
    queue = Queue()
    db_name = None
    db = None
    alarm = None
    client = None
    key = None
    def __init__(self, queue, db_name, alarm, key):
        Thread.__init__(self)
        self.queue = queue
        self.db_name = db_name
        self.db = None
        self.alarm = alarm
        self.key = key
        self.client = etcd_client.client

    def execute_query(self, conn, statement):
        curs = conn.cursor()
        curs.execute(statement)
        datas = curs.fetchall()
        return datas

    def run(self):
        pool = database.pools[self.db_name]
        __resource = pool.getResource()
        conn = __resource.getValue()
        
        datas = self.execute_query(conn, self.alarm['statement'])


        size = len(datas)
        if int(self.alarm['severity']) != size:
            print('Alert', self.alarm['dbname'], self.alarm['statement'], end=" ")
            print("")

            new_json = "{" + '"dbname":"' + self.alarm['dbname'] + '" , "statement":"' + self.alarm['statement'] + '" , "severity":"' + \
                       str(size) + '" , "time_run":"' + str(datetime.datetime.now()) + '"}'
            self.client.set(self.key, new_json)


        pool.returnResource(__resource)
        self.queue.task_done()


