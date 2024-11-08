### AUBOUTIQUE

#### Project Description

This application provides a platform where users can manage products (add, update, view, buy, and remove), interact with others, and perform basic e-commerce operations. The server handles these requests in real-time, maintaining data integrity and user-specific information.

Libraries used:
socket library used to handle sockets of both clients and server
sqlite3 which is used to handle the database
json which is essential to send and receive messages of type json so that there is an exchange between the client side (web application (front end)) and the server side (backend)
threading which allows multiple users to connect all at once on the specified address and port number of the server
time which was used to properly handle threading (properly handle the time between all threads)
bcrypt which was used to encrypt passwords that are stored in the database (an extra layer of security)
sys which was used to extract the (inputed) port number

#### How to Install and Run the Project

- ##### On Windows:
  1. `git clone <repo name>`
  2. `cd <repo name>`
  3. Create a virtual environment by running `python -m venv .venv`
  4. Activate the virtual environment by running `.venv\Scripts\activate`
  5. Install the required libraries by running `pip install -r requirements.txt`
  6. Run the client side code `python client.py` and the server side code `python server.py`
- ##### On Mac/Linux:
  1. `git clone <repo name>`
  2. `cd <repo name>`
  3. Create a virtual environment by running `python -m venv .venv`
  4. Activate the virtual environment by running `source .venv/bin/activate`
  5. Install the required libraries by running `pip install -r requirements.txt`
  6. Run the client side code `python client.py` and the server side code `python server.py`

#### Youtube link of the demo

https://youtu.be/102fU2aH_Ds
