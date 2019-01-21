from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column,  Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///intranet.db', echo=True)
Base = declarative_base()


class EMPLOYEES(Base):
    __tablename__ = 'EMPLOYEES'

    EMP_ID = Column(Integer, primary_key=True)
    FIRST_NAME = Column(String, nullable=False)
    LAST_NAME = Column(String, nullable=False)
    PHONE_NUMBER = Column(Integer, unique=True, nullable=False)
    EMAIL = Column(String, unique=True, nullable=False)
    PASSWORD = Column(String, nullable=False)

    def __init__(self, fname, lname, phone, email, password):

        self.FIRST_NAME = fname
        self.LAST_NAME = lname
        self.PHONE_NUMBER = phone
        self.EMAIL = email
        self.PASSWORD = password


class COMPANIES(Base):
    __tablename__ = 'COMPANIES'
    COMPANY_NAME = Column(String, primary_key=True, nullable=False)
    DESCRIPTION = Column(String, nullable=False)

    def __init__(self, cname, description):

        self.COMPANY_NAME = cname
        self.DESCRIPTION = description


class ORDERS(Base):

    __tablename__ = 'ORDERS'
    ORDER_ID = Column(Integer, primary_key=True, nullable=False)
    COMPANY_NAME = Column(String, ForeignKey(COMPANIES.COMPANY_NAME), nullable=False)
    PRODUCTS = Column(String, nullable=False)
    DATEM = Column(String, nullable=False)
    DATED = Column(String, nullable=False)

    def __init__(self, cname2,products,datem,dated):

        self.COMPANY_NAME = cname2
        self.PRODUCTS = products
        self.DATEM = datem
        self.DATED = dated



Base.metadata.create_all(engine)
