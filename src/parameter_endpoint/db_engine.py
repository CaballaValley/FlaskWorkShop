from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///animals.db", echo=True, future=True)
