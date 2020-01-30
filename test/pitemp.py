#!/usr/bin/env python
# Code from: https://www.raspberrypi.org/forums/viewtopic.php?t=22180
# Also required: sudo apt-get install python-psutil or maybe pip3 install psutil
# ref: https://psutil.readthedocs.io/en/latest/
from __future__ import division
from subprocess import PIPE, Popen
import psutil


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def main():
#    cpu_temperature = get_cpu_temperature()
    cpu_usage = psutil.cpu_percent()
    
#    ram = psutil.phymem_usage()
#    ram_total = ram.total / 2**20       # MiB.
#    ram_used = ram.used / 2**20
#    ram_free = ram.free / 2**20
#    ram_percent_used = ram.percent
    
    disk = psutil.disk_usage('/')
    disk_total = disk.total / 2**30     # GiB.
    disk_used = disk.used / 2**30
    disk_free = disk.free / 2**30
    disk_percent_used = disk.percent
    # 
    # Print top five processes in terms of virtual memory usage.
    # 
    processes = sorted(
        ((p.get_memory_info().vms, p) for p in psutil.process_iter()),
        reverse=True
    )
    for virtual_memory, process in processes[:5]:
        print ( virtual_memory // 2**20, process.pid, process.name )


if __name__ == '__main__':
    main()
