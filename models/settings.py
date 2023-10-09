import os
from sqla_wrapper import SQLAlchemy

# connect to a database
# get env var named "DATABASE_URL" (PostgreSQL database on Heroku). If it doesn't exist, use sqlite database instead.
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))