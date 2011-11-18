#!/usr/local/bin/python

import sys
import time

def main():
    total = 0
    speed = 1048576
    bytes_per_chunk = 104857
    start_time = time.time()
    bytes_this_chunk = 0
    while True:
        #start_time = time.time()
        v = sys.stdin.read(65536)
        cur_len = len(v)
        bytes_this_chunk += cur_len
        sys.stdout.write(v)
        #print len(v), total
        if cur_len == 0:
            #print 'done?'
            return
        if bytes_this_chunk > bytes_per_chunk:
            cur_time = time.time()
            time_so_far = cur_time - start_time
            if time_so_far >= 0.01:
                pass
            else:
                time.sleep(0.01 - time_so_far)
            start_time = time.time()
            bytes_this_chunk = 0




if __name__ == '__main__':
    main()
