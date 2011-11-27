#! /usr/bin/python

import optparse
import sys
import time

DEFAULT_BLOCK_SIZE = 1024 #larger size = less cpu usage
DEFAULT_BW = 1048576 #1MB/s default


def write_one_timeslice(readfile, writefile, bytes_to_send, old_leftover_data, block_size):
    bytes_sent = 0
    new_leftover_data = None
    if old_leftover_data:
        data_to_write = old_leftover_data[:bytes_to_send]
        new_leftover_data = old_leftover_data[bytes_to_send:]
        bytes_sent = len(data_to_write)
        writefile.write(data_to_write)
    while bytes_sent < bytes_to_send:
        data = readfile.read(block_size)
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


def init_options():
    global options, args
    parser = optparse.OptionParser()
    parser.add_option("--bandwidth", default=DEFAULT_BW, type="int", help="Bytes / second to rate limit to")
    parser.add_option("--block-size", default=DEFAULT_BLOCK_SIZE, type="int", help="bytes to read at a time (1K default).  Bigger may mean less cpu usage, especially for high bandwidth, low latency throttlings.  Try 65536 if you want to bump this up.")
    parser.add_option("--input-file", default=sys.stdin, type="string", help="file to read from (default stdin)")
    parser.add_option("--output-file", default=sys.stdout, type="string", help="file to write to (default stdout)")
    options, args = parser.parse_args()

def main():
    init_options()
    total = 0
    bytes_per_chunk, remainder_per_chunk = divmod(options.bandwidth, 100)
    start_time = time.time()
    super_start_time = start_time
    is_done = False
    leftover_data = None
    remainder_this_chunk = 0
    while not is_done:
        bytes_this_chunk = bytes_per_chunk
        remainder_this_chunk += remainder_per_chunk
        while remainder_this_chunk >= 100:
            bytes_this_chunk += 1
            remainder_this_chunk -= 100
        is_done, leftover_data = write_one_timeslice(options.input_file, options.output_file, bytes_this_chunk, leftover_data, options.block_size)
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
