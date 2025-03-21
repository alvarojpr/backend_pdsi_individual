from fastapi import FastAPI, status, Depends
import classes, model
from database import engine, get_db
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

#teste 2

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello":"World!"}

@app.get("/mensagens")
def listar_mensagens(db: Session = Depends(get_db)):
    mensagens = db.query(model.Model_Mensagem).all()
    return mensagens


@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    # mensagem_criada = model.Model_Mensagem(titulo=nova_mensagem.tutulo,conteudo=nova_mensagem.conteudo, publicada=nova_mensagem.publicada)
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return{"Mensagem:": mensagem_criada}

    # print(nova_mensagem)
    # return {"Mensagem": f"Titulo: {nova_mensagem.titulo} Conteudo: {nova_mensagem.conteudo} Publicada: {nova_mensagem.publicada}"}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.post("/webscrapping")
def webScrapping(db: Session = Depends(get_db)):
    response = requests.get('https://ufu.br')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra a navegação desejada
    nav_section = soup.find('nav', id='block-ufu-rodape-2')
    
    if nav_section:
        list_items = nav_section.find_all('li', class_='nav-item')

        for li in list_items:
            a_tag = li.find('a', class_='nav-link')
            if a_tag:
                menu_nav = a_tag.text.strip()
                link = 'https://ufu.br' + a_tag['href']

                # Cria um objeto SQLAlchemy e adiciona ao banco
                novo_menu = model.Model_Desafio(menuNav=menu_nav, link=link)
                db.add(novo_menu)

        # Confirma as inserções
        db.commit()
        return{"Dados":"inseridos com sucesso!"}

    else:
        return{"Seção":"de navegação não encontrada."}

# uvicorn app.main:app --reload --root-path server
# uvicorn main:app --reload

# ATUALIZAR
# git fetch origin
# git pull origin main

# SUBIR MUDANÇAS
# git add .                 git add requirements.txt
# git commit -m "mensagem"
# git push origin main

# GERAR E INSATALAR requirements.txt
# pip freeze > requirements.txt
# pip install requirements.txt