import sys
from pathlib import Path

# Adiciona o diretório raiz ao PATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database.connection import SessionLocal
from app.models.model import *

from datetime import date

from app.database.connection import Base, engine
Base.metadata.create_all(bind=engine)

def seed_pets():
    db = SessionLocal()

    try:
        pets_data = [
            {"nome": "Luffy",
             "dataNasc": date(2025, 3, 1), #ano, mes, dia
             "tipo": "Cachorro",
             "cor": "Dourado",
             "peso": 8.5,
             "raca": "Golden Retriever",
             "sexo": "Macho",
             "id_foto": 1,
             "id_usuario": 1 #associado ao admin#
            },
             {
             "nome": "Greg",
             "dataNasc": date(2022, 2, 7),
             "tipo": "Gato",
             "cor": "Branco",
             "peso": 4.5,
             "sexo": "Macho",
             "id_foto": 2,
             "id_usuario": 2  # Associa ao João
             }
        ]
        # Limpa a tabela (opcional)
        db.query(Pet).delete()
        
        # Adiciona os pets
        for pet_data in pets_data:
            db.add(Pet(**pet_data))
        
        db.commit()
        print("✅ Pets seeders executados com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao executar seeders: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_pets()