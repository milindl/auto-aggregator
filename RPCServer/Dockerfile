FROM node:latest
RUN mkdir /app
WORKDIR /app
COPY package.json /app
COPY docker_runner.sh /app
RUN npm install

COPY RPCServer.js /app

ARG port=6800
ENV SHARE_AUTO_PORT=$port
EXPOSE $port

ENTRYPOINT ["/app/docker_runner.sh"]
