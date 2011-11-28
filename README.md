throttle.py -- A Bandwidth throttler in python
==============================================

throttle.py takes (by default) stdin and writes it to stdout limited to whatever rate you specify.  This is useful for limiting disk bandwidth, or in conjunction with nc, network bandwidth.

The actual algorithm for performing the rate limiting runs every 10ms.  100 times a second it writes 1/100th of the per-second data rate that you specify.  If for some reason the input fails to keep up with the output, throttle.py will continue writing as fast as it can, until the average it back to the rate specified.

Inspired by James Klicman's c throttle at http://klicman.org/throttle/


Instructions:
-------------

```
Usage: throttle.py [options]

Options:
  -h, --help            show this help message and exit
  --bandwidth=BANDWIDTH
                        Bytes / second to rate limit to
  --block-size=BLOCK_SIZE
                        bytes to read at a time (1K default).  Bigger may mean
                        less cpu usage, especially for high bandwidth, low
                        latency throttlings.  Try 65536 if you want to bump
                        this up.
  --input-file=INPUT_FILE
                        file to read from (default stdin)
  --output-file=OUTPUT_FILE
                        file to write to (default stdout)
```

Example: `cat largefile.txt | python throttle.py --bandwidth 1048576 > largefile2.txt` would write largefile.txt to largefile2.txt at the rate of 1MB/s
