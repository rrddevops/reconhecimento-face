#!/usr/bin/env python3
"""
Script para executar o sistema em modo simples
"""

import sys
import os

# Adicionar o diretório app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from main_simple import app
    import uvicorn
    
    print("🚀 Sistema de Reconhecimento Facial - Modo Simples")
    print("=" * 50)
    print("📝 Funcionalidades disponíveis:")
    print("   ✅ Cadastro de usuários")
    print("   ✅ Reconhecimento simulado")
    print("   ✅ Validação de CPF")
    print("   ✅ Interface web")
    print("   ⚠️ Detecção automática (modo manual)")
    print("=" * 50)
    print("🌐 Acesse: http://localhost:8002")
    print("📊 Status: http://localhost:8002/status")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que as dependências estão instaladas:")
    print("   pip install fastapi uvicorn")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1) 