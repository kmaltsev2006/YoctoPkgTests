#!/bin/bash

# Exit on error
set -e

print_usage() {
    echo "Usage: $0 [-d] -i IMAGE_NAME"
}

DAEMONIZE='false'
IMAGE_NAME=''

while getopts 'di:' FLAG; do
    case "${FLAG}" in
        d) DAEMONIZE='true' ;;
        i) IMAGE_NAME="${OPTARG}" ;;
        *) print_usage; exit 1 ;;
    esac
done

# Check if IMAGE_NAME is setted
if [ -z "$IMAGE_NAME" ]; then
    print_usage
    exit 1
fi

# Copy image in /var/lib/yocto-built-images for running
cp -r /var/yocto/built-images/${IMAGE_NAME} /var/lib/yocto-built-images

if [ "$DAEMONIZE" == 'true' ]; then
    sudo qemu-system-x86_64 \
        -cpu IvyBridge \
        -smp 4 \
        -m 512 \
        -kernel /var/lib/yocto-built-images/${IMAGE_NAME}/bzImage \
        -drive file=/var/lib/yocto-built-images/${IMAGE_NAME}/core-image-minimal-qemux86-64.rootfs.ext4,if=virtio,format=raw \
        -object rng-random,filename=/dev/urandom,id=rng0 \
        -device virtio-net-pci,netdev=net0 \
        -device virtio-rng-pci,rng=rng0 \
        -netdev user,id=net0,hostfwd=tcp::${SSH_QEMU_INTERNAL_PORT}-:22 \
        -display none \
        -daemonize \
        -append 'root=/dev/vda rw net.ifnames=0 oprofile.timer=1 tsc=reliable no_timer_check rcupdate.rcu_expedited=1 swiotlb=0 ip=dhcp'
else
    sudo qemu-system-x86_64 \
        -cpu IvyBridge \
        -smp 4 \
        -m 512 \
        -kernel /var/lib/yocto-built-images/${IMAGE_NAME}/bzImage \
        -drive file=/var/lib/yocto-built-images/${IMAGE_NAME}/core-image-minimal-qemux86-64.rootfs.ext4,if=virtio,format=raw \
        -object rng-random,filename=/dev/urandom,id=rng0 \
        -device virtio-net-pci,netdev=net0 \
        -device virtio-rng-pci,rng=rng0 \
        -netdev user,id=net0,hostfwd=tcp::${SSH_QEMU_INTERNAL_PORT}-:22 \
        -serial mon:stdio \
        -serial null \
        -nographic \
        -append 'root=/dev/vda rw net.ifnames=0 console=ttyS0 console=ttyS1 oprofile.timer=1 tsc=reliable no_timer_check rcupdate.rcu_expedited=1 swiotlb=0 ip=dhcp'
fi
