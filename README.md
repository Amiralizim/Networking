# Database project:
Defined relations for sampled networking data in a specific time and location and created a simple CLI interface to query the data.

## Diagrams:

```./Diagrams/ER.png``` for the entity relation diagram of the data.

```./Diagrams/Client_diagram.png``` for basic flow design of the client application


## Datasets:
https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps
https://www.kaggle.com/jsrojas/labeled-network-traffic-flows-114-applications

## Setups:
Before running our code, there are a few python and sql scripts that needs to be run in the following order:

- **Make sure you are at the Networking_dataset directory** 
- First move the two data sets found at the links above in `Networking_dataset/21-Network-Traffic/` directory to the 
- Run `python extract.py` to change formatting of the data csv files.

- If you have mysql install:

        mysql -uroot -proot
        source tableSetupShort.sql

- With Ubuntu operating system you can use the docker-compose.yml file for your sql instance, make sure docker and docker-compose are installed on the computer: 
        
        Start the docker container: docker-compose up -d
        Run bash on the docker compose: docker-compose exec db bash
        Login to mysql server: mysql -uroot -proot
        Run: source tableSetupShort.sql

## How to run our CLI
- Activate your virtual env from the root folder: ```source env/bin/activate```
- Make sure your requirements are installed: ```pip install -r requirements.txt```
- In order to correctly run the client, make sure ur setting matches with /Networking_dataset/CLI/instances/config.ini specifically the config file contais: 

        host = <hostname> (default: localhost)
        port = <portnumber> (default: 3307)
        username = <username> (default: root)
        password = <password> (default: root)
        database_name = <database> (default: Networking)

- To run our CLI, simply run `python CLI/main.py`. Then you will be required to enter your username and password.

### login
- For admin, enter username: **admin** and password: **password123**
- For user, enter username: **user** and password: **password456**

## Tests:
The test has been implemented in order to check the private/public ip route of the client side.
User will be able to run the tests by 
``` python -m unittest tests.py ```
inside the project's CLI directory
