from subprocess import Popen
from disks import *
from proc import run
import os

PORT_BASE = 10000
# Ports to forward into the guest
PORTS = [ 22, 80, 443, 9418 ]

GRAPHICS_DEFAULT = 0
GRAPHICS_HIDE = 1

class VM(object):
    def __init__(self, extra_args = [], netboot = False, snapshot = False,
                 graphics = GRAPHICS_DEFAULT ):
        self.netboot = netboot
        self.extra_args = extra_args
        self.snapshot = snapshot
        self.disk_set = "base"
        self.graphics = graphics

    def add_args(self, args):
        self.extra_args += args

    def new_disk(self, name, size):
        "Create a new disk and add it to the current set"

        run( "qemu-img create -f qcow2 {0} {1}".format(
                self.disk_get_path( name ),
                size ) )

    def create_default_disks(self):
        "Create the set of default disks"

        self.new_disk( "hd-boot", "1G" )
        self.new_disk( "hd-root", "30G" )

    def create_set(self, name, base = "base"):
        "Create a new set of disks, and switch to it"

        disks = { "hd-boot": {}, "hd-root": {} }

        for disk_name, info in disks.iteritems():
            info["base"] = self.disk_get_path(disk_name)

        self.set_disk_set( name )
        os.mkdir( self.disk_get_dir() )

        for disk_name, info in disks.iteritems():
            new = self.disk_get_path(disk_name)

            run( "qemu-img create -f qcow2 -o backing_file={0} {1}".format(
                    info["base"], new ) )

    def list_disk_sets(self):
        "Return a list of the names of the available disk snapshots"

        snapshots = []
        for f in os.listdir( DISKS_DIR ):
            full = os.path.join( DISKS_DIR, f )

            if os.path.isdir(full):
                snapshots.append(f)

        return snapshots

    def set_disk_set(self, name):
        self.disk_set = name

    def disk_get_dir(self):
        return os.path.join( DISKS_DIR, self.disk_set )

    def disk_get_path(self, disk):
        return os.path.join( self.disk_get_dir(), disk )

    def run(self):
        args = [ "qemu-kvm", "-m", "1023", "-net", "nic,vlan=1" ]

        if self.snapshot:
            args += ["-snapshot"]

        netargs = "user,vlan=1"

        # Forward ports into the VM
        for port in PORTS:
            netargs += ",hostfwd=tcp::{hostport}-:{guestport}".format(
                hostport = PORT_BASE + port,
                guestport = port )

        if self.netboot:
            args += [ "-boot", "n" ]
            netargs += ",tftp=pxe,bootfile=/pxelinux.0"
        else:
            args += [ "-boot", "c" ]

        args += [ "-net", netargs ]

        # Disks
        args += [ "-drive",
                  "file={0},index=0,media=disk".format( self.disk_get_path( "hd-boot" ) ),
                  "-drive",
                  "file={0},index=1,media=disk".format( self.disk_get_path( "hd-root" ) ) ]

        if self.graphics == GRAPHICS_HIDE:
            args += [ "-display", "none" ]

        args += self.extra_args

        self.p = Popen( args )

    def wait(self):
        return self.p.wait()
