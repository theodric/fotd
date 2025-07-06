#!/usr/bin/env perl
# fotd_puffs.pl - OpenBSD PUFFS/Perl FUSE fortune filesystem
# USAGE:
#   doas perl fotd_puffs.pl /path/to/mountpoint [fortune_file]
#   cat /path/to/mountpoint/fortune
# N.B. You must create the mountpoint directory first.
#
use strict;
use warnings;
use Fuse qw(:all);
use POSIX qw(ENOENT EISDIR);

my $fortune_file = $ARGV[1];

sub getattr {
    my ($path) = @_;
    if ($path eq '/') {
        return [ 0040755, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0 ];
    } elsif ($path eq '/fortune') {
        # Regular file, size is a dummy value
        return [ 0100644, 0, 1, 0, 0, 0, 4096, 0, 0, 0, 0 ];
    } else {
        return -ENOENT();
    }
}

sub readdir {
    my ($path, $offset) = @_;
    return -ENOENT() unless $path eq '/';
    return ['.', '..', 'fortune'];
}

sub open {
    my ($path, $flags) = @_;
    return -ENOENT() unless $path eq '/fortune';
    return 0;
}

sub read {
    my ($path, $size, $offset) = @_;
    return -ENOENT() unless $path eq '/fortune';
    my $cmd = 'fortune';
    $cmd .= " $fortune_file" if defined $fortune_file;
    my $output = `$cmd`;
    my $data = substr($output, $offset, $size);
    return $data;
}

sub statfs {
    # Return a minimal statfs structure
    # (blocks, bfree, bavail, files, ffree, bsize, namelen, frsize)
    return (1, 1, 1, 1, 1, 4096, 255, 4096);
}

sub destroy {
    # No-op, but required for some FUSE/PUFFS implementations
    return 0;
}

Fuse::main(
    mountpoint => $ARGV[0],
    getattr    => \&getattr,
    readdir    => \&readdir,
    open       => \&open,
    read       => \&read,
    statfs     => \&statfs,
    destroy    => \&destroy,
    threaded   => 0,
); 