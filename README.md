# Second Chance Clothing Co: MySQL + Flask Boilerplate Project

This repository is for SecondChanceCo, an online marketplace for secondhand clothing. Individuals can upload photos and descriptions of their items and sell them to others. By providing a platform for people to resell their clothes, it offers an economically feasible alternative for individuals who cannot afford to buy brand new clothing at retail prices.

SecondChanceCo promotes sustainable fashion by reducing the demand for mass production of new clothing items, helping minimize the environmental impact of the fashion industry, which is known to be one of the largest polluting industries in the world. By reducing the demand for the mass-production of clothing items, SecondChanceCo can help minimize the exploitation of workers in production environments (especially fast-fashion). The website counteracts the fast fashion industry by promoting a more sustainable approach to fashion, and acts as a more accessible option for people to buy and sell second hand clothing, eliminating the need to physically go to a thrift store.

This repository is for the flask routes and also contains a docker_compose.yaml file, which breaks down the ports for connection to a database container that can be viewed in DataGrip as well as connection to AppSmith for the deployment of the application to a user. Routes were developed for two blueprints: customers and sellers. Customers could browse posted products, and add or delete products from their cart. Sellers could create new posts in order to post new products, update their profile information with new address information, and also delete product listings no longer available. 

The application for SecondChanceCo was designed and implemented by Alexandra Descoteaux, Sreeya Gudlavalleti, Angela Fee, Jennifer Cheung, and deployed on April 20th 2023.

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




