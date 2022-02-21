from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint: [POST] /users/ - Create a user
@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(
    request: schemas.User, response: Response, db: Session = Depends(get_db)
):
    # Create a new User. Pydantic and the Enum class already do the arguments validation.
    # The ID field in the request body is ignored, since an ID value will be assigned by the DB.
    new_user = models.User(
        name=request.name,
        favorite_tv_show=request.favorite_tv_show,
    )

    db.add(new_user)

    # Check if we have any error while adding it to the DB, and provide a 500 status code.
    try:
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"A problem occurred when adding the user to the database.",
        )

    db.refresh(new_user)

    return new_user


# Endpoint: [DELETE] /users/{id} - Delete a user given an ID
@app.delete(
    "/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"]
)
def delete_user(id: int, db: Session = Depends(get_db)):
    # Get the first user with the given ID
    user = db.query(models.User).filter(models.User.id == id)

    # If there is no user with the given ID, return error 404 and custom message
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} is not available.",
        )

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Endpoint: [PUT] /users/ - Update a user
@app.put("/users/", status_code=status.HTTP_202_ACCEPTED, tags=["users"])
def update_user(request: schemas.User, db: Session = Depends(get_db)):
    # Get the first user with the given ID
    user = db.query(models.User).filter(models.User.id == request.id)

    # If there is no user with the given ID, return error 404 and custom message
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {request.id} is not available.",
        )

    user.update(request.dict())
    db.commit()

    return f"The user with ID {request.id} was successfully updated."


# Endpoint: [GET] /users/ - Get all users
@app.get("/users", response_model=List[schemas.User], tags=["users"])
def get_users(db: Session = Depends(get_db)):
    # Get all users from DB
    users = db.query(models.User).all()

    return users


# Endpoint: [GET] /users/{id} - Get user by ID
@app.get("/users/{id}", response_model=schemas.User, tags=["users"])
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    # Get the first user with the given id
    user = db.query(models.User).filter(models.User.id == id).first()

    # If there is no user with the given ID, return error 404 and custom message
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} is not available.",
        )

    return user
