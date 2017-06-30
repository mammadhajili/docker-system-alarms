import psycopg2
import cx_Oracle
from collections import defaultdict
class Resource:
    """ Some resource, that clients need to use.

    The resources usualy have a very complex and expensive
    construction process, which is definitely not a case
    of this Resource class in my example.
    """

    __value = None

    def reset(self):
        """ Put resource back into default setting. """
        self.__value = None

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value


class ObjectPool:
    """ Resource manager.
    """

    __db = None
    __resources = dict()

    def __init__(self, db):
        self.__db = db
        self.__resources.setdefault(self.__db['dbname'], [])

    def getResource(self):
        #print(len(self.__resources))
        if len(self.__resources[self.__db['dbname']]) > 0:
            print("Using existing resource.")

            __resource = self.__resources[self.__db['dbname']].pop(0)
            return __resource

        else:
            print("Creating new resource.", self.__db['dbname'])
            newRes = Resource()
            if self.__db['type'] == 'postgres':
                conn_string = self.__db['connection']
                conn = psycopg2.connect(conn_string)
                newRes.setValue(conn)
                return newRes

            elif self.__db['type'] == 'oracle':
                conn_string = self.__db['connection']
                conn = cx_Oracle.connect(conn_string)
                newRes.setValue(conn)
                return newRes

    def returnResource(self, resource):
        #resource.reset()
        self.__resources[self.__db['dbname']].append(resource)


