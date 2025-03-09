from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

app = Flask(__name__)

SqlAlchemyBase = declarative_base()


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    hashed_password = Column(String)
    age = Column(Integer)
    modified_date = Column(DateTime)
    email = Column(String, unique=True)


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey('users.id'), nullable=False)
    job = Column(String, nullable=False)
    work_size = Column(Integer, nullable=False)
    collaborators = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_finished = Column(Boolean, default=False)

    def __repr__(self):
        return (f"{self.id} {self.job} {self.work_size} "
                f"{self.collaborators} {self.is_finished}")


engine = create_engine('sqlite:///mars_explorer.sqlite', echo=True)
SqlAlchemyBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def show_jobs():
    session = Session()
    jobs = session.query(Jobs).all()
    session.close()
    return render_template('jobs.html', jobs=jobs)


app.run(debug=True)
