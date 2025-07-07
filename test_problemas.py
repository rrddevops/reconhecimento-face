#!/usr/bin/env python3
"""
Script de diagnóstico para problemas reportados no sistema
"""

import requests
import json
import sys
import time

def test_consulta_cadastros():
    """Testa especificamente o problema da consulta de cadastros"""
    
    print("🔍 Testando problema da consulta de cadastros...")
    print("-" * 50)
    
    # Testar diferentes portas
    ports = [8002, 8000]
    
    for port in ports:
        print(f"\n📡 Testando porta {port}...")
        
        try:
            # Teste 1: Página principal
            response = requests.get(f"http://localhost:{port}/", timeout=5)
            print(f"   Página principal: {'✅' if response.status_code == 200 else '❌'} ({response.status_code})")
            
            # Teste 2: Página de consulta
            response = requests.get(f"http://localhost:{port}/consulta", timeout=5)
            print(f"   Página consulta: {'✅' if response.status_code == 200 else '❌'} ({response.status_code})")
            
            # Teste 3: Endpoint de usuários
            response = requests.get(f"http://localhost:{port}/usuarios", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   Endpoint usuários: ✅ ({data.get('total', 0)} usuários)")
            else:
                print(f"   Endpoint usuários: ❌ ({response.status_code})")
            
            # Se tudo funcionou nesta porta, usar ela
            if response.status_code == 200:
                print(f"\n✅ Porta {port} está funcionando corretamente!")
                return port
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Servidor não está rodando na porta {port}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return None

def test_face_api_loading():
    """Testa se o face-api.js está carregando corretamente"""
    
    print("\n🤖 Testando carregamento do Face-API.js...")
    print("-" * 50)
    
    # URLs para testar
    urls = [
        "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js",
        "https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js"
    ]
    
    for url in urls:
        try:
            print(f"📡 Testando: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ CDN funcionando (tamanho: {len(response.content)} bytes)")
                
                # Verificar se é JavaScript válido
                if "faceapi" in response.text[:1000]:
                    print("   ✅ Conteúdo parece ser face-api.js válido")
                    return True
                else:
                    print("   ⚠️ Conteúdo não parece ser face-api.js")
            else:
                print(f"   ❌ Erro HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro de conexão: {e}")
    
    return False

def test_camera_access():
    """Testa se a câmera está acessível"""
    
    print("\n📹 Testando acesso à câmera...")
    print("-" * 50)
    
    print("ℹ️ Para testar a câmera, abra o navegador e acesse:")
    print("   http://localhost:8002")
    print("   ou")
    print("   http://localhost:8000 (se estiver usando Docker)")
    print("\n💡 Verifique se:")
    print("   • O navegador pede permissão para a câmera")
    print("   • A câmera aparece na tela")
    print("   • Não há erros no console do navegador")

def test_manual_mode():
    """Testa se o modo manual está funcionando"""
    
    print("\n🔧 Testando modo manual...")
    print("-" * 50)
    
    # Determinar porta ativa
    port = test_consulta_cadastros()
    if not port:
        print("❌ Nenhuma porta está funcionando. Verifique se o servidor está rodando.")
        return False
    
    print(f"\n🧪 Testando modo manual na porta {port}...")
    
    try:
        # Teste 1: Cadastro
        print("1️⃣ Testando endpoint de cadastro...")
        response = requests.post(f"http://localhost:{port}/cadastro", 
                               json={"cpf": "12345678901", "imagem_base64": "teste"},
                               timeout=5)
        
        if response.status_code in [200, 400]:  # 400 é esperado para dados inválidos
            print("   ✅ Endpoint de cadastro respondendo")
        else:
            print(f"   ❌ Erro no cadastro: {response.status_code}")
        
        # Teste 2: Reconhecimento
        print("2️⃣ Testando endpoint de reconhecimento...")
        response = requests.post(f"http://localhost:{port}/reconhecer", 
                               json={"imagem_base64": "teste"},
                               timeout=5)
        
        if response.status_code in [200, 400, 404]:  # 404 é esperado para rosto não detectado
            print("   ✅ Endpoint de reconhecimento respondendo")
        else:
            print(f"   ❌ Erro no reconhecimento: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro nos testes: {e}")
        return False

def generate_solutions():
    """Gera soluções para os problemas encontrados"""
    
    print("\n💡 SOLUÇÕES PARA OS PROBLEMAS:")
    print("=" * 50)
    
    print("\n🔧 Problema 1: 'Not Found' na consulta de cadastros")
    print("   Soluções:")
    print("   1. Verifique se o servidor está rodando:")
    print("      python run.py")
    print("   2. Acesse diretamente: http://localhost:8002/consulta")
    print("   3. Use a página de diagnóstico: http://localhost:8002/diagnostico")
    
    print("\n🤖 Problema 2: Detecção automática não funcionando")
    print("   Soluções:")
    print("   1. Verifique sua conexão com a internet")
    print("   2. Tente usar o modo manual (botões funcionam)")
    print("   3. Verifique se não há bloqueio de CDN")
    print("   4. Use a página de diagnóstico para verificar")
    
    print("\n📹 Problema 3: Câmera não funciona")
    print("   Soluções:")
    print("   1. Verifique as permissões do navegador")
    print("   2. Certifique-se de que a câmera não está sendo usada por outro app")
    print("   3. Tente em um navegador diferente")
    
    print("\n🌐 URLs importantes:")
    print("   • Página principal: http://localhost:8002")
    print("   • Consulta de cadastros: http://localhost:8002/consulta")
    print("   • Diagnóstico: http://localhost:8002/diagnostico")

def main():
    """Função principal"""
    print("🚀 Diagnóstico de Problemas - Sistema de Reconhecimento Facial")
    print("=" * 70)
    
    # Teste 1: Consulta de cadastros
    port_ativa = test_consulta_cadastros()
    
    # Teste 2: Face-API.js
    face_api_ok = test_face_api_loading()
    
    # Teste 3: Câmera (instruções)
    test_camera_access()
    
    # Teste 4: Modo manual
    manual_ok = test_manual_mode()
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DO DIAGNÓSTICO:")
    print(f"   🌐 Servidor: {'✅ Funcionando' if port_ativa else '❌ Não encontrado'}")
    print(f"   🤖 Face-API.js: {'✅ Acessível' if face_api_ok else '❌ Problemas de CDN'}")
    print(f"   🔧 Modo Manual: {'✅ Funcionando' if manual_ok else '❌ Problemas'}")
    
    # Gerar soluções
    generate_solutions()
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    if port_ativa:
        print("   1. Acesse a página de diagnóstico: http://localhost:8002/diagnostico")
        print("   2. Use o modo manual se a detecção automática não funcionar")
        print("   3. Teste a consulta de cadastros: http://localhost:8002/consulta")
    else:
        print("   1. Inicie o servidor: python run.py")
        print("   2. Verifique se não há outros processos usando a porta")
        print("   3. Execute este script novamente")
    
    return 0 if port_ativa and manual_ok else 1

if __name__ == "__main__":
    sys.exit(main()) 