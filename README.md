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
