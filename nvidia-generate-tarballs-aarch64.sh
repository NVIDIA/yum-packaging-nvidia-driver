#!/bin/sh
set -e

VERSION=${VERSION:-390.42}
DL_SITE=${DL_SITE:-http://us.download.nvidia.com/XFree86}
TEMP_UNPACK=${TEMP_UNPACK:-temp}

ARCH=${ARCH:-aarch64}
PLATFORM=${PLATFORM:-Linux-${ARCH}}
RUN_FILE=${RUN_FILE:-NVIDIA-${PLATFORM}-${VERSION}.run}

get_run_file() {
    printf "Downloading installer for ${VERSION} ${ARCH}... "
    [[ -f $RUN_FILE ]] || wget -c -q ${DL_SITE}/${PLATFORM}/${VERSION}/$RUN_FILE
    printf "OK\n"
}

extract_run_file() {
    sh ${RUN_FILE} --extract-only --target ${TEMP_UNPACK}
}

create_tarball() {
    printf "Creating tarballs for ${VERSION} ${ARCH}... "

    KMOD_OPEN=nvidia-open-kmod-${VERSION}-${ARCH}
    KMOD_LEGACY=nvidia-kmod-${VERSION}-${ARCH}
    DRIVER=nvidia-driver-${VERSION}-${ARCH}
    mkdir ${KMOD_OPEN} ${KMOD_LEGACY} ${DRIVER}

    cd ${TEMP_UNPACK}

    # Compiled from source
    rm -f \
        nvidia-xconfig* \
        nvidia-persistenced* \
        nvidia-modprobe* \
        libnvidia-gtk* nvidia-settings* \
        libGLESv1_CM.so.* libGLESv2.so.* libGL.la libGLdispatch.so.* libOpenGL.so.* libGLX.so.* libGL.so.1* libEGL.so.1* \
        libnvidia-egl-wayland.so.* \
        libnvidia-egl-gbm.so.* \
        libnvidia-vulkan-producer.so.* \
        libOpenCL.so.1*

    # Non GLVND libraries
    rm -f libGL.so.${VERSION} libEGL.so.${VERSION}

    # Useless with packages
    rm -f nvidia-installer* .manifest make* mk* tls_test*

    # useless on modern distributions
    rm -f libnvidia-wfb*

    if [[ -d "kernel-open" ]]; then
        mv kernel-open ../${KMOD_OPEN}/
    else
        rmdir ../${KMOD_OPEN}/
    fi

    mv kernel ../${KMOD_LEGACY}/
    mv * ../${DRIVER}/

    cd ..
    rm -fr ${TEMP_UNPACK}

    [[ -d ${KMOD_OPEN} ]] &&
    tar --remove-files -cJf ${KMOD_OPEN}.tar.xz ${KMOD_OPEN}
    tar --remove-files -cJf ${KMOD_LEGACY}.tar.xz ${KMOD_LEGACY}
    tar --remove-files -cJf ${DRIVER}.tar.xz ${DRIVER}

    printf "OK\n"
}

get_run_file
extract_run_file
create_tarball
