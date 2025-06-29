# 🐾 **Petto API**

Um sistema de gerenciamento de pets, com autenticação de usuários, registros de doenças, vacinas e medicamentos, além de diários personalizados para cada bichinho!  
---
## 📁 Estrutura do Projeto

```
Petto/
│
├── app/                      # Pasta principal da aplicação
│   ├── database/             # Configurações do banco de dados
│   │   └── connection.py
│   ├── migrations/           # Migrações Alembic
│   │   ├── versions/
│   │   └── env.py
│   ├── models/               # Modelos e schemas
│   │   ├── model.py
│   │   └── schemas.py
│   ├── routes/               # Endpoints FastAPI
│   │   ├── auth.py
│   │   ├── diaries.py
│   │   ├── medical.py
│   │   ├── pets.py
│   │   └── users.py
│   └── seeders/              # Scripts de seed
│       ├── diarios.py
│       ├── fotos.py
│       ├── pets.py
│       ├── run_seeders.py
│       ├── saude.py
│       └── users.py
│
├── seed_data/                # Imagens utilizadas pelos seeders
│   ├── gatoviralata_teste02.jpg
│   └── goldenretriver_teste01.jpg
│
├── venv/                     # Ambiente virtual Python
├── .env                      # Variáveis de ambiente (produção)
├── .env.example              # Exemplo de variáveis de ambiente
├── alembic.ini               # Configuração do Alembic
├── main.py                   # Ponto de entrada da aplicação
├── petto.db                  # Banco de dados SQLite
├── README.md                 # Documentação do projeto
└── requirements.txt          # Dependências do projeto
```

---

## 📥 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/klawwwz/Petto-API.git
cd Petto
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
```

- **Windows:**
```bash
venv\Scripts\activate
```

- **Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente

```bash
cp .env.example .env
# Edite o .env com suas configurações
```

---

## 🚀 Execução

### 1. Aplique as migrações

```bash
alembic upgrade head
```

### 2. (Opcional) Carregue dados iniciais

```bash
python -m app.seeders.run_seeders
```

### 3. Inicie o servidor

```bash
uvicorn main:app --reload
```