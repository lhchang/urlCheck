# urlCheck

## Purpose
urlCheck is a adhoc tool that can be used to measure the uptime (and inversely the downtime) of a HTTP/HTTPS application. The idea stemmed from a need to test a adhoc system failover implementation. What was desired was a method to simply measure the total downtime or uptime of an application as the failover mechanism occurred.

While there exists many tools to monitor server and application status, or for load testing a server/application in a production setting, urlCheck is meant to be a small lightweight standalone tool that allows a user to easily measure uptime/downtime of an application over a defined period of time. 

## How it works
urlCheck uses a defined span of time that is specified by the user and queries a given URL for that specified amount of time. A cumulative timer is kept for every HTTP 200 response urlCheck gets. Upon reception of a host unreachable error or other unexpected HTTP response, another cumulative timer for measuring downtime is started. Each timer is stopped and started again depending on the server state received by urlChecker so that if within the defined test time range the server comes back online, the cumulative timer will begin counting again.

## Requirements
This tools leverages the pycurl library to make HTTP requests. To install:

```apt update && apt install libcurl4-gnutls-dev librtmp-dev```

```pip3 install pycurl```

## Example
```python3 urlcheck.py --url http://www.example.com # will continuously query www.example.com for 10 seconds```

Output:
``` 
Total number of queries made: 43
Number of successful queries: 43 	 Number of error or timed out queries: 0
Timeout was set to 1 second(s)

*****************************************


Total seconds of application uptime: 9.6170
Total seconds of application downtime: 0.0000
100.00% Application uptime 	 0.00% Application downtime

```
