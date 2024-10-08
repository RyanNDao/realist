# Realist

## Overview
Realist is a tool designed to assist real estate buyers by analyzing property listings. It scrapes real estate listing websites for home data and sends the data into a database to be stored. In the future, the tool will provide insights that help users make informed purchasing decisions.

## Website
Realist is hosted on the web at https://tryrealist.com

To log in:
```
Username: RealistGuest
Password: FakeEstate1!
```

## Screenshots
![image](https://github.com/user-attachments/assets/d4413929-fa3d-4420-a6a2-92feec53de43)
![image](https://github.com/user-attachments/assets/0b877beb-32dc-4d3e-bf45-ad24839ba3d4)


## Installation

To set up the project environment, follow these steps:

### Prerequisites
- Ensure Python 3.11, [Poetry](https://python-poetry.org/docs/), Celery, and Redis Server are installed on your machine.

### Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:RyanNDao/realist.git
    cd realist
    ```
2. Install dependencies
    ```bash
    poetry install
    ```
3. Turn on Redis-Server
    ```bash
    redis-server

    ```

## Starting the Server

To get the Realist application up and running, follow these steps to start both the backend and frontend servers:

### Backend Server
The backend server is built with Flask. To start the backend server, use the following command:
```bash
poetry run start-flask
```

### Frontend Server
The frontend interface is developed using React. Start the frontend development server by running:
```bash
npm run dev
```

## Testing
To run tests and ensure the functionality of the application, use the following command:
``` bash
poetry run pytest .
```
This command executes all tests written for the Realist application, ensuring that all components function correctly as expected.

## Deployment
For deployment to a production server, make sure that the instance is running Nginx

### Launching The Backend
Use the following command, where recommended number of workers is (# of cores * 2 + 1). At least 5 workers are recommended. 
``` bash
poetry run gunicorn -w {workers} "src.backend.server.flask_index:app" --bind 0.0.0.0:8000 --log-file ./gunicorn.log
```

### Starting the Scheduler
The scheduler uses Celery to schedule scraping. It should only be ran in production and not while developing. To start the scheduler,
run the script
``` bash
sh scripts/start_celery_scheduler.sh
```
To stop the scheduler
``` bash
sh scripts/stop_celery_scheduler.sh
```
### Building the Frontend Static Files
Use the command to generate the static files. The files will be generated in /src/frontend/realist-app/dist
``` bash
npm run build
``` 

### Configuring Nginx
With the server running and the frontend built, Nginx needs to be configured to serve the app. Configure Nginx by pointing the root to the dist directory created by the npm run build command. Then, proxy requests to gunicorn port.

## Future Features

### Data Analysis Enhancements: 
Implementation of advanced analytics to assess market trends and predict future property values.

### Recommendation Engine: 
Development of a recommendation system using large language models (LLMs) to provide personalized buying suggestions based on user preferences and historical data.
