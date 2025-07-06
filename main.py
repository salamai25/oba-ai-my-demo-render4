
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/", StaticFiles(directory="static", html=True), name="static")

SQLALCHEMY_DATABASE_URL = "sqlite:///./oba.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    program_id = Column(Integer, ForeignKey("programs.id"))

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    total_marks = Column(Integer)
    weightage = Column(Integer)
    session = Column(String)
    date = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "programs": db.query(Program).count(),
        "courses": db.query(Course).count(),
        "assessments": db.query(Assessment).count()
    }
