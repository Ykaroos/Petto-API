import os
from pathlib import Path
from datetime import date
from app.database.connection import SessionLocal
from app.models.model import *

def seed_fotos():
    db = SessionLocal()
    
    try:
        # 1. Configuração dos caminhos
        base_dir = Path(__file__).parent.parent.parent  # Volta até a raiz do projeto
        seed_data_dir = base_dir / "seed_data"
        
        # 2. Lista de imagens para inserir
        imagens = [
            "goldenretriver_teste01.jpg",  # Nome do primeiro arquivo
            "gatoviralata_teste02.jpg"   # Nome do segundo arquivo
        ]
        
        # 3. Verifica se a pasta existe
        if not seed_data_dir.exists():
            raise FileNotFoundError(f"Pasta seed_data não encontrada em: {seed_data_dir}")
        
        # 4. Limpa a tabela (opcional)
        db.query(Foto).delete()
        
        # 5. Processa cada imagem
        for nome_imagem in imagens:
            image_path = seed_data_dir / nome_imagem
            
            if not image_path.exists():
                print(f"⚠️ Aviso: Imagem {nome_imagem} não encontrada, pulando...")
                continue
            
            # Determina o tipo MIME automaticamente
            if nome_imagem.lower().endswith('.jpg') or nome_imagem.lower().endswith('.jpeg'):
                tipo_arquivo = "image/jpeg"
            elif nome_imagem.lower().endswith('.png'):
                tipo_arquivo = "image/png"
            else:
                tipo_arquivo = "application/octet-stream"
            
            # Lê a imagem
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Cria o registro
            db.add(Foto(
                foto=image_data,
                tipo_arquivo=tipo_arquivo,
            ))
            print(f"✔️ Imagem {nome_imagem} carregada com sucesso")
        
        db.commit()
        print("✅ Todas as fotos foram processadas com sucesso!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erro crítico ao executar seeders de fotos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_fotos()