#!/bin/sh

sudo docker run --name mypostgres -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password -d alarmer-postgre:latest
