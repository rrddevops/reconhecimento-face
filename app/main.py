from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import base64
import os
from sqlalchemy.exc import IntegrityError
from .database import SessionLocal, engine
from .models import Usuario, Base
from .face_utils import get_face_encoding_from_base64
from .webhook_handler import webhook_handler

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Reconhecimento Facial", version="1.0.0")

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

class CadastroRequest(BaseModel):
    cpf: str
    imagem_base64: str

class ReconhecerRequest(BaseModel):
    imagem_base64: str

class WebhookRequest(BaseModel):
    cpf: str

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.post("/webhook")
async def webhook(request: WebhookRequest):
    """Endpoint para receber notificações de reconhecimento"""
    from datetime import datetime
    
    print(f"🎉 WEBHOOK RECEBIDO: CPF {request.cpf} foi reconhecido!")
    print(f"Timestamp: {datetime.now().isoformat()}")
    # Aqui você pode adicionar lógica adicional como:
    # - Registrar log de entrada
    # - Enviar notificação por email/SMS
    # - Atualizar dashboard
    # - Integrar com outros sistemas
    
    return JSONResponse(content={
        "status": "success", 
        "message": f"Entrada registrada para CPF: {request.cpf}",
        "timestamp": datetime.now().isoformat()
    })

@app.get("/test-webhook")
async def test_webhook():
    """Endpoint para testar o webhook manualmente"""
    from datetime import datetime
    
    test_cpf = "12345678901"
    print(f"🧪 Testando webhook para CPF: {test_cpf}")
    
    webhook_success = await webhook_handler.enviar_reconhecimento(test_cpf)
    
    return JSONResponse(content={
        "status": "test_completed",
        "webhook_success": webhook_success,
        "test_cpf": test_cpf,
        "webhook_url": webhook_handler.webhook_url,
        "timestamp": datetime.now().isoformat()
    })

@app.get("/debug-webhook")
async def debug_webhook():
    """Endpoint para debug da configuração do webhook"""
    import httpx
    
    # Testar conectividade
    connectivity_test = "Falha"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(webhook_handler.webhook_url.replace('/webhook', ''))
            connectivity_test = f"Sucesso - Status: {response.status_code}"
    except Exception as e:
        connectivity_test = f"Falha - Erro: {str(e)}"
    
    return JSONResponse(content={
        "webhook_url": webhook_handler.webhook_url,
        "enable_logging": webhook_handler.enable_logging,
        "timeout": webhook_handler.timeout,
        "connectivity_test": connectivity_test,
        "environment": {
            "WEBHOOK_URL": os.getenv('WEBHOOK_URL'),
            "WEBHOOK_LOGGING": os.getenv('WEBHOOK_LOGGING'),
            "WEBHOOK_TIMEOUT": os.getenv('WEBHOOK_TIMEOUT')
        }
    })

@app.post("/cadastro")
async def cadastro(request: CadastroRequest):
    encoding = get_face_encoding_from_base64(request.imagem_base64)
    if encoding is None:
        return JSONResponse(content={"status": "erro", "mensagem": "Rosto não detectado."}, status_code=400)
    db = SessionLocal()
    try:
        usuario = Usuario(cpf=request.cpf, imagem_base64=request.imagem_base64, face_encoding=encoding)
        db.add(usuario)
        db.commit()
        
        # Enviar webhook de novo cadastro
        await webhook_handler.enviar_cadastro(request.cpf)
        
        return JSONResponse(content={"status": "recebido", "cpf": request.cpf})
    except IntegrityError:
        db.rollback()
        return JSONResponse(content={"status": "erro", "mensagem": "CPF já cadastrado."}, status_code=400)
    finally:
        db.close()

from fastapi import status
from sqlalchemy.orm import Session
import numpy as np
import face_recognition

@app.post("/reconhecer")
async def reconhecer(request: ReconhecerRequest):
    encoding = get_face_encoding_from_base64(request.imagem_base64)
    if encoding is None:
        return JSONResponse(content={"status": "erro", "mensagem": "Rosto não detectado."}, status_code=400)
    db: Session = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        for usuario in usuarios:
            known_encoding = np.array(usuario.face_encoding)
            match = face_recognition.compare_faces([known_encoding], np.array(encoding))[0]
            if match:
                print(f"Usuário reconhecido: CPF {usuario.cpf}")
                # Enviar webhook quando usuário for reconhecido
                webhook_success = await webhook_handler.enviar_reconhecimento(usuario.cpf)
                print(f"Webhook enviado: {'Sucesso' if webhook_success else 'Falha'}")
                return JSONResponse(content={"status": "match", "cpf": usuario.cpf})
        return JSONResponse(content={"status": "nao_encontrado"}, status_code=404)
    finally:
        db.close() 