Stupid Designs (Dunning–Kruger effect kicks in)
================================================
> Many (much more senior level) programmers believes, that their design is
actually pretty great even if they are not measuring or profiling and with
zero understanding of hardware included. It is true, that a lot of actual
processing is unknown, because quite a lot of today computing components has
completely proprietary internal structure of general computing components like
CPUs. I have actually tried to find how 'Branch prediction' unit is behaving
inside.

# Sure design patterns are great, but ...
> I there is a good saw fitting this in design pattern use, it is this:
"Measure twice cut once". There Dunning-Kruger effect comes to play a lot.
Without profiling and measurement how much CPU time, memory or if distributed
application is the case, then how much application messages is exchanged
between instances and is not killing performance of the application by it self
or network capacity basically DDOSing itself.

> Most recent problem I have encountered many times in a lot of different codes
it that people are not able to see **cost of serialization** between interfaces
and a lot of it comes from [IPC](https://en.wikipedia.org/wiki/Inter-process_communication)
data exchange on the same node with multiple processes. Flame graphs
[http://www.brendangregg.com/flamegraphs.html] are there usually spiking on
**serializing/deserializing** interface. There are other cheaper ways like
/dev/shm in Linux or just shared memory use. Those thing surface a lot in
languages like Python in case of CPython interpreter which is slow by itself and
I really do not want to write about troubles with
[GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock) and how code gets
complicated when you want to use more than one cpu core in this Python
interpret it is always way of creating new processes (multiprocessing) library.
Serialization data into multiprocessing queue could get pretty costly -
default serialization library is Pickle.

>Pickle short
>> Could be quite expensive (CPU time)
>> It can serialize python code and run it after serialization


