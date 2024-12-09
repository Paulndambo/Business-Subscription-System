# Business Payment System
This is a simple backend web application that is designed to allow business owners to list there businesses from
where they can be able to post their products.

# Functionalities
    1. Users Management.
    2. Businesses and Business Branches Managements.
    3. Business Subscriptions Management.
    4. Payments Processing.

# Technologies and Tools
- Python, Django and Django Rest Framework.
- Sqlite3 Database.

# How to Run
## 1. Virtual Environment
To run the project, you need to install dependencies, for easy management of the dependencies, create a virtual
environment. Use the following command to do so;-

```sql
python -m venv venv
```
or
```sql
python3 -m venv venv
```

Then activate the virtual environment, use the following command
```sql
source venv\Scripts\activate
```
or
```sql
source venv/bin/activate
```


## 2. Clone the repository
To clone the repository using the following command;-
```sql
git clone https://github.com/Paulndambo/Business-Subscription-System.git
```
or
```sql
git clone git@github.com:Paulndambo/Business-Subscription-System.git
```

# 3. Install the dependencies
change directory into the cloned folder and run the following command;-
```sql
pip install -r requirements.txt
```

# 4. Running the project
To start the server run the following command;-
```sql
python manage.py runserver
```

# 5. Accessing the API Documentation
To access the API documentation, go to the browser and type:
<link>http://localhost:8000/docs</link>