It is very useful to be able to have a clone of the Student Robotics server for development purposes.
This repo allows just that, using puppet to create a VM that closesly matches the main server.

This automagically installs Fedora into a VM, and then applies a puppet config to it.

Here are some approximate instructions on how to use it:

    git clone --recursive git://srobo.org/~rspanton/server.git
    cd server
    ./install
    # follow instructions if it provides any
    # (likely you'll need to install some dependencies)
    ./dsets new puppet
    ./run-vm --save-changes --disk-set puppet

    # wait for that to boot, then in another shell:
    git clone git://srobo.org/~rspanton/server-dummy-secrets.git secrets
    ./config
    # then wait some time for that to finish
    # (takes ~10 minutes on my laptop)

Then point your browser at https://localhost:10443 and accept the self-signed certificate etc.
You can shell into that machine on port 10022 as root with password 123456.

The secrets repository, contains secrets like HTTPS certificates, mysql passwords, etc.
The "dummy-secrets" repository is of the same format as secrets, but is public and for development purposes.

This is still a work-in-progress -- the firewall, srweb, anonymous git, and trac are configured.
Coming soon are:

* ldap
* gerrit
* the IDE
* phpbb

The best thing about this situation is that it is now possible to accept patches against the server configuration.
If you would like to get involved, let us know, generate patches, etc.
