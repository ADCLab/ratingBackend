from fastapi import FastAPI, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import os
from sqlalchemy import Table, Column, Integer, String, Boolean, TIMESTAMP, MetaData, insert, select
from datetime import datetime

# Load environment variables
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "dbname")

MONGODB_USER = os.getenv("MONGODB_USER", "user")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "password")
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_DB = os.getenv("MONGODB_DB", "mydatabase")

MYSQL_DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"

# Initialize FastAPI app
app = FastAPI()

# Set up MySQL async engine and session
mysql_engine = create_async_engine(MYSQL_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=mysql_engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()
ratings_table = Table(
    "Ratings", metadata,
    Column("c_id", Integer, nullable=False),
    Column("u_id", Integer, nullable=False),
    Column("d_id", Integer, nullable=False),
    Column("rating", Integer, nullable=True),
    Column("flag", Boolean, nullable=True),
    Column("skip", Boolean, nullable=True),
    Column("other", String, nullable=True),
    Column("time", TIMESTAMP, nullable=False, default=datetime.utcnow),
)

comments_table = Table(
    "Comments", metadata,
    Column("c_id", Integer, nullable=False),
    Column("d_id", Integer, nullable=False)
)

evaluators_table = Table(
    "Evaluators", metadata,
    Column("u_id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True)
)

def get_mysql_session():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Set up MongoDB client
mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client.get_database(MONGODB_DB)

@app.post("/ratecomment")
async def rate_comment(d_id: int, c_id: int, u_id: int, rating: int, flag: bool, other: str, db: AsyncSession = Depends(get_mysql_session)):
    stmt = insert(ratings_table).values(
        d_id=d_id, c_id=c_id, u_id=u_id, rating=rating, flag=flag, other=other, time=datetime.utcnow()
    )
    await db.execute(stmt)
    await db.commit()
    return {"message": "Rating submitted successfully"}

async def get_comments_in_dataset(d_id: int, db: AsyncSession):
    stmt = select(comments_table.c.c_id).where(comments_table.c.d_id == d_id)
    result = await db.execute(stmt)
    return [row[0] for row in result.fetchall()]

async def get_comments_from_mongodb(c_id_list: list):
    return [doc async for doc in mongo_db.comments.find({"c_id": {"$in": c_id_list}})]

@app.get("/getcomments")
async def get_comments(d_id: int, db: AsyncSession = Depends(get_mysql_session)):
    c_id_list = await get_comments_in_dataset(d_id, db)
    comments = await get_comments_from_mongodb(c_id_list)
    return {"comments": comments}

@app.get("/allevaluators")
async def get_all_evaluators(db: AsyncSession = Depends(get_mysql_session)):
    stmt = select(evaluators_table.c.u_id, evaluators_table.c.name)
    result = await db.execute(stmt)
    evaluators = result.fetchall()
    
    output = "\n".join([f"{row.u_id}, {row.name}" for row in evaluators])
    return Response(content=output, media_type="text/plain")

@app.post("/addcomments")
async def add_comments(comments: list):
    await mongo_db.comments.insert_many(comments)
    return {"message": "Comments added successfully"}

@app.post("/adddataset")
async def add_dataset(d_id: int, c_id_list: list, db: AsyncSession = Depends(get_mysql_session)):
    stmt = insert(comments_table).values([{"d_id": d_id, "c_id": c_id} for c_id in c_id_list])
    await db.execute(stmt)
    await db.commit()
    return {"message": "Dataset added successfully"}

@app.post("/checkevaluator")
async def check_evaluator(name: str, db: AsyncSession = Depends(get_mysql_session)):
    stmt = select(evaluators_table.c.u_id).where(evaluators_table.c.name == name)
    result = await db.execute(stmt)
    row = result.fetchone()
    
    if row:
        return {"u_id": row.u_id}
    
    stmt = insert(evaluators_table).values(name=name)
    result = await db.execute(stmt)
    await db.commit()
    return {"message": "Evaluator added", "u_id": result.lastrowid}

# Run the application with: uvicorn filename:app --reload
