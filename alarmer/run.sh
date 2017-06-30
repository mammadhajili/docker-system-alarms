#!/bin/sh
 
sudo docker run -d --name alarmer-app --link mypostgres:mypostgres --link myetcd:myetcd alarmer:latest
