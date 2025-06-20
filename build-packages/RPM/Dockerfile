# https://www.redhat.com/sysadmin/create-rpm-package
# https://stackoverflow.com/questions/51640995/python-3-5-create-rpm-with-pyinstaller-generated-executable
FROM fedora:42 AS build

# install packages needed for application
RUN sudo dnf install -y rpmdevtools rpm-build git python python3-pyqt6 python3-kubernetes python3-pip

ARG UID=1000
ARG VERSION=0.0.1
ARG BRANCH=main

# create user for build
RUN useradd -rm -d /home/rpm -s /bin/bash -u $UID user
USER $UID

WORKDIR /home/rpm

# pyinstaller is not in the fedora repo
RUN python -m pip install pyinstaller \
    && mkdir source && mkdir rpmbuild

COPY babelvis-k8s-cronjob-trigger.spec.template babelvis-k8s-cronjob-trigger.spec

# update template with version to build
# add pyinstaller to PATH, build the rpm package
RUN sed -i 's/_VERSION_/'$VERSION'/g' babelvis-k8s-cronjob-trigger.spec \
    && sed -i 's,_BRANCH_,'$BRANCH',g' babelvis-k8s-cronjob-trigger.spec \
    && PATH="$PATH:/home/rpm/.local/bin" \
    && cd /home/rpm \
    && rpmbuild -ba babelvis-k8s-cronjob-trigger.spec

# copy the output to local machine
FROM scratch AS export-stage
COPY --from=build /home/rpm/rpmbuild/RPMS .