import subprocess
import shlex
def os_system_dd():
   cmd = ['dd','if=\\\?\Device\Harddisk1\Partition0', 'of=C:\\temp\\tmp.img',
                           'bs=512' ,'--size', '--progress']
   # cmd = shlex.split('dd if=\\?\Device\Harddisk1\Partition0 of=C:\temp\tmp.img bs=1M conv=sync --size --progress')
   a = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE) # notice stderr
   print subprocess.list2cmdline(cmd)
   stdout, stderr = a.communicate()

   print stdout, stderr

if __name__ == '__main__':
   os_system_dd()