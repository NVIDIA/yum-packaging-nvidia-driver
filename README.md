# yum packaging nvidia driver

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Contributing](https://img.shields.io/badge/Contributing-Developer%20Certificate%20of%20Origin-violet)](https://developercertificate.org)

## Overview

Packaging templates for `yum` and `dnf` based Linux distros to build NVIDIA driver packages.

The `main` branch contains this README. The `.spec`, `.conf`, and `.sh` files can be found in the appropriate [rhel7](../../tree/rhel7), [rhel8](../../tree/rhel8), and [fedora](../../tree/fedora) branches.

## Table of Contents

- [Overview](#Overview)
- [Deliverables](#Deliverables)
- [Packaging Guide](#Packaging-Guide)
- [Demo](#Demo)
- [Prerequisites](#Prerequisites)
  * [Clone this git repository](#Clone-this-git-repository)
  * [Install build dependencies](#Install-build-dependencies)
- [Building with script](#Building-with-script)
- [Building Manually](#Building-Manually)
- [Related](#Related)
  * [DKMS nvidia](#DKMS-nvidia)
  * [NVIDIA kmod common](#NVIDIA-kmod-common)
  * [NVIDIA modprobe](#NVIDIA-modprobe)
  * [NVIDIA persistenced](#NVIDIA-persistenced)
  * [NVIDIA plugin](#NVIDIA-plugin)
  * [NVIDIA precompiled kmod](#NVIDIA-precompiled-kmod)
  * [NVIDIA settings](#NVIDIA-settings)
  * [NVIDIA xconfig](#NVIDIA-xconfig)
- [See also](#See-also)
  * [Ubuntu driver](#Ubuntu-driver)
  * [SUSE driver](#SUSE-driver)
- [Contributing](#Contributing)


## Deliverables

This repo contains the `.spec` file used to build the following **RPM** packages:


> _note:_ `XXX` is the first `.` delimited field in the driver version, ex: `460` in `460.32.03`

* **RHEL8** or **Fedora** streams: `XXX`, `XXX-dkms`, `latest`, and `latest-dkms`
 ```shell
 - nvidia-driver
 - nvidia-driver-cuda
 - nvidia-driver-cuda-libs
 - nvidia-driver-devel
 - nvidia-driver-libs
 - nvidia-driver-NvFBCOpenGL
 - nvidia-driver-NVML
 ```


For RHEL7 and derivatives, there are three sets of packages with different package dependencies.

The `latest` and `latest-dkms` flavors always update to the highest versioned driver, while the `branch-XXX` flavor locks driver updates to the specified driver branch.

* **RHEL7** flavor: `latest-dkms`
 ```shell
 - nvidia-driver-latest-dkms
 - nvidia-driver-latest-dkms-cuda
 - nvidia-driver-latest-dkms-cuda-libs
 - nvidia-driver-latest-dkms-devel
 - nvidia-driver-latest-dkms-libs
 - nvidia-driver-latest-dkms-NvFBCOpenGL
 - nvidia-driver-latest-dkms-NVML
 ```


> *note:* `XXX-dkms` is not supported for RHEL7


To use the precompiled flavors `latest` and `branch-XXX`, use [yum-packaging-precompiled-kmod](https://github.com/NVIDIA/yum-packaging-precompiled-kmod) to build `kmod-nvidia-latest` or `kmod-nvidia-branch-XXX` kernel modules for a specific kernel and driver combination.

* **RHEL7** flavor: `latest`
 ```shell
 - nvidia-driver-latest
 - nvidia-driver-latest-cuda
 - nvidia-driver-latest-cuda-libs
 - nvidia-driver-latest-devel
 - nvidia-driver-latest-libs
 - nvidia-driver-latest-NvFBCOpenGL
 - nvidia-driver-latest-NVML
 ```


* **RHEL7** flavor: `branch-XXX`
 ```shell
 - nvidia-driver-branch-XXX
 - nvidia-driver-branch-XXX-cuda
 - nvidia-driver-branch-XXX-cuda-libs
 - nvidia-driver-branch-XXX-devel
 - nvidia-driver-branch-XXX-libs
 - nvidia-driver-branch-XXX-NvFBCOpenGL
 - nvidia-driver-branch-XXX-NVML
 ```


## Packaging Guide

> _note:_ this guide covers building all of the `yum-packaging` NVIDIA driver packages. To build only the deliverables in this repository, see [Prerequisites](#Prerequisites) and [Building Manually](#Building-Manually) sections.

### RHEL7-derivatives

- [Markdown](docs/guide-rhel7.md) :page_facing_up:
- [HTML](https://developer.download.nvidia.com/compute/github-demos/yum-packaging-nvidia-driver/guide-rhel7/) :notebook:
- [PDF](https://developer.download.nvidia.com/compute/github-demos/yum-packaging-nvidia-driver/guide-rhel7.pdf) :book:


### RHEL8 and Fedora-derivatives

- Coming soon

## Demo

![Demo](http://developer.download.nvidia.com/compute/github-demos/yum-packaging-nvidia-driver/demo.gif)

[![asciinema](https://img.shields.io/badge/Play%20Video-asciinema-red)](http://developer.download.nvidia.com/compute/github-demos/yum-packaging-nvidia-driver/demo-ascii/)   [![gist](https://img.shields.io/badge/Auto%20TTY-gist-green)](https://gist.github.com/kmittman/087100eeda3705691ffb768dddf085b5)


## Prerequisites

### Clone this git repository:

Supported branches: `rhel7`, `rhel8` & `fedora`

```shell
git clone -b ${branch} https://github.com/NVIDIA/yum-packaging-nvidia-driver
> ex: git clone -b rhel8 https://github.com/NVIDIA/yum-packaging-nvidia-driver
```

### Install build dependencies

```shell
# Misc
yum install libappstream-glib
# Packaging
yum install rpm-build
```


## Building with script

### Fetch script from `main` branch

```shell
cd yum-packaging-nvidia-driver
git checkout remotes/origin/main -- build.sh
```

### Usage
> _note:_ distro is `fedora33`, `rhel7`, `rhel8`

```shell
./build.sh path/to/*.run ${distro}
> ex: time ./build.sh ~/Downloads/NVIDIA-Linux-x86_64-460.32.03.run rhel7
```


## Building Manually

### Generate tarballs from runfile

```shell
version="460.32.03"
export RUN_FILE="/path/to/NVIDIA-Linux-${arch}-${version}.run"
export VERSION="$version"
rm -rf temp
nvidia-generate-tarballs-${arch}.sh
ls *.tar.xz
> nvidia-driver-${version}-${arch}.tar.xz  # x86_64 script does not have -${arch} suffix
> nvidia-driver-${version}-i386.tar.xz     # 32-bit libraries for x86_64 only
> nvidia-kmod-${version}-${arch}.tar.xz    # not used here
```

### Packaging (`dnf` distros)
> note: `fedora` & `rhel8`-based distros

```shell
mkdir BUILD BUILDROOT RPMS SRPMS SOURCES SPECS
cp *.conf SOURCES/
cp nvidia-driver-${version}-${arch}.tar.xz SOURCES/
cp nvidia-driver.spec SPECS/

rpmbuild \
    --define "%_topdir $(pwd)" \
    --define "debug_package %{nil}" \
    --define "version $version" \
    --define "epoch 3" \
    --target "${arch}" \
    -v -bb SPECS/nvidia-driver.spec
```

### Packaging (`yum` distros)
> note: `rhel7`-based distros

```shell
mkdir BUILD BUILDROOT RPMS SRPMS SOURCES SPECS
cp *.rules SOURCES/
cp *.conf SOURCES/
cp nvidia-driver-${version}-${arch}.tar.xz SOURCES/
cp nvidia-driver.spec SPECS/

# latest-dkms
rpmbuild \
    --define "%_topdir $(pwd)" \
    --define "debug_package %{nil}" \
    --define "version $version" \
    --define "driver_branch latest-dkms" \
    --define "is_dkms 1" \
    --define "is_latest 1" \
    --define "epoch 3" \
    --target "${arch}" \
    -v -bb SPECS/nvidia-driver.spec

# latest
rpmbuild \
    --define "%_topdir $(pwd)" \
    --define "debug_package %{nil}" \
    --define "version $version" \
    --define "driver_branch latest" \
    --define "is_dkms 0" \
    --define "is_latest 1" \
    --define "epoch 3" \
    --target "${arch}" \
    -v -bb SPECS/nvidia-driver.spec

# branch-460
rpmbuild \
    --define "%_topdir $(pwd)" \
    --define "debug_package %{nil}" \
    --define "version $version" \
    --define "driver_branch branch-460" \
    --define "is_dkms 0" \
    --define "is_latest 0" \
    --define "epoch 3" \
    --target "${arch}" \
    -v -bb SPECS/nvidia-driver.spec
```


## Related

### DKMS nvidia

- dkms-nvidia
  * [https://github.com/NVIDIA/yum-packaging-dkms-nvidia](https://github.com/NVIDIA/yum-packaging-dkms-nvidia)

### NVIDIA kmod common

- Common files
  * [https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common](https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common)

### NVIDIA modprobe

- nvidia-modprobe
  * [https://github.com/NVIDIA/yum-packaging-nvidia-modprobe](https://github.com/NVIDIA/yum-packaging-nvidia-modprobe)

### NVIDIA persistenced

- nvidia-persistenced
  * [https://github.com/NVIDIA/yum-packaging-nvidia-persistenced](https://github.com/NVIDIA/yum-packaging-nvidia-persistenced)

### NVIDIA plugin

- _dnf-plugin-nvidia_ & _yum-plugin-nvidia_
  * [https://github.com/NVIDIA/yum-packaging-nvidia-plugin](https://github.com/NVIDIA/yum-packaging-nvidia-plugin)

### NVIDIA precompiled kmod

- Precompiled kernel modules
  * [https://github.com/NVIDIA/yum-packaging-precompiled-kmod](https://github.com/NVIDIA/yum-packaging-precompiled-kmod)

### NVIDIA settings

- nvidia-settings
  * [https://github.com/NVIDIA/yum-packaging-nvidia-settings](https://github.com/NVIDIA/yum-packaging-nvidia-settings)

### NVIDIA xconfig

- nvidia-xconfig
  * [https://github.com/NVIDIA/yum-packaging-nvidia-xconfig](https://github.com/NVIDIA/yum-packaging-nvidia-xconfig)


## See also

- negativo17
  * [https://github.com/negativo17/nvidia-driver](https://github.com/negativo17/nvidia-driver)

### Ubuntu driver

  * [https://github.com/NVIDIA/ubuntu-packaging-nvidia-driver](https://github.com/NVIDIA/ubuntu-packaging-nvidia-driver)

### SUSE driver

  * [https://github.com/NVIDIA/zypper-packaging-nvidia-driver](https://github.com/NVIDIA/zypper-packaging-nvidia-driver)


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
