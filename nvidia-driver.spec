%global debug_package %{nil}
%global __strip /bin/true

%if 0%{?rhel} == 6
%global _glvnd_libdir   %{_libdir}/libglvnd
%endif

Name:           nvidia-driver
Version:        410.93
Release:        5%{?dist}
Summary:        NVIDIA's proprietary display driver for NVIDIA graphic cards
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64

Source0:        %{name}-%{version}-i386.tar.xz
Source1:        %{name}-%{version}-x86_64.tar.xz
# For servers without OutputClass device options
Source10:       99-nvidia-modules.conf
Source11:       10-nvidia-driver.conf
# For servers with OutputClass device options
Source12:       10-nvidia.conf

Source40:       com.nvidia.driver.metainfo.xml
Source41:       parse-readme.py

Source99:       nvidia-generate-tarballs.sh

%ifarch x86_64

BuildRequires:  python2

%if 0%{?fedora} || 0%{?rhel} >= 8
# AppStream metadata generation
BuildRequires:  libappstream-glib%{?_isa} >= 0.6.3
%endif

%endif

Requires:       nvidia-driver-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}
Requires:       nvidia-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:       libva-vdpau-driver%{?_isa}

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
# X.org "OutputClass"
Requires:       xorg-x11-server-Xorg%{?_isa} >= 1.16
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
# Extended "OutputClass" with device options
Requires:       xorg-x11-server-Xorg%{?_isa} >= 1.19.0-3
# For auto-fallback to nouveau systemd service
%{?systemd_requires}
%endif

Conflicts:      catalyst-x11-drv
Conflicts:      catalyst-x11-drv-legacy
Conflicts:      fglrx-x11-drv
Conflicts:      nvidia-x11-drv
Conflicts:      nvidia-x11-drv-173xx
Conflicts:      nvidia-x11-drv-304xx
Conflicts:      nvidia-x11-drv-340xx
Conflicts:      nvidia-x11-drv-390xx
Conflicts:      xorg-x11-drv-nvidia
Conflicts:      xorg-x11-drv-nvidia-173xx
Conflicts:      xorg-x11-drv-nvidia-304xx
Conflicts:      xorg-x11-drv-nvidia-340xx
Conflicts:      xorg-x11-drv-nvidia-390xx

%description
This package provides the most recent NVIDIA display driver which allows for
hardware accelerated rendering with recent NVIDIA chipsets.

For the full product support list, please consult the release notes for driver
version %{version}.

%package libs
Summary:        Libraries for %{name}
Requires:       egl-wayland
Requires:       libvdpau%{?_isa} >= 0.5
Requires:       libglvnd%{?_isa} >= 1.0
Requires:       libglvnd-egl%{?_isa} >= 1.0
Requires:       libglvnd-gles%{?_isa} >= 1.0
Requires:       libglvnd-glx%{?_isa} >= 1.0
Requires:       libglvnd-opengl%{?_isa} >= 1.0

%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       vulkan-loader
%endif

%if 0%{?rhel} == 7
Requires:       vulkan-filesystem
%endif

Conflicts:      nvidia-x11-drv-libs
Conflicts:      nvidia-x11-drv-libs-96xx
Conflicts:      nvidia-x11-drv-libs-173xx
Conflicts:      nvidia-x11-drv-libs-304xx
Conflicts:      nvidia-x11-drv-libs-340xx
Conflicts:      nvidia-x11-drv-libs-390xx
Conflicts:      xorg-x11-drv-nvidia-gl
Conflicts:      xorg-x11-drv-nvidia-libs
Conflicts:      xorg-x11-drv-nvidia-libs-173xx
Conflicts:      xorg-x11-drv-nvidia-libs-304xx
Conflicts:      xorg-x11-drv-nvidia-libs-340xx
Conflicts:      xorg-x11-drv-nvidia-libs-390xx
%ifarch %{ix86}
Conflicts:      nvidia-x11-drv-32bit
Conflicts:      nvidia-x11-drv-32bit-96xx
Conflicts:      nvidia-x11-drv-32bit-173xx
Conflicts:      nvidia-x11-drv-32bit-304xx
Conflicts:      nvidia-x11-drv-32bit-340xx
Conflicts:      nvidia-x11-drv-32bit-390xx
%endif

