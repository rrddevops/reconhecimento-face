from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import base64
import os
import json
from datetime import datetime

app = FastAPI(title="Sistema de Reconhecimento Facial - Modo Simples", version="1.0.0")

# Permitir CORS para testes locais
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Simular banco de dados em memória
usuarios_db = {}

class CadastroRequest(BaseModel):
    cpf: str
    imagem_base64: str

class ReconhecerRequest(BaseModel):
    imagem_base64: str

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.get("/status")
async def status():
    """Endpoint para verificar status do servidor"""
    return JSONResponse(content={
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "usuarios_cadastrados": len(usuarios_db),
        "modo": "simples"
    })

@app.post("/cadastro")
async def cadastro(request: CadastroRequest):
    """Cadastra usuário (modo simples - sem validação facial)"""
    try:
        # Validar CPF básico
        cpf_limpo = request.cpf.replace(r'[^\d]', '')
        if len(cpf_limpo) != 11:
            return JSONResponse(content={
                "status": "erro", 
                "mensagem": "CPF deve ter 11 dígitos."
            }, status_code=400)
        
        # Verificar se CPF já existe
        if request.cpf in usuarios_db:
            return JSONResponse(content={
                "status": "erro", 
                "mensagem": "CPF já cadastrado."
            }, status_code=400)
        
        # Salvar usuário
        usuarios_db[request.cpf] = {
            "cpf": request.cpf,
            "imagem_base64": request.imagem_base64,
            "data_cadastro": datetime.now().isoformat()
        }
        
        print(f"✅ Usuário cadastrado: {request.cpf}")
        
        return JSONResponse(content={
            "status": "recebido", 
            "cpf": request.cpf,
            "mensagem": "Usuário cadastrado com sucesso!"
        })
        
    except Exception as e:
        print(f"❌ Erro no cadastro: {e}")
        return JSONResponse(content={
            "status": "erro", 
            "mensagem": f"Erro interno: {str(e)}"
        }, status_code=500)

@app.post("/reconhecer")
async def reconhecer(request: ReconhecerRequest):
    """Reconhece usuário (modo simples - comparação direta)"""
    try:
        # Em modo simples, retorna o primeiro usuário cadastrado
        # (simulação para teste)
        if usuarios_db:
            # Pegar o primeiro usuário cadastrado
            primeiro_usuario = list(usuarios_db.keys())[0]
            usuario = usuarios_db[primeiro_usuario]
            
            print(f"✅ Usuário reconhecido (simulado): {usuario['cpf']}")
            
            return JSONResponse(content={
                "status": "match", 
                "cpf": usuario['cpf'],
                "mensagem": "Usuário reconhecido (modo simulado)"
            })
        else:
            return JSONResponse(content={
                "status": "nao_encontrado",
                "mensagem": "Nenhum usuário cadastrado no sistema."
            }, status_code=404)
            
    except Exception as e:
        print(f"❌ Erro no reconhecimento: {e}")
        return JSONResponse(content={
            "status": "erro", 
            "mensagem": f"Erro interno: {str(e)}"
        }, status_code=500)

@app.get("/usuarios")
async def listar_usuarios():
    """Lista usuários cadastrados"""
    return JSONResponse(content={
        "usuarios": list(usuarios_db.keys()),
        "total": len(usuarios_db)
    })

@app.delete("/usuarios/{cpf}")
async def remover_usuario(cpf: str):
    """Remove usuário cadastrado"""
    if cpf in usuarios_db:
        del usuarios_db[cpf]
        return JSONResponse(content={
            "status": "removido",
            "mensagem": f"Usuário {cpf} removido com sucesso."
        })
    else:
        return JSONResponse(content={
            "status": "erro",
            "mensagem": "Usuário não encontrado."
        }, status_code=404)

@app.get("/test-cpf/{cpf}")
async def test_cpf(cpf: str):
    """Testa validação de CPF"""
    import re
    
    # Limpar CPF
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    
    # Validar CPF
    if len(cpf_limpo) != 11:
        return JSONResponse(content={
            "cpf_original": cpf,
            "cpf_limpo": cpf_limpo,
            "valido": False,
            "erro": "CPF deve ter 11 dígitos"
        })
    
    # Verificar se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        return JSONResponse(content={
            "cpf_original": cpf,
            "cpf_limpo": cpf_limpo,
            "valido": False,
            "erro": "CPF não pode ter todos os dígitos iguais"
        })
    
    # Calcular dígitos verificadores
    soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
    resto = 11 - (soma % 11)
    dv1 = 0 if resto < 2 else resto
    
    soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
    resto = 11 - (soma % 11)
    dv2 = 0 if resto < 2 else resto
    
    valido = cpf_limpo[9] == str(dv1) and cpf_limpo[10] == str(dv2)
    
    return JSONResponse(content={
        "cpf_original": cpf,
        "cpf_limpo": cpf_limpo,
        "valido": valido,
        "dv1_calculado": dv1,
        "dv1_recebido": int(cpf_limpo[9]),
        "dv2_calculado": dv2,
        "dv2_recebido": int(cpf_limpo[10])
    })

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor em modo simples...")
    print("📝 Funcionalidades disponíveis:")
    print("   - Cadastro de usuários")
    print("   - Reconhecimento simulado")
    print("   - Validação de CPF")
    print("   - Listagem de usuários")
    print("🌐 Acesse: http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002) 