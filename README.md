# Users Management using FastAPI

This is a simple CRUD for managing users using FastAPI, pydantic, SQLAlchemy, and Python 3.8.10.

## Endpoints

It is recommended to check and test the available endpoints on http://127.0.0.1:8000/docs

- ``[GET] /users`` - Get all users
- ``[POST] /users/`` - Create a user
- ``[DELETE] /users/{id}`` - Delete a user given an ID
- ``[PUT] /users/`` - Update a user
- ``[GET] /users/{id}`` - Get user by ID

## Installation and Usage
Clone this git repository to your computer and access the API folder:

```
git clone https://github.com/jcazeredo/user_mgmt_fastapi.git
cd user_mgmt_fastapi
```

Install required Python libraries:
```
pip install -r requirements.txt
```

Now you can run the following command:
```
uvicorn app.main:app
```
The server should be running on http://127.0.0.1:8000
