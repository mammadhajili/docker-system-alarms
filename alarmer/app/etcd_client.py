import etcd
import config

client = etcd.Client(host=config.config['etcd']['host'], port=int(config.config['etcd']['port']))

