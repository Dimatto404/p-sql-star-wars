import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

favorites_table = Table(
    'favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), nullable=True),
    Column('character_id', Integer, ForeignKey('character.id'), nullable=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))

    favorites = relationship('Planet', secondary=favorites_table, back_populates='favorited_by')
    favorites_characters = relationship('Character', secondary=favorites_table, back_populates='favorited_by')

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    climate = Column(String(100))
    terrain = Column(String(100))
    population = Column(Integer)

    characters = relationship('Character', back_populates='homeworld')
    favorited_by = relationship('User', secondary=favorites_table, back_populates='favorites')

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(50))
    birth_year = Column(String(50))
    eye_color = Column(String(50))

    homeworld_id = Column(Integer, ForeignKey('planet.id'))
    homeworld = relationship('Planet', back_populates='characters')
    favorited_by = relationship('User', secondary=favorites_table, back_populates='favorites_characters')

render_er(Base, 'diagram.png')