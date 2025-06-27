# using older ubuntu, so it will work on more (older) Linux Mint/Debian/Ubuntu
FROM ubuntu:22.04 AS build

RUN apt update && apt install -y qt6-base-dev build-essential python3 python3-pip git debhelper fakeroot strace libglib2.0-0 xcb libxcb-cursor0 libxkbcommon-dev libdbus-1-3 libatk-bridge2.0-dev

# Need for update to ubuntu 24.04
# RUN userdel -r ubuntu

ARG UID=1000
ARG BRANCH=main
ARG VERSION=0.0.1

RUN useradd -rm -d /home/deb -s /bin/bash -u $UID user

USER $UID

# Need for update to ubuntu 24.04 add: --break-system-packages
RUN PATH="$PATH:/home/deb/.local/bin" && python3 -m pip install pyinstaller sip pyqt6 pyinstaller kubernetes

WORKDIR /home/deb

RUN mkdir source
RUN mkdir build

COPY --chown=$UID:999 . ./source
RUN sed -i 's/_VERSION_/'$VERSION'/g' source/debian/changelog.template \
    && sed -i 's,_BRANCH_,'$BRANCH',g' source/debian/rules.template \
    && mv source/debian/changelog.template source/debian/changelog \
    && mv source/debian/rules.template source/debian/rules

WORKDIR /home/deb/source

# add pyinstaller to PATH, build the deb package
RUN PATH="$PATH:/home/deb/.local/bin" \
    && cd /home/deb/source \
    && DEB_BUILD_OPTIONS=terse \
    && dpkg-buildpackage -b \
    && cp /home/deb/*.deb /home/deb/build

# copy the output to local machine
FROM scratch AS export-stage
COPY --from=build /home/deb/build .
