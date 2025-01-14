from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()

DATABASE_URL = "sqlite:///../DB/esa_dev.db"
# DATABASE_URL = "sqlite:///DB/esa_dev.db"

engine = create_engine(DATABASE_URL, echo=False)

# scoped session factory
Session = scoped_session(sessionmaker(bind=engine))


class MainCategory(Base):
    __tablename__ = "main_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_category = Column(String(collation="NOCASE"), unique=True, nullable=False)


class SubCategory(Base):
    __tablename__ = "sub_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_category = Column(String(collation="NOCASE"), nullable=False)
    main_category_id = Column(Integer, ForeignKey("main_categories.id"), nullable=False)


class Results(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    file_name = Column(String(collation="NOCASE"))
    output_json = Column(String(collation="NOCASE"))
    analyzed_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
