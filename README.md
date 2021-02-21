# Cossandra
Based on the name taken from [Apache Cassandra](https://cassandra.apache.org "Apache Cassandra") and COVID-19, Cossandra is a simple web application that records basic customer information. During the COVID-19 pandemic, with regulations from the government and initiatives for contact tracing, restaurants/bars in Jakarta, Indonesia started asking customers to fill out a form upon entry in order to record who's visited and notify these customers if anyone was found to test positive for COVID. Since some of these places relied on free tools that did not relationally store the information, the problem was that you had to fill out the same basic information each time you visited. This got repetitive.

## A Use Case
Cosssandra was built to solve the above problem, and I used one of my favorite places in Jakarta, Coffeebeerian, as an example implementation of the solution.

## Running with Docker
There are several ways to run the Cossandra app, my favorite is with [Docker](http://docker.com "Docker") because I don't like installing dependencies directly on my machine. This project already has a `docker-compose.yml` that can be used. In your terminal, run the following commands:

1. `docker-compose up` to build and pull the required Docker images and set up the instance
2. `docker-run run web python manage.py migrate` to perform the needed database migrations
3. `docker-run run web python manage.py createsuperuser` to create a root user for the admin panel

That should be it. The app should be running at `http://localhost:8000`.