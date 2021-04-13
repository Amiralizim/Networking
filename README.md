# Networking_dataset
ECE356 project
ER relationship diagram: draw.io
# Datasets:
https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps
https://www.kaggle.com/jsrojas/labeled-network-traffic-flows-114-applications

# Dependencies:
Our code is written in python and there are a number of libraries that need to be installed first. Please run the following commands:
```pip3 install click```
```pip3 install MySQLConnector```
```pip3 install hashlib```
```pip3 install pandas```
```pip3 install csv```
```pip3 install numpy```
```pip3 install sklearn```
```pip3 install matplotlib```

# Setups:
Before running our code, there are a few python and sql scripts that needs to be run in the following order:
First navigate to the `21-Network-Traffic`

# Tests:
The test has been implemented in order to check the private/public ip route of the client side.
User will be able to run the tests by 
``` python -m unittest tests.py ```
inside the project's CLI directory