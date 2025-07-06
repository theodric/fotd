#!/usr/bin/env python3
# theodric 20250706
# USAGE:
# (as root) ./thisfile /path/to/desired/mountpoint /path/to/desired/fortune/file
# cat /path/to/desired/mountpoint/fortune
# N.B. you need to actually create the mountpoint directory before you can use it
# 
import os
from fuse import FUSE, Operations, FuseOSError
import errno

class FotdFS(Operations):
    def __init__(self, fortune_file=None):
        self.fortune_file = fortune_file

    def getattr(self, path, fh=None):
        print(f"[DEBUG] getattr called on {path}")
        if path == '/':
            return dict(st_mode=(0o40755), st_nlink=2)
        elif path == '/fortune':
            # Set st_size to a dummy value (e.g., 4096)
            return dict(st_mode=(0o100644), st_nlink=1, st_size=4096)
        else:
            raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        print(f"[DEBUG] readdir called on {path}")
        return ['.', '..', 'fortune']

    def read(self, path, size, offset, fh):
        print(f"[DEBUG] read called on {path} (fortune_file={self.fortune_file}) size={size} offset={offset}")
        if path != '/fortune':
            raise FuseOSError(errno.ENOENT)
        cmd = ['fortune']
        if self.fortune_file:
            cmd.append(self.fortune_file)
        print(f"[DEBUG] Running command: {' '.join(cmd)}")
        output = os.popen(' '.join(cmd)).read()
        print(f"[DEBUG] Output: {output[:60]}{'...' if len(output) > 60 else ''}")
        return output.encode('utf-8')[offset:offset+size]

    def write(self, path, data, offset, fh):
        print(f"[DEBUG] write called on {path} with data: {data}")
        if path != '/fortune':
            raise FuseOSError(errno.ENOENT)
        self.fortune_file = data.decode('utf-8').strip()
        print(f"[DEBUG] fortune_file set to: {self.fortune_file}")
        return len(data)

    def truncate(self, path, length):
        pass

    def open(self, path, flags):
        print(f"[DEBUG] open called on {path} with flags {flags}")
        return 0

    def create(self, path, mode, fi=None):
        print(f"[DEBUG] create called on {path} with mode {mode}")
        return 0

    def access(self, path, mode):
        print(f"[DEBUG] access called on {path} with mode {mode}")
        if path in ('/', '/fortune'):
            return 0
        raise FuseOSError(errno.ENOENT)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('usage: {} <mountpoint> [fortune_file]'.format(sys.argv[0]))
        exit(1)
    mountpoint = sys.argv[1]
    fortune_file = sys.argv[2] if len(sys.argv) == 3 else None
    FUSE(FotdFS(fortune_file), mountpoint, foreground=True, allow_other=True)
