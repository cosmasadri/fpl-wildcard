FROM node:12-alpine

ENV APPDIR /app

# procps for nest cli
RUN apk add --no-cache procps

RUN mkdir ${APPDIR}
WORKDIR ${APPDIR}

COPY package.json yarn.lock ./
RUN yarn install

COPY . ${APPDIR}

CMD ["yarn", "run", "start"]
