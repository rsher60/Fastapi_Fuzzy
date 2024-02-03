from datab import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    iso_country = Column(String)
    theater = Column(Integer)
    available = Column(Boolean, default=False)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class matchbase(Base):
    __tablename__ = 'matchbase'

    CSCSITEID__C = Column(Integer, primary_key=True, index=True)
    ACCOUNTNAMEENGLISH__C = Column(String)
    BRANCH_CUSTOMER_PARTY_KEY = Column(Integer)
    BRANCH_PRIMARY_NAME = Column(String)
    HQ_PRIMARY_NAME = Column(String)
    GU_PRIMARY_NAME = Column(String)
    BRANCH_ISO_COUNTRY_CD = Column(String)
    BRANCH_PARTY_SSOT_PARTY_ID_INT = Column(Integer)
    BRANCH_HQ_BRANCH_CD = Column(String)
    EXACT_COUNTRY = Column(String)


class srilankainput(Base):
    __tablename__ = 'srilankainput'

    ACCOUNT_NAME = Column(Integer)
    LEAD_ID = Column(Integer, primary_key=True, index=True)
    GOMINE_ACCOUNT = Column(Integer)
    ACCOUNT_MATCH_TYPE = Column(Integer)
    PARTNER_COUNTRY = Column(Integer)
    ORIGINAL_LV_000 = Column(Integer)
    REPORTED_LV_000 = Column(Integer)
