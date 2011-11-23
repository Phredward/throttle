#! /usr/bin/python

import sys
import time

def main():
    total = 0
    #speed = 1048576
    bytes_per_chunk = 104857
    start_time = time.time()
    super_start_time = start_time
    bytes_this_chunk = 0
    while True:
        #start_time = time.time()
        v = sys.stdin.read(1024)
        cur_len = len(v)
        bytes_this_chunk += cur_len
        total += cur_len
        sys.stdout.write(v)
        #print >> sys.stderr, len(v), total
        if cur_len == 0:
            print >> sys.stderr, 'done?'
            return
        if bytes_this_chunk > bytes_per_chunk:
            cur_time = time.time()
            #print >> sys.stderr, 1.0*bytes_this_chunk/(cur_time-start_time)
            time_so_far = cur_time - start_time
            if time_so_far >= 0.01:
                pass
            else:
                time.sleep(0.01 - time_so_far)
                #newt=time.time()
            start_time = time.time()
            start_time = cur_time + 0.01 - time_so_far
            bytes_this_chunk = 0




if __name__ == '__main__':
    main()
