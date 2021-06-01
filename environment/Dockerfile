FROM ubuntu:20.04
ENV BUILD_THREADS=4

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./environment/apt-list /opt/apt-list

# install all deps. We use a single apt call to improve first-build speed
# bash line removes lines with comments and newlines.
RUN apt-get update && \
    cat /opt/apt-list | \
    sed 's/#.*$//g' | \
    sed '/^$/d' | \
    tr '\n' ' ' | \
    xargs apt-get install -y


# python packages
COPY ./environment/dev_requirements.txt /opt/
COPY ./environment/install_requirements.txt /opt/
RUN pip install --upgrade pip
# Installing first pip-licenses so we can track what licenses/versions of packages
RUN pip install -U pip-licenses
RUN pip install --no-cache-dir -r /opt/dev_requirements.txt
RUN pip install --no-cache-dir -r /opt/install_requirements.txt


# User credentials:
ARG USERNAME
ARG USER_UID
ARG USER_GID

# Create the user
RUN (groupadd --gid $USER_GID $USERNAME; exit 0) && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders && \
    chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server*

# Add sudo support to install extra software if needed
RUN apt-get install -y sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Clean up
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Switch to the user
USER $USERNAME

ENV DEBIAN_FRONTEND=dialog 
ENV PYTHONPATH=${PYTHONPATH}:/workdir


CMD [ "/bin/bash" ]
