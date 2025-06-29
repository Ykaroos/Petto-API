import sys
from pathlib import Path

# Adiciona o diretório raiz ao PATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database.connection import SessionLocal
from app.models.model import *

from app.database.connection import Base, engine
Base.metadata.create_all(bind=engine)

def seed_diarios():
    db = SessionLocal()

    try:
        diarios_data = [
            {
                "conteudo": "Luffy ta cavando muito no quintal, acho que tá atrás do One Piece",
                "id_pet": 1  # Associa ao Luffy
            },
            {
                "conteudo": "Greg vive no mundo, acho que esqueceu do dono",
                "id_pet": 2  # Associa ao Greg
            }
        ]

        db.query(Diario).delete()
        
        for diario_data in diarios_data:
            db.add(Diario(**diario_data))
        
        db.commit()
        print("✅ Diários seeders executados com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao executar seeders de diários: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_diarios()