%description libs
This package provides the shared libraries for %{name}.

%package cuda-libs
Summary:        Libraries for %{name}-cuda

%description cuda-libs
This package provides the CUDA libraries for %{name}-cuda.

%package NvFBCOpenGL
Summary:        NVIDIA OpenGL-based Framebuffer Capture libraries
# Loads libnvidia-encode.so at runtime
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description NvFBCOpenGL
This library provides a high performance, low latency interface to capture and
optionally encode the composited framebuffer of an X screen. NvFBC and NvIFR are
private APIs that are only available to NVIDIA approved partners for use in
remote graphics scenarios.

%package NVML
Summary:        NVIDIA Management Library (NVML)
Provides:       cuda-nvml%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description NVML
A C-based API for monitoring and managing various states of the NVIDIA GPU
devices. It provides a direct access to the queries and commands exposed via
nvidia-smi. The run-time version of NVML ships with the NVIDIA display driver,
and the SDK provides the appropriate header, stub libraries and sample
applications. Each new version of NVML is backwards compatible and is intended
to be a platform for building 3rd party applications.

%package devel
Summary:        Development files for %{name}
Conflicts:      xorg-x11-drv-nvidia-devel
Conflicts:      xorg-x11-drv-nvidia-devel-173xx
Conflicts:      xorg-x11-drv-nvidia-devel-304xx
Conflicts:      xorg-x11-drv-nvidia-devel-340xx
Conflicts:      xorg-x11-drv-nvidia-devel-390xx
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-NvFBCOpenGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides the development files of the %{name} package.

%ifarch x86_64

%package cuda
Summary:        CUDA integration for %{name}
Conflicts:      xorg-x11-drv-nvidia-cuda
Requires:       nvidia-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}
Requires:       nvidia-persistenced = %{?epoch:%{epoch}:}%{version}
Requires:       opencl-filesystem
Requires:       ocl-icd

%description cuda
This package provides the CUDA integration components for %{name}.

%endif
 
%prep
%ifarch %{ix86}
%setup -q -n %{name}-%{version}-i386
%endif

%ifarch x86_64
%setup -q -T -b 1 -n %{name}-%{version}-x86_64
%endif

# Create symlinks for shared objects
ldconfig -vn .

# Required for building gstreamer 1.0 NVENC plugins
ln -sf libnvidia-encode.so.%{version} libnvidia-encode.so
# Required for building ffmpeg 3.1 Nvidia CUVID
ln -sf libnvcuvid.so.%{version} libnvcuvid.so

# Required for building against CUDA
ln -sf libcuda.so.%{version} libcuda.so
# libglvnd indirect entry point
ln -sf libGLX_nvidia.so.%{version} libGLX_indirect.so.0

%if 0%{?fedora} || 0%{?rhel} >= 7
cat nvidia_icd.json.template | sed -e 's/__NV_VK_ICD__/libGLX_nvidia.so.0/' > nvidia_icd.%{_target_cpu}.json
%else
rm -f libnvidia-glvkspirv.so.%{version}
%endif

%build

%install

mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d/
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d/
mkdir -p %{buildroot}%{_includedir}/nvidia/GL/
mkdir -p %{buildroot}%{_libdir}/vdpau/

%ifarch x86_64

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/nvidia/
mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers/
mkdir -p %{buildroot}%{_libdir}/xorg/modules/extensions/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
mkdir -p %{buildroot}%{_sysconfdir}/nvidia/
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors/

%if 0%{?rhel}
mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d/
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
mkdir -p %{buildroot}%{_datadir}/appdata/
%endif

# OpenCL config
install -p -m 0755 nvidia.icd %{buildroot}%{_sysconfdir}/OpenCL/vendors/

# Binaries
install -p -m 0755 nvidia-{debugdump,smi,cuda-mps-control,cuda-mps-server,bug-report.sh} %{buildroot}%{_bindir}

