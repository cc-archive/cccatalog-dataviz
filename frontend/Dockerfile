# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /frontend

# add `/frontend/node_modules/.bin` to $PATH
ENV PATH /frontend/node_modules/.bin:$PATH

# install frontend dependencies
RUN apk add --no-cache git
COPY package.json ./
# COPY package-lock.json ./
RUN npm install
RUN npm install -g react-scripts@3.4.0

# add frontend
COPY . ./

# start frontend
CMD ["npm", "start"]

