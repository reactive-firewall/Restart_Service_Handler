restart_service_handler Template
================================

A template for the python script restart_service.py to restart services. By default uses systemV style ``service restart`` to restart services. For remote services usese ``NRPE`` by default to communicate with the remote host.

.. image:: https://travis-ci.org/reactive-firewall/Restart_Service_Handler.svg?branch=master
    :target: https://travis-ci.org/reactive-firewall/Restart_Service_Handler

Syntax:
-------

```bash
restart_service.py [-h] [-E THRESHOLD] [-C | -D] {OK,WARNING,PENDING,UNKNOWN,CRITICAL} {SOFT,HARD} check_count host_name service_cmd service_name
```

positional arguments:
  {OK,WARNING,PENDING,UNKNOWN,CRITICAL}
                        the service status
  {SOFT,HARD}           the service state
  check_count           the service state count
  host_name             the host running the service
  service_cmd           the service restart script
  service_name          the service to restart

optional arguments:
  -h, --help            show this help message and exit
  -E THRESHOLD, --threshold THRESHOLD
                        the threshold at which to take action
  -C, --crit-happens    crit happens - allow hard critical state before taking
                        action, overrides other preferances
  -D, --crit-is-down    crit avoidence - never wait for critical state before
                        taking action, overrides other preferances

That's it!

Possible Improvements:
---------------------
- add more examples to docs
