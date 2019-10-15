Be careful about software, that you are installing on your Linux.
[https://reproducible-builds.org/who/]


[https://www.commandlinefu.com/commands/view/4488/analyze-traffic-remotely-over-ssh-w-wireshark]
ssh root@server.com 'tshark -f "port !22" -w -' | wireshark -k -i -



# Possible problems with tcpdump
> tcpdump could get many packets dropped by kernel. They could be suffering by
lack of buffer space, default value could be as low as 2 MiB. So if you have
enough memory available try to increase buffer size.

tcpdump -B 32768

# Favorite way of remote capture

> This is nice even running on OpenWRT devices, with tcpdump and remote traffic
gets about 1% CPU load.

> Nice and simple use with suricata
>> suricata -c &lt;config&gt; -r /tmp/fifo

> Take whatever parts you need:

>> mkfifo /tmp/fifo; ssh-keygen; ssh-copyid root@remotehostaddress; sudo ssh root@remotehost "tcpdump -i any 'not tcp port 22' -w -" > /tmp/fifo &; sudo wireshark -k -i /tmp/fifo;

# Kernel tracing
> strace https://strace.io
>> Aweome tool, slows execution as hell, but writes out all system calls
>> Good even for memory allocations tracing

> perf
>> Quite good utility for CPU bound diagnostics - bad with memory
> pmap
>> Great tool for memory
> eBPF

