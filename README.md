# Visualize CC Catalog Data

## About

The landscape of openly licensed content is wide and varied. Millions of web pages host and share CC-licensed works—in fact, we estimate that there are over 1.6 billion across the web! With this growth of CC-licensed works, Creative Commons (CC) is increasingly interested in learning how hosts and users of CC-licensed materials are connected, as well as the types of content published under a CC license and how this content is shared. Each month, CC uses [Common Crawl](https://commoncrawl.org/) data to find all domains that contain CC-licensed content. This dataset contains information about the URL of the websites and the licenses used. 

In order to draw conclusions and insights from this dataset, we created the **Linked Commons**: a visualization that shows how the Commons is digitally connected.

A live demo of the project can be found in [here](http://dataviz.creativecommons.engineering/)

![](https://opensource.creativecommons.org/blog/entries/linked-commons-gsoc-wrap-up/design-light.png)

## Getting Started

### Directory Structure
```bash
src
│   README.md
│   docker-compose.yml # Development docker compose
│
└───GSoC2019
└───data-release
│
└───frontend
│  |   .env # Contains Backend Server Base Endpoint
│  │   package.json
│  │   package.lock.json
│  │
│  └───src # Contains all React Components
│  
└───backend
   │   requirements.txt
   │   .env # Contains list of environment variables the project needs
   │
   └───scripts # Contains scripts to parse JSON data and upload it to MongoDB server
   └───src # Contains server side Django Apps
```


## Setting Up Local Development Environment Without Docker

### Prerequisites

The frontend application is using react, for which NodeJS **v12+** and npm are necessary. NodeJS can be installed from [here](https://nodejs.org/en/).

The backend application is using Django, for which Python **v3.7+** necessary. Python can be installed from [here](https://www.python.org/downloads/).

### Frontend
1. Navigate to `frontend/` directory.
```bash
cd frontend/
```
2. Install all dependencies (Make sure that there exists a package.json in the current path)
```bash
npm install
```
3. To start the development server, use the following command in the terminal.
```bash
npm start
```
4. To create an optimized build for production, run the following command in the terminal.
```bash
npm run build
```

### Backend and Database


1. Navigate to `backend/` directory.
```bash
cd backend/
```
2. Before proceeding further, ensure that all the variables in `.env` file are updated and `MONGO_HOSTNAME` is set to `localhost:27017`.
3. Install all dependencies
```bash
pip install -r requirements.txt
```
4. Navigate to `src/` directory where `Django-server` code exists
```bash
cd src/
```
5. To start the development server, use the following command
```bash
python manage.py runserver
```
7. Now the backend should be live at `localhost:8000`.
8. The server needs a running instance of MongoDB. Start the Mongo DB server and ensure that the `authentication credentials` are exactly same as defined in the `.env` file. If you wish to update the data inside the Database, head over to [this](#add-data-to-mongodb) section.
9. Happy Contributing to Linked Commons! 🚀🚀🚀


## Setting Up Local Development Environment using Docker

### Development 

1. Make sure that the root directory contains `docker-compose.yml`. And ensure that `backend/.env` has file is updated and `MONGO_HOSTNAME` is set to `mongodb:27017`.
2. Run the following command to build and start the container.
```bash
docker-compose up
```
3. Now the frontend, backend and database should be live.
   - The frontend can be accessed at [localhost:3000](http://localhost:3000/).
   - The backend can be accessed at [localhost:8000](http://localhost:8000/).
   - Mongodb server can be accessed at [localhost:27017](http://localhost:27017/).
4. If this is the first time you have built the container, head over to [this](#add-data-to-mongodb) section to learn how to add data to the MongoDB.
5. Any changes in the `backend/` and `frontend/` will trigger a rebuild process and you will be able to see the changes on server! 
6. Happy Contributing to Linked Commons! 🚀🚀🚀



### Building production version

**Important:** For simiplicity the production version can be built only with `docker`. Please note that any changes in project files after build won't get reflected in the running container and you need to rebuild the image again. 

1. Before building images, ensure that all the variables in `.env` file are updated and `MONGO_HOSTNAME` is set to `mongodb:27017`.
2. Now, navigate to backend and then build the `django-backend` image.
```bash
cd backend/
docker build . -f Dockerfile.prod -t linked_commons/backend
```
3. Create a new user-defined bridge network
```bash
docker network create --driver=bridge linkedcommons-net
```
4. Now run the recently built `linked_commons/backend` image.
```bash
docker run --name backend \
   -p 8000:8000 --env-file ./env \
   --network=linkedcommons-net \
   --rm -d linked_commons/backend
```
5. Now to start the database in an isolated container.
```bash
docker run -it --name mongodb \
   --network=linkedcommons-net \
   -p 27017:27017 -v mongodbdata:/data/db \
   --env-file ./.env --rm -d mongo:4.0.8
```
6. You can now access the backend at port `8000` and database at port `27017` of localhost. If you wish to add data then head over to [this](#add-data-to-mongodb) section.

7. Now, let's build the `frontend`. Navigate to frontend directory and build the `react-frontend` image.
```bash
cd frontend
docker build . -f Dockerfile.prod  -t  linkedcommons/frontend
```
8. Now to start the frontend application run the following command.
```bash
docker run --name frontend \
   -p 3000:80 --rm -d linkedcommons/frontend
```
9. Now, the frontend can be accessed at [localhost:3000](http://localhost:3000/).


### Add data to MongoDB
1. Navigate to the directory containing `build_db_script.py`.
```bash
cd backend/scripts
```
2. Ensure that the directory contains `fdg_input_file.json` or update the `INPUT_FILE_PATH` variable which will be uploaded to the database. A sample `fdg_input_file.json` can be found inside `data-release/` directory.
3. Ensure that all the variables in `.env` file are updated with the running mongodb server.
4. Now run the `build_db_script` in the terminal. 
```bash
# It will connect to the database at `localhost:27017` and update the data. 
python build_db_script.py localhost
```
5. It should take a while depending on the JSON file size. 
6. Congrats! You have successfully updated the data. 🎉🎉🎉


## Archive

[GSoC2019](https://github.com/creativecommons/cccatalog-dataviz/tree/master/GSoC2019) - Google Summer of Code project by [María Belén Guaranda](https://github.com/soccerdroid)
