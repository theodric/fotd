# fotd
FOTD - Fortune Of The Day
Creates a special file with FUSE which calls 'fortune' on a specific fortune file, allowing you to cause /etc/motd to print random fortunes.

## Installation
PREREQUISITES:  
On the Python side, you'll need fusepy (however you want to get that - either from your distro's repos or via pip).  
On the OS side, you'll also need to install the `fortune` binary as well as some fortunes - however your OS/distro decides to handle that.  

## Usage
(as `root`):
```bash
./fotd_fuse.py /path/to/desired/mountpoint /path/to/desired/fortune/file
```
THEN  

```bash
cat /path/to/desired/mountpoint/fortune
```
will print a random fortune from the fortune file you specified as a mount argument.  

The idea here is that you set this up to run at boot and symlink /path/to/desired/mountpoint/fortune to /etc/motd, which will cause anything that prints the MOTD to grab a random fortune instead.

## Service
~Can try putting it into /etc/fstab~
~```/path/to/fotd_fuse.py /mnt/fortune fuse.python3,noauto,x-systemd.automount,_netdev,allow_other 0 0```~

~Otherwise, ~
try the fotd-fuse.service file (but edit it to reflect your system configuration)
The one provided work with openSUSE Tumbleweed as of 2025-07-06 and defaults to Zippy fortunes

1. Put the service file in /etc/systemd/system
2. mkdir /wherever/you/decided/
3. Edit the service file your paths
4. ```sudo systemctl daemon-reload```
5. ```sudo systemctl enable --now fotd-fuse.service```


## Stuff
The Perl version is targeted at OpenBSD, but is not working because Perl's FUSE module doesn't build properly.
