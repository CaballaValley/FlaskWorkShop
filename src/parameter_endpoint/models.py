from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from db_engine import engine

Base = declarative_base()


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Animal({self.name})>"


class Specie(Base):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    animal_id = Column(Integer, ForeignKey('animals.id'))

    def __repr__(self):
        return f"<Species({self.name})>"


Base.metadata.create_all(engine)
