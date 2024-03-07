from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()

DATABASE_URL = "sqlite:///DB/esa_dev.db"

engine = create_engine(DATABASE_URL, echo=False)
# Creating a scoped session factory
Session = scoped_session(sessionmaker(bind=engine))


class MainCategory(Base):
    __tablename__ = 'main_categories' 

    id = Column(Integer, primary_key=True)
    main_category = Column(String, unique=True)


class SubCategory(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True)
    sub_category = Column(String)
    main_category_id = Column(Integer, ForeignKey('main_categories.id'))


# #For testing and running the models directly
# if __name__ == "__main__":
    
#     engine = create_engine(DATABASE_URL)
#     # Creating a scoped session factory
#     #Session = scoped_session(sessionmaker(bind=engine))
