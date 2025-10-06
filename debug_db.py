# debug_db.py

import os
from core.database import SessionLocal, create_db_and_tables
from core.models import Persona

print("--- INICIANDO TESTE DE BANCO DE DADOS ---")

# 1. Deletar o banco de dados antigo para garantir um começo limpo
if os.path.exists("./personapost.db"):
    os.remove("./personapost.db")
    print("Arquivo de banco de dados antigo removido.")

# 2. Criar a estrutura do banco de dados e as tabelas
try:
    create_db_and_tables()
    print("Banco de dados e tabela 'personas' criados com sucesso.")
except Exception as e:
    print(f"!!! ERRO AO CRIAR TABELAS: {e}")
    exit()

# 3. Tentar criar e salvar uma nova Persona
db = SessionLocal()
print("Sessão com o banco de dados aberta.")

try:
    print("Tentando criar um novo objeto Persona...")

    # Criamos um objeto Persona com dados de teste
    nova_persona = Persona(
        nome="Teste Debug",
        descricao="Uma persona para testar a escrita no DB.",
        tom_de_voz="Direto",
        session_id="debug-123"
    )

    print("Objeto Persona criado em memória com sucesso.")

    db.add(nova_persona)
    print("Objeto adicionado à sessão (db.add).")

    db.commit()
    print("✅ SUCESSO! Commit no banco de dados realizado. A persona foi salva.")

except Exception as e:
    print("\n!!! FALHA AO SALVAR A PERSONA !!!")
    print("O erro ocorreu durante a interação com o banco de dados.")
    print("Traceback completo do erro:")
    # Imprime o erro completo para descobrirmos a causa
    import traceback
    traceback.print_exc()

finally:
    db.close()
    print("Sessão com o banco de dados fechada.")
    print("--- FIM DO TESTE ---")