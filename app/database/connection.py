from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    os.environ["database_url"], connect_args={"check_same_thread": False}
    )

try:
        connection = engine.connect()
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        connection.close()
except Exception as e:
        print(f"❌ Falha ao conectar ao banco de dados: {e}")
        raise
except KeyError:
    print("❌ Variável DATABASE_URL não encontrada no arquivo .env")
    raise
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()