# Man pages
install -p -m 0644 nvidia-{smi,cuda-mps-control}*.gz %{buildroot}%{_mandir}/man1/

%if 0%{?fedora}
# install AppData and add modalias provides
install -p -m 0644 %{SOURCE40} %{buildroot}%{_datadir}/appdata/
fn=%{buildroot}%{_datadir}/appdata/com.nvidia.driver.metainfo.xml
%{SOURCE41} README.txt "NVIDIA GEFORCE GPUS" | xargs appstream-util add-provide ${fn} modalias
%{SOURCE41} README.txt "NVIDIA QUADRO GPUS" | xargs appstream-util add-provide ${fn} modalias
%{SOURCE41} README.txt "NVIDIA NVS GPUS" | xargs appstream-util add-provide ${fn} modalias
%{SOURCE41} README.txt "NVIDIA TESLA GPUS" | xargs appstream-util add-provide ${fn} modalias
%{SOURCE41} README.txt "NVIDIA GRID GPUS" | xargs appstream-util add-provide ${fn} modalias
%endif

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
install -p -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/99-nvidia-modules.conf
sed -i -e 's|@LIBDIR@|%{_libdir}|g' %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/99-nvidia-modules.conf
install -p -m 0644 %{SOURCE11} %{buildroot}%{_datadir}/X11/xorg.conf.d/10-nvidia-driver.conf
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
sed -i -e 's|@LIBDIR@|%{_libdir}|g' %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%endif

# X stuff
install -p -m 0755 nvidia_drv.so %{buildroot}%{_libdir}/xorg/modules/drivers/
install -p -m 0755 libglxserver_nvidia.so.%{version} %{buildroot}%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

# NVIDIA specific configuration files
install -p -m 0644 nvidia-application-profiles-%{version}-key-documentation \
    %{buildroot}%{_datadir}/nvidia/
install -p -m 0644 nvidia-application-profiles-%{version}-rc \
    %{buildroot}%{_datadir}/nvidia/

%endif

%if 0%{?fedora} || 0%{?rhel} >= 7
# Vulkan and EGL loaders
install -p -m 0644 nvidia_icd.%{_target_cpu}.json %{buildroot}%{_datadir}/vulkan/icd.d/
%endif
install -p -m 0644 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d/

# Unique libraries
cp -a lib*GL*_nvidia.so* libcuda.so* libnv*.so* %{buildroot}%{_libdir}/
cp -a libvdpau_nvidia.so* %{buildroot}%{_libdir}/vdpau/

# libglvnd indirect entry point and private libglvnd libraries
%if 0%{?rhel} == 6
cp -a libGLX_indirect.so* %{buildroot}%{_libdir}/
install -m 0755 -d %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo -e "%{_glvnd_libdir} \n" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/nvidia-%{_target_cpu}.conf
%endif

%ldconfig_scriptlets libs

%ldconfig_scriptlets cuda-libs

%ldconfig_scriptlets NvFBCOpenGL

%ldconfig_scriptlets NVML

%ifarch x86_64

%files
%license LICENSE
%doc NVIDIA_Changelog README.txt html
%dir %{_sysconfdir}/nvidia
%{_bindir}/nvidia-bug-report.sh
%if 0%{?fedora}
%{_datadir}/appdata/com.nvidia.driver.metainfo.xml
%endif
%{_datadir}/nvidia
%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so
%{_libdir}/xorg/modules/drivers/nvidia_drv.so

# X.org configuration files
%if 0%{?rhel} == 6 || 0%{?rhel} == 7
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/99-nvidia-modules.conf
%config(noreplace) %{_datadir}/X11/xorg.conf.d/10-nvidia-driver.conf
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%endif

