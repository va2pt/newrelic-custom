#! /bin/bash

netstat -tun | grep 27017 | grep -v LISTEN | awk '{print $5}'| cut -d: -f1 | sort | uniq -c | sort -nr
