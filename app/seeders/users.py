import sys
from pathlib import Path

# Adiciona o diretório raiz ao PATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database.connection import SessionLocal
from app.models.model import *

from app.database.connection import Base, engine
Base.metadata.create_all(bind=engine)

def seed_usuarios():
    db = SessionLocal()

    try:
        usuarios_data = [
            {
                "email": "admin@petto.com",
                "nome": "Administrador",
                "senha": "batatinhafrita123"  # senha: secret
            },
            {
                "email": "cliente@example.com",
                "nome": "João Silva",
                "senha": "forrolimaocommel"
            }
        ]

        db.query(Usuario).delete()
        
        for usuario_data in usuarios_data:
            db.add(Usuario(**usuario_data))
        
        db.commit()
        print("✅ Usuários seeders executados com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao executar seeders de usuários: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_usuarios()
