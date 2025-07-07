#!/usr/bin/env python3
"""
Script para testar conectividade e dependências do sistema
"""

import requests
import sys
import subprocess
import os

def test_url(url, description):
    """Testa se uma URL está acessível"""
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {description}: OK")
            return True
        else:
            print(f"❌ {description}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description}: Erro - {e}")
        return False

def test_python_dependencies():
    """Testa se as dependências Python estão instaladas"""
    print("\n🔍 Testando dependências Python...")
    
    dependencies = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('face_recognition', 'face_recognition'),
        ('opencv-python', 'OpenCV'),
        ('sqlalchemy', 'SQLAlchemy')
    ]
    
    all_ok = True
    for package, name in dependencies:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {name}: OK")
        except ImportError:
            print(f"❌ {name}: Não instalado")
            all_ok = False
    
    return all_ok

def test_server():
    """Testa se o servidor está rodando"""
    print("\n🌐 Testando servidor local...")
    
    try:
        response = requests.get('http://localhost:8001/', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor local: OK")
            return True
        else:
            print(f"❌ Servidor local: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Servidor local: Erro - {e}")
        return False

def test_cdns():
    """Testa conectividade com CDNs"""
    print("\n📡 Testando conectividade com CDNs...")
    
    cdns = [
        ('https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js', 'CDN Principal (jsdelivr)'),
        ('https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js', 'CDN Alternativa (unpkg)'),
        ('https://cdn.jsdelivr.net/npm/face-api.js/weights/tiny_face_detector_model-weights_manifest.json', 'Modelos de Detecção'),
    ]
    
    all_ok = True
    for url, description in cdns:
        if not test_url(url, description):
            all_ok = False
    
    return all_ok

def test_camera_access():
    """Testa se a câmera pode ser acessada (simulação)"""
    print("\n📹 Testando acesso à câmera...")
    
    # No macOS, verificar se há dispositivos de vídeo
    try:
        result = subprocess.run(['system_profiler', 'SPCameraDataType'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'Camera' in result.stdout:
            print("✅ Câmera detectada no sistema")
            return True
        else:
            print("⚠️ Câmera não detectada ou não acessível")
            return False
    except Exception as e:
        print(f"⚠️ Não foi possível verificar câmera: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 Teste de Conectividade - Sistema de Reconhecimento Facial")
    print("=" * 60)
    
    # Testar dependências Python
    python_ok = test_python_dependencies()
    
    # Testar CDNs
    cdns_ok = test_cdns()
    
    # Testar servidor
    server_ok = test_server()
    
    # Testar câmera
    camera_ok = test_camera_access()
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    print(f"Python Dependencies: {'✅ OK' if python_ok else '❌ PROBLEMAS'}")
    print(f"CDNs: {'✅ OK' if cdns_ok else '❌ PROBLEMAS'}")
    print(f"Servidor Local: {'✅ OK' if server_ok else '❌ PROBLEMAS'}")
    print(f"Câmera: {'✅ OK' if camera_ok else '⚠️ VERIFICAR'}")
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")
    
    if not python_ok:
        print("- Execute: pip3 install -r requirements.txt")
    
    if not cdns_ok:
        print("- Verifique sua conexão com a internet")
        print("- Verifique se há firewall/proxy bloqueando")
        print("- O sistema funcionará em modo manual")
    
    if not server_ok:
        print("- Execute: python3 run.py")
    
    if not camera_ok:
        print("- Verifique permissões de câmera no navegador")
        print("- Verifique se a câmera não está sendo usada por outro app")
    
    if python_ok and cdns_ok and server_ok:
        print("✅ Sistema pronto para uso!")
        print("🌐 Acesse: http://localhost:8001")
    else:
        print("⚠️ Alguns problemas detectados. Verifique as recomendações acima.")

if __name__ == "__main__":
    main() 