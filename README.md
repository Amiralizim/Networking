# Networking_dataset
ECE356 project
ER relationship diagram: draw.io
## Datasets:
https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps
https://www.kaggle.com/jsrojas/labeled-network-traffic-flows-114-applications

## Dependencies:
Our code is written in python and there are a number of libraries that need to be installed first. Please run the following commands:
```
pip3 install click
pip3 install MySQLConnector
pip3 install hashlib
pip3 install pandas
pip3 install csv
pip3 install numpy
pip3 install sklearn
pip3 install matplotlib
```

## Setups:
Before running our code, there are a few python and sql scripts that needs to be run in the following order:
- **Make sure you are at the Networking_dataset directory** 
- First move the `Networking_dataset/21-Network-Traffic/extract.py` to the `21-Network-Traffic` folder where the data csv is (basically put extract.py in the same folder as the data csv). Run `python extract.py` to change formatting of the data csv files.
- Start up your mysql database, and inside the mysql command line run `source tableSetupFull.sql` to set up your database.

## How to run our CLI
make sure to export the following evironmental variables in your environment before running the main.py:
```export DB_CONNECTION=localhost```
```export DB_PORT=3306```
To run our CLI, simply run `python CLI/main.py`. Then you will be required to enter your username and password.

### login
- For admin, enter username: **admin** and password: **password123**
- For user, enter username: **user** and password: **password456**

## Tests:
The test has been implemented in order to check the private/public ip route of the client side.
User will be able to run the tests by 
``` python -m unittest tests.py ```
inside the project's CLI directory