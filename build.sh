#!/bin/sh

echo "RPMBUILD SUCKS"
for directory in "SRPMS" "RPMS" "BUILDROOT" "BUILD"; do
	[ ! -e $directory ] && mkdir $directory
done
exec rpmbuild --define "_topdir $PWD" -ba kernel-module-zram.spec
