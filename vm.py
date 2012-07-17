from subprocess import Popen
from disks import *

PORT_BASE = 10000
# Ports to forward into the guest
PORTS = [ 22, 80, 443 ]

class VM(object):
    def __init__(self, extra_args = [], netboot = False, snapshot = False):

        args = [ "qemu-kvm", "-m", "1023", "-net", "nic,vlan=1" ]

        if snapshot:
            args += ["-snapshot"]

        netargs = "user,vlan=1"

        # Forward ports into the VM
        for port in PORTS:
            netargs += ",hostfwd=tcp::{hostport}-:{guestport}".format(
                hostport = PORT_BASE + port,
                guestport = port )

        if netboot:
            args += [ "-boot", "n" ]
            netargs += ",tftp=pxe,bootfile=/pxelinux.0"
        else:
            args += [ "-boot", "c" ]

        args += [ "-net", netargs ]

        # Disks
        args += [ "-drive", "file={0},index=0,media=disk".format( HD_BOOT ),
                  "-drive", "file={0},index=1,media=disk".format( HD_ROOT ) ]

        args += extra_args

        self.p = Popen( args )

    def wait(self):
        return self.p.wait()
