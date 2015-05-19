import time
import sys
import subprocess
from threading  import Thread
from Queue import Queue, Empty

# http://stackoverflow.com/questions/28967970/unable-to-process-python-subprocess-stderr-on-windows#

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

cmd = ['dd','if=\\\?\Device\Harddisk1\Partition0', 'of=C:\\temp\\tmp.img', 'bs=32k',
        '--size', '--progress']
a = subprocess.Popen(cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0, shell=True) # notice stderr
while a.poll() is None:
    time.sleep(.3)
    line = a.stderr.r()
    if not line:
        break
    print line

# q = Queue()
# t = Thread(target=enqueue_output, args=(a.stderr, q))
# t.daemon = True # thread dies with program
# t.start()
#
# #read lines without blocking
# while 1:
#     try:
#         line = q.get(timeout=.5)
#         print line
#     except Empty:
#         continue
