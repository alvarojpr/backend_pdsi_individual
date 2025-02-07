from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv # biblioteca para carregar variáveis de ambiente

dotenv_path = os.path.join(os.path.dirname(__file__), '.env') # caminho para o arquivo .env: 
load_dotenv(dotenv_path) # carrega as variáveis de ambiente


DATABASE_URL = os.getenv("DATABASE_URL") # pega a variável de ambiente DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi encontrada no arquivo .env")

engine = create_engine(DATABASE_URL) # cria o engine que é responsável por se conectar ao banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # sessão, responsável por fazer as queries no banco de dados
Base = declarative_base() # cria a base que é usada para criar as tabelas no banco de dados

#função que retorna a sessão para as rotas manipularem o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()