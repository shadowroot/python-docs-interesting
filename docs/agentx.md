AgentX SNMP subagent with multiprocess Python
===============================================

### Tags: Python, SNMP, SNMP Agent, AgentX, Python Forking, Pickle, JSON, Multiprocessing, Multiprocessing Queue


If tasks running in your web server are highly CPU bound - eg. doing
a lot of parsing, visible or invisible serializing and you need to run SNMP
counters, then there is an example of doing that.

# Solution
Simplest is to use Named Pipes on Linux, other options like sockets
(file sockets, tcp sockets), AMQs are recommended, when you want to balance
a load a bit between multiple machines.

Be careful about **serialization cost**, it is not visible every time and
could be more expensive, than you think. If you are not sure, where problem
could be - try to **profile** your code.

Why you shouldn't pickle -
[https://www.benfrederickson.com/dont-pickle-your-data/]. In order to not end up
in a pickle. [https://medium.com/@jwnx/multiprocessing-serialization-in-python-with-pickle-9844f6fa1812]

Multiprocessing library uses Pickle for data serialization. Queues are mostly
realized as stdin - stdout and vice versa connected processes and data serialization
internally is realized by pickle.

Protocol Buffers (https://developers.google.com/protocol-buffers) could be
more interesting choice than JSON, **never** use **pickle** it can serialize
eg. python methods, ... . Python implementation json is also quite slow json is
faster but needs compilation. XML has quite data overhead, avoid it if you can.

Use of /dev/shm is not very well implemented in Python so far, Named pipes are
better for now.

## Implementation
Use of multiprocessing queue vs socket with simple serialization.


# Possible problems
## Multiple registrations on the same OID
If in SNMP log are mentioned like this 'duplicate registration', it is almost
a sure thing, that you are running more that 1 instance of snmp agent.
Simple way to investigate it is:

Watch connections, there needs to be only 1 connection.
> Port is 705 in this case.

> watch "netstat -anp | grep 705"

It is also wise to watch changes in counters
> watch "snmpwalk -v 2c -c acipublic localhost:161 .1.3.6.1.4.1.3830"

## Troubleshooting net snmp agent library
The net snmp agent Python library uses same net-snmp
(system binary libraries) as snmpd, if it is used on the same machine, so
version incompatibility is very unlikely to happen.

## Problem with forking control in WSGI servers
When you are creating multiple workers in web server (Gunicorn. uWSGI). Those
servers have hooks in their lifecycle, but those hooks could be weirdly
invoked - not whole module loaded, just methods and it can be
different on each server - use of Gunicorn with sync worker class caused
CORE DUMPS with 'when_ready' hook used for single instancing(singleton) of SNMP
subagent.


