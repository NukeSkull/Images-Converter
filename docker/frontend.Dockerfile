FROM node:18-alpine

WORKDIR /sp-tools-images-converter/frontend

COPY ./frontend/package.json ./

RUN yarn install

COPY ./frontend ./

CMD [ "yarn", "start:prod" ]