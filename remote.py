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

    def _check_call(self, cmd):
        fds = self.exec_command( cmd )
        assert fds[0].channel.recv_exit_status() == 0

    def push_dir( self, localdir, remdir,
                  remove_remote = False,
                  mode = "0775" ):

        if remove_remote:
            self._check_call( "rm -rf {0}".format( remdir ) )

        # Create the remote dir if necessary
        self._check_call( "test -e {0} || mkdir -p {0}".format( remdir ) )

        # Fix permissions
        print "chmod {0} {1}".format( mode, remdir )

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

        assert p.wait() == 0
        assert fds[0].channel.recv_exit_status() == 0

        # WARNING: There will be a gap in time when the requested permissions
        #          do not apply.  This needs fixing!
        self._check_call( "chmod {0} {1}".format( mode, remdir ) )
