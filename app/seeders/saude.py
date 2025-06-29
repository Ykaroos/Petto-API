import sys
from pathlib import Path

# Adiciona o diretório raiz ao PATH
sys.path.append(str(Path(__file__).parent.parent.parent))


from app.database.connection import SessionLocal
from app.models.model import *

from app.database.connection import Base, engine
Base.metadata.create_all(bind=engine)

def seed_saude():
    db = SessionLocal()

    try:
        saude_data = [
            {
                "id_pet": 1,
                "vacinas": "Raiva (2023-05-10), V8 (2023-05-10)",
                "medicamentos": "Vermífugo mensal",
                "doencas": "Nenhuma"
            },
            {
                "id_pet": 2,
                "vacinas": "Raiva (2023-02-15), Tríplice Felina (2023-02-15)",
                "medicamentos": "Nenhum",
                "doencas": "Alergia a poeira"
            }
        ]

        db.query(SaudePet).delete()
        
        for saude in saude_data:
            db.add(SaudePet(**saude))
        
        db.commit()
        print("✅ Saúde pet seeders executados com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao executar seeders de saúde: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_saude()