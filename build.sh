#!/bin/sh

echo "RPMBUILD SUCKS"
exec rpmbuild --define "_topdir $PWD" -ba kernel-module-zram.spec
