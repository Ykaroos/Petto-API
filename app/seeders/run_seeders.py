import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from .users import seed_usuarios
from .pets import seed_pets
from .diarios import seed_diarios
from .saude import seed_saude
from .fotos import seed_fotos

def run_all():
    print("Iniciando seeders...")
    seed_usuarios()
    seed_fotos()
    seed_pets()
    seed_diarios()
    seed_saude()
    print("✅ Todos os seeders foram executados!")

if __name__ == "__main__":
    run_all()