
from fastapi import FastAPI, Depends, HTTPException, status, Path
import models

from datab import engine, SessionLocal

from routers import auth , main_fuzzy
# depends : Dependency injection
app = FastAPI()

# this line will create everything from the datab and models.py files
# this line will  only run if the .db file does not exist; so if we make any change in the models.py file, this will not run
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(main_fuzzy.router)
# open a db connection only while you are using and
# close it when done
