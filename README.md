# yum packaging nvidia driver

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Contributing](https://img.shields.io/badge/Contributing-Developer%20Certificate%20of%20Origin-violet)](https://developercertificate.org)

## Overview

Packaging templates for `yum` and `dnf` based Linux distros to build NVIDIA driver packages.

The `main` branch contains this README. The `.spec`, `.conf`, and `.sh` files can be found in the appropriate [rhel7](../../tree/rhel7), [rhel8](../../tree/rhel8), and [fedora](../../tree/fedora) branches.

## Table of Contents

- [Overview](#Overview)
- [Deliverables](#Deliverables)
- [Prerequisites](#Prerequisites)
  * [Clone this git repository](#Clone-this-git-repository)
  * [Install build dependencies](#Install-build-dependencies)
- [Related](#Other-NVIDIA-driver-packages)
  * [DKMS nvidia](#DKMS-nvidia)
  * [NVIDIA kmod common](#NVIDIA-kmod-common)
  * [NVIDIA modprobe](#NVIDIA-modprobe)
  * [NVIDIA persistenced](#NVIDIA-persistenced)
  * [NVIDIA plugin](#NVIDIA-plugin)
  * [NVIDIA precompiled kmod](#NVIDIA-precompiled-kmod)
  * [NVIDIA settings](#NVIDIA-settings)
  * [NVIDIA xconfig](#NVIDIA-xconfig)
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


## Prerequisites

### Clone this git repository:

Supported branches: `rhel7`, `rhel8` & `fedora`

```shell
git clone -b ${branch} https://github.com/NVIDIA/yum-packaging-nvidia-driver
> ex: git clone -b rhel8 https://github.com/NVIDIA/yum-packaging-nvidia-driver
```

### Install build dependencies

```shell
# Packaging
yum install rpm-build
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


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
