Name:          kernel-module-zram-jolla
Version:       3.4.91.20140612.1
Summary:       zRAM for Jolla Kernel %{version}
Release:       2
License:       GPLv2+
Group:         System Environment/Kernel

# Sources
# sailfishos_kernel_jolla_msm8930-%{version}.tar.bz2 is the result of
# 'git archive master | bzip2' against the HEAD of
# https://github.com/KonstaT/sailfishos_kernel_jolla_msm8930
Source0:       sailfishos_kernel_jolla_msm8930-%{version}.tar.bz2
Source1:       config-%{version}
Source2:       Module.symvers-%{version}

Patch0:        zsmalloc_remove_x86_dependency.patch
Patch1:        zram_switch_kconfig_dependency.patch
Patch2:        zram_fix_32bit_overflow.patch
Patch3:        zram_finish_fix_32bit_overflow.patch

%description
zRAM (formerly compcache) is a module of the Linux kernel that permits
the creation of compressed swap devices directly into the RAM.

This package contains only the zram and zsmalloc modules. You'll need
to configure the modules manually or use tools like zramcfg.

### PREP
%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -p %SOURCE1 ./.config
cp -p %SOURCE2 ./Module.symvers

### BUILD
%build
echo "CONFIG_ZSMALLOC=m" >> .config
echo "CONFIG_ZRAM=m" >> .config

make oldnoconfig
make prepare
make modules_prepare

make SUBDIRS=drivers/staging/zsmalloc modules
# UGLY
cat drivers/staging/zsmalloc/Module.symvers >> Module.symvers

make SUBDIRS=drivers/staging/zram modules

### INSTALL
%install
make SUBDIRS=drivers/staging/zram modules_install INSTALL_MOD_PATH=%{buildroot}
make SUBDIRS=drivers/staging/zsmalloc modules_install INSTALL_MOD_PATH=%{buildroot}

### FILES
%files
%defattr(-,root,root,-)
/lib

### POST AND POSTUN (depmod)
%post -p /sbin/depmod
%postun -p /sbin/depmod
