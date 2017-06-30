sudo docker run \
  -p 2379 \
  --volume=/var/lib/etcd:/etcd-data \
  --name myetcd -d quay.io/coreos/etcd:latest \
  /usr/local/bin/etcd 




