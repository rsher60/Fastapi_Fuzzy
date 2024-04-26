from typing import Annotated
from pydantic import BaseModel, Field
from io import BytesIO
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Path , APIRouter , Request , File, UploadFile
import pandas as pd
from models import country, matchbase, srilankainput
#from datab import engine, SessionLocal
from datab import engine, SessionLocal
from fuzzy_matcher import Lead_fuzzymatch
from fastapi.responses import  HTMLResponse
from fastapi.templating import  Jinja2Templates

# depends : Dependency injection
router = APIRouter()

# this line will create everything from the datab and models.py files
# this line will  only run if the .db file does not exist; so if we make any change in the models.py file, this will not run


# open a db connection only while you are using and
# close it when done

templates = Jinja2Templates(directory="templates")

class CountryRequest(BaseModel):
    __tablename__ = 'country'

    name: str = Field(min_length=3)
    iso_country: str = Field(min_length=3, max_length=100)
    theater: str = Field(min_length=3, max_length=100)
    available: bool


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# print(db_dependency.query(matchbase).all())


# print(db_dependency.query(country).all())
# commented for trial



@router.get("/form", response_class=HTMLResponse)
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@router.get("/test/{user_name}", response_class=HTMLResponse)
async def test(request: Request , user_name:str):
    return templates.TemplateResponse("home.html" , {"request":request , "username": user_name})


@router.get("/fuzzy", response_class=HTMLResponse)
async def read_all(request: Request ,db: Annotated[Session, Depends(get_db)]):
    #countries = db.query(srilankainput)
    # df = pd.read_sql(statement, db.engine)
    df_q2_srilanka = pd.read_sql_query(db.query(srilankainput).statement, con=engine)
    compare_df_sri_lanka = pd.read_sql_query(db.query(matchbase).statement, con=engine)

    a = Lead_fuzzymatch('SRI LANKA', 10, 5, df_q2_srilanka, compare_df_sri_lanka)
    output_df = a.fuzzy_merge()
    #output = output_df[['ACCOUNT_NAME', 'Match1_Ratio']]
    output = dict(zip(output_df['ACCOUNT_NAME'], output_df['Match1_Ratio']))
    return templates.TemplateResponse("fuzzy.html" , context={'request': request, 'result': output})



@router.get("/country")
async def read_countries(db: db_dependency):
    countries = db.query(country).all()
    return {country.name for country in countries}


@router.post("/predict_file")
async def create_upload_file(file:UploadFile,db: Annotated[Session, Depends(get_db)]):
    df_q2_srilanka = pd.read_csv(file.file)

    compare_df_sri_lanka = pd.read_sql_query(db.query(matchbase).statement, con=engine)

    a = Lead_fuzzymatch('SRI LANKA', 10, 5, df_q2_srilanka, compare_df_sri_lanka)
    output_df = a.fuzzy_merge()
    #output = output_df[['ACCOUNT_NAME', 'Match1_Ratio']]
    output = dict(zip(output_df['ACCOUNT_NAME'], output_df['Match1_Ratio']))
    return { 'result': output}

    file.file.close()
    return {"filename": file.filename}

"""
@app.get("/country/{country_name}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, country_name: str):
    # add the first to optimise the query as we dont know how many id's exist
    country_model = db.query(country).filter(country.name == country_name.upper()).first()
    if country_model is not None:
        return country_model
    raise HTTPException(status_code=404, detail='Country not found in the database')

@app.get("/fuzzy_match" , status_code=status.HTTP_200_OK)
async def get_fuzzy(db: db_dependency, country_name: str):
     = pd.read_sql_query(db.query(matchbase).all())

    a = Lead_fuzzymatch({country_name}, 10, 5, df_q2_srilanka, compare_df_sri_lanka)
    output_df = a.fuzzy_merge()
    return output_df[['account_name', 'Match1_Ratio']]



@app.post("/country" , status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency , country_request: CountryRequest):
    country_model = country(**country_request.dict())
    #if country_request.dict()["name"].lower() in db
    db.add(country_model)
    db.commit()


#PUT is best used when you are updating or replacing existing data on the server, while POST is
# best used when you are creating new data
"""
