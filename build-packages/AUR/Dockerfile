FROM manjarolinux/base AS build

RUN pacman --noconfirm -Syyu \
    && pacman --noconfirm -Syu --needed debugedit gtk3 procps-ng git python python-pip namcap python-pyqt6 \
    && rm -rf /var/cache/pacman/pkg/*

ARG UID=1000
ARG VERSION=0.0.1
ARG BRANCH=main

RUN useradd -u $UID -rm -d /builder -s /bin/bash builder || true

RUN echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo "MAKEFLAGS=\"-j$(nproc)\"" >> /etc/makepkg.conf

USER builder

WORKDIR /builder

RUN mkdir results
RUN PATH="$PATH:/builder/.local/bin" && pip install pyinstaller sip kubernetes --break-system-packages

COPY PKGBUILD.template PKGBUILD
RUN sed -i 's/_VERSION_/'$VERSION'/g' PKGBUILD \
    && sed -i 's,_BRANCH_,'$BRANCH',g' PKGBUILD

RUN PATH="$PATH:/builder/.local/bin" \
    && namcap PKGBUILD && makepkg -f \
    && sudo cp *.pkg.tar.zst results/

# copy the output to local machine
FROM scratch AS export-stage
COPY --from=build /builder/results .
