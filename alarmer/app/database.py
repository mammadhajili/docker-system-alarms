import psycopg2
import config
from object_pool import ObjectPool

pools = dict()

for db_name in config.config['databases']:
    # TODO create a pool object and add to pools dict
    pools[db_name] = ObjectPool(config.config['databases'][db_name])


def getPool(db_name):
    return pools[db_name]
