#!/bin/bash

# Exit on error
set -e

# Poky
if [ -d "/opt/poky" ] && [ -n "$(ls -A "/opt/poky")" ]; then
    echo "Destination path '/opt/poky' already exists and is not an empty directory => using it."
else
    git clone https://github.com/yoctoproject/poky.git /opt/poky --branch ${YOCTO_RELEASE_BRANCH_NAME}
fi

cd /opt/poky

# Initialize the build environment
source oe-init-build-env

# Use user's configs if available, otherwise use the existing ones
cp -r /var/yocto/conf/. /opt/poky/build/conf

# Use bblayers provided by user
chmod +w -R /var/yocto/bblayers
cp -r /var/yocto/bblayers/. /opt/poky

echo -e '\n# Following lines are added by the build script:' >> /opt/poky/build/conf/local.conf

# Add ssh-server
echo 'EXTRA_IMAGE_FEATURES:append = " ssh-server-dropbear"' >> /opt/poky/build/conf/local.conf

# Add shadow (to be able to add a user with a password)
echo 'IMAGE_INSTALL:append = " shadow"' >> /opt/poky/build/conf/local.conf

# Start the build
bitbake core-image-minimal | tee /var/log/yocto/bitbake.log

# Copy image to volume with a suffix as current UNIX time
IMAGE_NAME=qemux86-64_$(date +%s)
cp -r /opt/poky/build/tmp/deploy/images/qemux86-64 /var/yocto/built-images/${IMAGE_NAME}

cd ~

echo ${IMAGE_NAME} # output used by another script
