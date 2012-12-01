#!/usr/bin/python
from __future__ import print_function

import xbmc
import subprocess
import functools

# Set of (protocol, local port) tuples.
watched = {
    ('tcp', 22), # SSH
    ('tcp', 445), # samba
    }
sleep_time = 60 * 1000 # sleep time between checks in miliseconds

log = functools.partial(print, "service.inhibit_shutdown:")

def check_services():
    """ Check if any of the watched services is running. """

    netstat = subprocess.check_output(['/bin/netstat', '--protocol=inet', '-n'], universal_newlines=True)

    for line in netstat.split('\n')[2:]:
        items = line.split()

        proto = items[0]
        port = int(items[3].split(':')[-1])

        if (proto, port) in watched:
            log("Found {} connection from {} to port {}".format(proto, items[4], port))
            return True

    log("No connection found.")
    return False

while not xbmc.abortRequested:
    if check_services():
        log("Inhibiting idle shutdown")
        xbmc.executebuiltin('InhibitIdleShutdown(true)')
    else:
        log("Allowing idle shutdown")
        xbmc.executebuiltin('InhibitIdleShutdown(false)')
    xbmc.sleep(sleep_time)
