# Stuff for interacting with the VM remotely
import ssh
import subprocess
from subprocess import Popen, PIPE

class VMSSH(object):
    def __init__(self):
        self.c = ssh.SSHClient()
        self.c.set_missing_host_key_policy(ssh.AutoAddPolicy())
        self.c.connect( "127.0.0.1", port=10022,
                        username="root", password="123456" )
        
    def exec_command(self, cmd):
        return self.c.exec_command(cmd)

    def push_dir( self, localdir, remdir, remove_remote = False ):

        if remove_remote:
            self.exec_command( "rm -rf {0}".format( remdir ) )

        # Create the remote dir if necessary
        self.exec_command( "test -e {0} || mkdir {0}".format( remdir ) )

        # Tar it up locally
        p = Popen( "tar -c ./",
                   shell = True,
                   stdout = PIPE,
                   cwd = localdir )

        # Untar it remotely
        # stdin, stdout, stderr
        fds = self.exec_command( "tar -xC {0}".format( remdir ) )

        r = None
        while r != "":
            r = p.stdout.read(10240)
            fds[0].write(r)

        p.wait()