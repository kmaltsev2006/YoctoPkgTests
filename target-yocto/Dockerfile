FROM ubuntu:22.04

# Install essential host packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    sudo=1.9.9-1ubuntu2.5 \
    ssh=1:8.9p1-3ubuntu0.13 \
    qemu-system-x86=1:6.2+dfsg-2ubuntu6.27 \
    iproute2=5.15.0-1ubuntu2 \
    iptables=1.8.7-1ubuntu5.2 \
    build-essential=12.9ubuntu3 \
    chrpath=0.16-2 \
    cpio=2.13+dfsg-7ubuntu0.1 \
    debianutils=5.5-1ubuntu2 \
    diffstat=1.64-1build2 \
    file=1:5.41-3ubuntu0.1 \
    gawk=1:5.1.0-1ubuntu0.1 \
    gcc=4:11.2.0-1ubuntu1 \
    git=1:2.34.1-1ubuntu1.15 \
    iputils-ping=3:20211215-1ubuntu0.1 \
    libacl1=2.3.1-1 \
    liblz4-tool=1.9.3-2build2 \
    locales=2.35-0ubuntu3.11 \
    python3=3.10.6-1~22.04.1 \
    python3-git=3.1.24-1 \
    python3-jinja2=3.0.3-1ubuntu0.4 \
    python3-pexpect=4.8.0-2ubuntu1 \
    python3-pip=22.0.2+dfsg-1ubuntu0.7 \
    python3-subunit=1.4.0-3 \
    socat=1.7.4.1-3ubuntu4 \
    texinfo=6.8-4build1 \
    unzip=6.0-26ubuntu3.2 \
    wget=1.21.2-2ubuntu1.1 \
    xz-utils=5.2.5-2ubuntu1 \
    zstd=1.4.8+dfsg-3build1 && \
    apt-get clean

RUN pip install websockets==15.0.1

# Args
ARG SSH_USER
ARG SSH_PASSWORD

# Environment variables
ENV SSH_USER=${SSH_USER}

# Set up locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

# Create sshd runtime directory
RUN mkdir -p /var/run/sshd

# Add user with permissions to run qemu-system-x86_64 and start ssh service
RUN useradd -ms /bin/bash ${SSH_USER} && \
    echo "${SSH_USER}:${SSH_PASSWORD}" | chpasswd && \
    adduser ${SSH_USER} sudo && \
    chmod +w /etc/sudoers && \
    echo "${SSH_USER} ALL=(ALL) NOPASSWD: /usr/bin/qemu-system-x86_64" >> /etc/sudoers && \
    echo "${SSH_USER} ALL=(ALL) NOPASSWD: /usr/sbin/sshd" >> /etc/sudoers && \
    chmod -w /etc/sudoers

# Change workdir to SSH_USER's home directory
WORKDIR /home/${SSH_USER}

# Create Yocto directories (owned by SSH_USER):
# /opt/poky                   - for building
# /var/log/yocto              - for logs
# /var/lib/yocto-built-images - for running images
# (images are copied here for safe execution, preventing corruption of originals)
RUN mkdir -p /opt/poky /var/log/yocto /var/lib/yocto-built-images && \
    chown -R ${SSH_USER}:${SSH_USER} /opt/poky /var/log/yocto /var/lib/yocto-built-images

# Copy scripts and make them executable for SSH_USER
COPY ./entrypoint.sh /home
COPY ./build.sh ./runqemu.sh /home/${SSH_USER}
RUN chmod +x /home/entrypoint.sh /home/${SSH_USER}/build.sh /home/${SSH_USER}/runqemu.sh && \
    chown ${SSH_USER}:${SSH_USER} /home/${SSH_USER}/build.sh /home/${SSH_USER}/runqemu.sh

USER ${SSH_USER}

ENTRYPOINT ["/home/entrypoint.sh"]