%files cuda
%{_sysconfdir}/OpenCL/vendors/*
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-cuda-mps-control.1.*
%{_mandir}/man1/nvidia-smi.*

%endif

%files devel
%{_includedir}/nvidia/
%{_libdir}/libnvcuvid.so
%{_libdir}/libnvidia-encode.so

%files libs
%if 0%{?rhel} == 6
%{_sysconfdir}/ld.so.conf.d/nvidia-%{_target_cpu}.conf
%{_libdir}/libGLX_indirect.so.0
%endif
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_datadir}/vulkan/icd.d/nvidia_icd.%{_target_cpu}.json
%endif
%{_libdir}/libEGL_nvidia.so.0
%{_libdir}/libEGL_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1
%{_libdir}/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLX_nvidia.so.0
%{_libdir}/libGLX_nvidia.so.%{version}
%ifarch x86_64
%{_libdir}/libnvidia-cbl.so.%{version}
%{_libdir}/libnvidia-cfg.so.1
%{_libdir}/libnvidia-cfg.so.%{version}
%{_libdir}/libnvidia-rtcore.so.%{version}
%{_libdir}/libnvoptix.so.1
%{_libdir}/libnvoptix.so.%{version}
%endif
%{_libdir}/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-fatbinaryloader.so.%{version}
%{_libdir}/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glsi.so.%{version}
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_libdir}/libnvidia-glvkspirv.so.%{version}
%endif
%{_libdir}/libnvidia-tls.so.%{version}
%{_libdir}/vdpau/libvdpau_nvidia.so.1
%{_libdir}/vdpau/libvdpau_nvidia.so.%{version}

%files cuda-libs
%{_libdir}/libcuda.so
%{_libdir}/libcuda.so.1
%{_libdir}/libcuda.so.%{version}
%{_libdir}/libnvcuvid.so.1
%{_libdir}/libnvcuvid.so.%{version}
%{_libdir}/libnvidia-compiler.so.%{version}
%{_libdir}/libnvidia-encode.so.1
%{_libdir}/libnvidia-encode.so.%{version}
%{_libdir}/libnvidia-opencl.so.1
%{_libdir}/libnvidia-opencl.so.%{version}
%{_libdir}/libnvidia-ptxjitcompiler.so.1
%{_libdir}/libnvidia-ptxjitcompiler.so.%{version}

%files NvFBCOpenGL
%{_libdir}/libnvidia-fbc.so.1
%{_libdir}/libnvidia-fbc.so.%{version}
%{_libdir}/libnvidia-ifr.so.1
%{_libdir}/libnvidia-ifr.so.%{version}

%files NVML
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/libnvidia-ml.so.%{version}

%changelog
* Mon Feb 04 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-5
- Move fatbinaryloader in main libraries subpackage.

* Sun Feb 03 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-5
- Split out all kernel related interactions into the nvidia-kmod-common package.
- Require nvidia-kmod-common in both nvidia-driver and nvidia-driver-cuda as
  they can now be installed separately.

* Sun Feb 03 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-4
- Remove CUDA provides/requires, move them to separate package.

* Sat Feb 02 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-3
- Add nvidia-drivers and cuda-drivers virtual provides as requested by Red Hat.

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-2
- Update requirements.

* Fri Jan 04 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-1
- Update to 410.93.

* Sat Dec 01 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-4
- No more private GLVND libraries on RHEL 7.

* Thu Nov 22 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-3
- Update scripts to always perform updates/removal of boot options.

* Thu Nov 22 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-2
- Remove modesetting again on Fedora.

* Mon Nov 19 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-1
- Update to 410.78.

* Tue Oct 30 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-4
- Disable modesetting on Fedora < 29.

* Sat Oct 27 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-3
- Revert grubby invocation on RHEL/CentOS 6.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-2
- Update post scriptlets to make sure new parameters are added correctly.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-1
- Update to 410.73.
- Enable modesetting and remove ignoreabi setting for Fedora.
- Update conditionals for RHEL/CentOS.
- Add additional conflicting packages.
- Bump GLVND requirements.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-2
- Do not enable Vulkan components on RHEL/CentOS 6.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-1
- Update to 410.66.
- Enable modeset for RHEL/CentOS 7 (7.6).

* Thu Sep 06 2018 Simone Caronni <negativo17@gmail.com> - 3:390.87-1
- Update to 390.87.

* Tue Jul 17 2018 Simone Caronni <negativo17@gmail.com> - 3:390.77-1
- Update to 390.77.

* Mon Jun 11 2018 Simone Caronni <negativo17@gmail.com> - 3:390.67-1
- Update to 390.67.

* Sat Jun 02 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-2
- Fix Vulkan ownership of files.
- Update conditionals for distributions.

* Tue May 22 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-1
- Update to 390.59.

* Tue Apr 03 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-1
- Update to 390.48.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-1
- Update to 390.42.

* Tue Feb 27 2018 Simone Caronni <negativo17@gmail.com> - 3:390.25-4
- Update Epoch so packages do not overlap with RPMFusion.

* Tue Feb 27 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-3
- Require libnvidia-ml.so in nvidia-driver-devel package.

* Fri Feb 02 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-2
- Fix omitting drivers from the initrd.

* Tue Jan 30 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-1
- Update to 390.25.

* Thu Jan 11 2018 Simone Caronni <negativo17@gmail.com> - 2:384.111-1
- Update to 384.111.

* Fri Nov 17 2017 Simone Caronni <negativo17@gmail.com> - 2:384.98-2
- Revert modeset by default for Fedora 27.

* Tue Nov 14 2017 Simone Caronni <negativo17@gmail.com> - 2:384.98-1
- Update to 384.98.

* Fri Sep 22 2017 Simone Caronni <negativo17@gmail.com> - 2:384.90-1
- Update to 384.90.

* Wed Aug 30 2017 Simone Caronni <negativo17@gmail.com> - 2:384.69-1
- Update to 384.69.

* Tue Aug 29 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-6
- Make the major number of Nvidia devices dynamic again:
  https://github.com/negativo17/nvidia-driver/issues/29
- Enable modeset by default for Fedora 27.

* Sun Aug 27 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-5
- Re-add udev rules to create device files with SELinux context (thanks Leigh).

* Wed Aug 16 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-4
- Momentarily revert udev rules installation for basic devices.

* Tue Aug 15 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-3
- Add udev rules to always create device nodes:
  https://github.com/negativo17/nvidia-driver/issues/27

* Tue Aug 08 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-2
- Remove spurious dependency on main driver for libraries.

* Tue Jul 25 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-1
- Update to 384.59.
- Use system wide default directory for Vulkan ICD loaders.
- Use _target_cpu in place of _lib where appropriate.
- Add nvidia-fallback.service which automatically fallsback to nouveau if the
  nvidia driver fails to load for some reason (F25+ only).
- Remove nouveau.modeset=0 from kernel cmdline arguments for Fedora 25+, as this
  breaks fallback to nouveau when nvidia.ko fails to load for some reason.
- Thanks to Hans de Goede <jwrdegoede@fedoraproject.org> for patches.

* Wed May 17 2017 Simone Caronni <negativo17@gmail.com> - 2:375.66-3
- Do not obsolete/provide packages from other repositories, instead conflict
  with them.

* Fri May 12 2017 Hans de Goede <jwrdegoede@fedoraproject.org> - 2:375.66-2
- Add dracut.conf.d/99-nvidia.conf file enforcing that the nvidia modules never
  get added to the initramfs (doing so would break things on a driver update)

* Wed May 10 2017 Simone Caronni <negativo17@gmail.com> - 2:375.66-1
- Update to 375.66.

* Wed Apr 19 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-7
- Update RHEL/CentOS 6 packages to use OutputClass as in RHEL/CentOS 7 (since
  RHEL 6.8 it's using X.org server 1.17+).

* Tue Apr 04 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-6
- Use private libglvnd libraries for RHEL 6/7 and Fedora 24.

* Wed Mar 29 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-5
- Use EPEL OpenCL loader also on RHEL/CentOS 7.
- Clean up the EGL Wayland provider installation.

* Tue Mar 21 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-4
- Install libGLX_indirect.so.0 only on Fedora 24 and RHEL 6/7.

* Wed Mar 01 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-3
- Add nvidia-uvm-tools device creation to CUDA subpackage.

* Tue Feb 21 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-2
- Install the OpenCL loader only on RHEL < 7 and in the system path.

* Wed Feb 15 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-1
- Update to 375.39.

* Tue Jan 10 2017 Simone Caronni <negativo17@gmail.com> - 2:375.26-4
- Enable SLI and BaseMosaic (SLI multimonitor) by default.

* Wed Dec 21 2016 Simone Caronni <negativo17@gmail.com> - 2:375.26-3
- Do not enable nvidia-drm modeset by default yet.
- Adjust removal of obsolete kernel command line options for RHEL 6.
- Update OutputClass configuration for Intel/Optimus systems.

* Tue Dec 20 2016 Simone Caronni <negativo17@gmail.com> - 2:375.26-2
- Add configuration options for new OutputClass Device integration on Fedora 25
  with X server 1.19.0-3 (new 10-nvidia.conf configuration file).
- Trim changelog.
- Remove support for Fedora 23.
- Remove no longer needed kernel command line options.
- Enable modeset by default for the nvidia-drm module.

* Thu Dec 15 2016 Simone Caronni <negativo17@gmail.com> - 2:375.26-1
- Update to 375.26.

* Fri Dec 02 2016 Simone Caronni <negativo17@gmail.com> - 2:375.20-2
- Remove library location override from the libs subpackage.

* Sat Nov 19 2016 Simone Caronni <negativo17@gmail.com> - 2:375.20-1
- Update to 375.20.
- Add IgnoreABI only on Fedora 26+.
- Remove releases from AppStream metadata file (can't track between various
  beta, short lived, long lived releases).
- Enable libglvnd 0.2.x based EGL.
- Update requirements on improved libglvnd package.
- Obsoletes/Provides cuda-drivers, as introduced in CUDA 8.0 packages.
- Require vulkan-filesystem on Fedora.
- Enable filtering by pci id in the AppStream metadata.
- Make the whole AppStream generation available only on Fedora 25+.
- Do not require nvidia-settings, make it possible to install without the GUI.
- Add modaliases to the MetaInfo file to only match supported NVIDIA hardware.
- Install an MetaInfo so the driver appears in the software center.

* Mon Oct 24 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-4
- Add missing libglvnd library dependency.

* Fri Oct 21 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-3
- Update requirements on improved libglvnd package.

* Fri Oct 14 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-2
- Obsoletes/Provides cuda-drivers, as introduced in CUDA 8.0 packages.

* Mon Oct 10 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-1
- Update to 367.57.

* Sun Oct 09 2016 Simone Caronni <negativo17@gmail.com> - 2:367.44-2
- Require vulkan-filesystem on Fedora.

* Thu Aug 25 2016 Simone Caronni <negativo17@gmail.com> - 2:367.44-1
- Update to 367.44.

* Sat Aug 13 2016 Simone Caronni <negativo17@gmail.com> - 2:367.35-2
- Move IgnoreABI directive to Fedora 26+.

* Fri Jul 22 2016 Simone Caronni <negativo17@gmail.com> - 2:367.35-1
- Update to 367.35.

* Thu Jul 14 2016 Simone Caronni <negativo17@gmail.com> - 2:367.27-3
- Add unversioned CUVID library to devel subpackage for building FFMPeg 3.1
  CUVID support.

* Tue Jun 21 2016 Simone Caronni <negativo17@gmail.com> - 2:367.27-2
- Add missing dependency on CUDA libs for CUDA driver components. The automatic
  one went missing with libraries reorganization.

* Mon Jun 13 2016 Simone Caronni <negativo17@gmail.com> - 2:367.27-1
- Update to 367.27.
- Disable modeset by default. There is no fb driver and the only consumer is a
  custom build of Wayland with rejected patches.
- Add Vulkan and DRM KMS support.
- Do not require vulkan-filesystem (yet):
  https://copr.fedorainfracloud.org/coprs/ajax/vulkan/
- Update description.
- Add new symlink libGLX_indirect.so.0.
- Add libnvidia-egl-wayland.so to the library subpackage only on Fedora systems.

* Thu Jun 09 2016 Simone Caronni <negativo17@gmail.com> - 2:361.45.11-2
- Add unversioned libnvidia-encode shared object to devel subpackage; required
  to build the Gstreamer NVENC plugin.

* Fri May 27 2016 Simone Caronni <negativo17@gmail.com> - 2:361.45.11-1
- Update to 361.45.11, use libglvnd libraries for everything except EGL.
- Load nvidia-uvm.ko through a soft dependency on nvidia.ko. This avoids
  inserting the nvidia-uvm configuration file in the initrd. Since the module
  is not (and should not be) in the initrd, this prevents the (harmless) module
  loading error in Plymouth.
- Requires libglvnd >= 0.1.0.

* Wed Mar 30 2016 Simone Caronni <negativo17@gmail.com> - 2:361.42-1
- Update to 361.42, add libglvnd requirement.
- Use non-libglvnd libGL as per default Nvidia installation, some Steam games
  check for non-abi stuff in libGL.
- Remove ARM (Carma, Kayla) support.
- Use new X.org OutputClass loader for RHEL 7 (X.org 1.16+, RHEL 7.2+).
- Update isa requirements.

* Tue Jan 26 2016 Simone Caronni <negativo17@gmail.com> - 2:352.79-1
- Update to 352.79.

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 2:352.63-1
- Update to 352.63.

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 2:352.55-2
- Add kernel command line also to Grub default files for grub2-mkconfig
  consumption.
- Create new macro for grubby command in post
- Remove support for Grub 0.97 in Fedora or CentOS/RHEL 7.
- Ignore ABI configuration file moved to Fedora 24+ (driver
  supports video driver ABI 20).
- Update modprobe configuration file position in CentOS/RHEL 6.
- Update isa requirements.

* Tue Oct 20 2015 Simone Caronni <negativo17@gmail.com> - 2:352.55-1
- Update to 352.55.

* Fri Aug 28 2015 Simone Caronni <negativo17@gmail.com> - 2:352.41-1
- Update to 352.41.

* Sat Aug 22 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-3
- Re-add nvidia-driver-libs requirement mistakenly removed in latest
  reorganization.

* Fri Aug 14 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-2
- Remove Fedora 20 checks now that is EOL.
- Fix NvFBCOpenGL requirements.
- Split out NVML in its own subpackage, so trying to build against it does not
  install the whole CUDA stack with modules.
- Move all libraries that do not replace system libraries in the default
  directories. There is no reason to keep them separate and this helps for
  building programs that link to these libraries (like nvidia-settings on NVML)
  and for writing out filters in the SPEC file.
- Build requires execstack in place of prelink on Fedora 23+.
- Rework completely symlink creation using ldconfig, remove useless symlink and
  trim devel subpackage.

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-1
- Update to 352.30.

* Wed Jun 17 2015 Simone Caronni <negativo17@gmail.com> - 2:352.21-1
- Update to 352.21.

* Mon Jun 08 2015 Simone Caronni <negativo17@gmail.com> - 2:352.09-2
- Ignore ABI configuration file moved to Fedora 23+.

* Tue May 19 2015 Simone Caronni <negativo17@gmail.com> - 2:352.09-1
- Update to 352.09.

* Wed May 13 2015 Simone Caronni <negativo17@gmail.com> - 2:346.72-1
- Update to 346.72.

* Mon Apr 27 2015 Simone Caronni <negativo17@gmail.com> - 2:346.59-2
- Load nvidia-uvm when installing nvidia-driver-cuda.

* Tue Apr 07 2015 Simone Caronni <negativo17@gmail.com> - 2:346.59-1
- Update to 346.59.

* Wed Feb 25 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-1
- Update to 346.47.
- Add license macro.

* Thu Jan 29 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-3
- Fix grubby command line.

* Wed Jan 28 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-2
- Update kernel parameters on all installed kernels, not just current. This
  solves issues when updating kernel, not rebooting, and installing the driver
  afterwards.

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-1
- Update to 346.35.

* Mon Jan 12 2015 Simone Caronni <negativo17@gmail.com> - 2:346.22-2
- RHEL/CentOS 7 does not have OpenCL packages (thanks stj).
