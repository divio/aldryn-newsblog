ARG PYTHON_VERSION=3.6
FROM circleci/python:$PYTHON_VERSION

RUN mkdir -p /home/circleci/app/
WORKDIR /home/circleci/app/

COPY . /home/circleci/app/

ENV NODE_VERSION=6.14.1

RUN \
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install $NODE_VERSION && \
    nvm use $NODE_VERSION && \
    npm config set spin false && \
    npm install -g gulp@3.9.0 && \
    npm install -g codeclimate-test-reporter && \
    npm install

ENV NODE_PATH=/home/circleci/.nvm/versions/node/v$NODE_VERSION/lib/node_modules \
    PATH=/home/circleci/.nvm/versions/node/v$NODE_VERSION/bin:$PATH

RUN sudo apt-get install libenchant-dev

RUN sudo chown -R circleci:circleci *

RUN sudo pip install tox coveralls
