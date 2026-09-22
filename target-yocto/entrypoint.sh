#!/bin/bash

# Exit on error
set -e

if [ -z "${1}" ]; then
    echo "Usage: $0 MODE (BUILD|RUN|IDLE) [params]" >&2
    exit 1
fi

MODE=${1}
IMAGE_NAME=${2}

# Set up ENV for SSH_USER
echo "export YOCTO_RELEASE_BRANCH_NAME=${YOCTO_RELEASE_BRANCH_NAME}" >> ~/.bashrc
echo "export SSH_QEMU_INTERNAL_PORT=${SSH_QEMU_INTERNAL_PORT}" >> ~/.bashrc

# Start ssh service asap
sudo /usr/sbin/sshd

case "${MODE}" in
    BUILD)
        echo "MODE: ${MODE}"
        ./runqemu.sh -d -i $(./build.sh | tail -n 1) # runs qemu as a daemon with image name received from build.sh
        ;;
    RUN)
        echo "MODE: ${MODE}"
        ./runqemu.sh -d -i ${IMAGE_NAME} # runs qemu as a daemon with given image name
        ;;
    IDLE)
        echo "MODE: ${MODE}"
        # Do nothing
        ;;
    *)
        echo "Usage: $0 MODE (BUILD|RUN|IDLE) [params]" >&2
        exit 1
        ;;
esac

# Keep docker container running
/bin/bash
