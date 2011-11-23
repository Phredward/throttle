#! /usr/bin/python

import sys
import time

BLOCK_READ_SIZE = 1024 #larger size = less cpu usage


def write_one_timeslice(readfile, writefile, bytes_to_send, old_leftover_data):
    bytes_sent = 0
    new_leftover_data = None
    if old_leftover_data:
        data_to_write = old_leftover_data[:bytes_to_send]
        new_leftover_data = old_leftover_data[bytes_to_send:]
        bytes_sent = len(data_to_write)
        writefile.write(data_to_write)
    while bytes_sent < bytes_to_send:
        data = readfile.read(BLOCK_READ_SIZE)
        data_len = len(data)
        if data_len == 0:
            return (True, None) #is_done, leftover_data
        chunk = bytes_to_send-bytes_sent
        if chunk >= data_len:
            data_to_write = data
            new_leftover_data = None
        else:
            data_to_write = data[:chunk]
            new_leftover_data = data[chunk:]
            data_len = chunk
        writefile.write(data_to_write)
        bytes_sent += data_len
    return (False, new_leftover_data)


def main():
    total = 0
    #speed = 1048576
    bytes_per_chunk = 104857
    start_time = time.time()
    super_start_time = start_time
    bytes_this_chunk = 0
    is_done = False
    leftover_data = None
    while not is_done:
        is_done, leftover_data = write_one_timeslice(sys.stdin, sys.stdout, bytes_per_chunk, leftover_data)
        #ok, we've written the right amount of data for our timeslice, now how much time has passed?
        cur_time = time.time()
        time_so_far = cur_time - start_time
        if time_so_far >= 0.01:
            #print >> sys.stderr, "more %0.6f" % time_so_far
            pass
        else:
            #print >> sys.stderr, "less %0.6f" % time_so_far
            time.sleep(0.01 - time_so_far)
        #start_time = cur_time + 0.01 - time_so_far #works even if we go over.
        start_time = start_time + 0.01 #what we really want

    print >> sys.stderr, 'done?'


if __name__ == '__main__':
    main()
