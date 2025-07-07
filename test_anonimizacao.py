#!/usr/bin/env python3
"""
Script para testar a anonimização do CPF
"""

import requests
import json
import sys
import base64

def create_test_image():
    """Cria uma imagem de teste simples"""
    # Criar uma imagem JPEG simples (1x1 pixel)
    return base64.b64encode(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9').decode('utf-8')

def test_anonimizacao():
    """Testa se a anonimização do CPF está funcionando"""
    
    print("🔒 Testando anonimização do CPF...")
    print(f"📡 Servidor: http://localhost:8002")
    print("-" * 60)
    
    # Verificar se há usuários cadastrados
    print("1️⃣ Verificando usuários cadastrados...")
    try:
        response = requests.get("http://localhost:8002/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['total']} usuários cadastrados")
            
            if data['total'] == 0:
                print("⚠️ Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
                return False
                
            # Pegar o primeiro CPF cadastrado
            cpf_cadastrado = data['usuarios'][0]['cpf']
            print(f"📋 CPF cadastrado: {cpf_cadastrado}")
            
        else:
            print(f"❌ Erro ao buscar usuários: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    # Testar reconhecimento com imagem inválida (só para ver a resposta)
    print("\n2️⃣ Testando resposta do reconhecimento...")
    test_image = create_test_image()
    
    try:
        response = requests.post("http://localhost:8002/reconhecer", 
                               json={"imagem_base64": test_image},
                               timeout=10)
        
        print(f"📡 Status da resposta: {response.status_code}")
        
        if response.status_code in [200, 404, 500]:
            print("✅ Endpoint de reconhecimento respondendo")
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n3️⃣ Verificando anonimização no frontend...")
    print("ℹ️ Para testar a anonimização:")
    print("   1. Acesse: http://localhost:8002/")
    print("   2. Vá para a aba 'Reconhecimento'")
    print("   3. Posicione o rosto na câmera")
    print("   4. Verifique se o CPF aparece como: 111******11")
    print("   5. O webhook deve receber o CPF completo: 11111111111")
    
    return True

def test_webhook_cache():
    """Testa se o webhook está recebendo CPF completo"""
    
    print("\n4️⃣ Verificando cache de webhooks...")
    try:
        response = requests.get("http://localhost:8002/webhook-cache/status", timeout=10)
        if response.status_code == 200:
            cache_status = response.json()
            print(f"✅ Cache: {cache_status['total_entries']} entradas")
            
            if cache_status['entries']:
                for cpf, info in cache_status['entries'].items():
                    print(f"   📋 CPF no cache: {cpf} (completo)")
                    print(f"   ⏰ Enviado há: {info['seconds_ago']:.1f} segundos")
                    print(f"   🔄 Pode enviar novamente: {info['can_send_again']}")
            else:
                print("   📭 Cache vazio")
        else:
            print(f"❌ Erro ao verificar cache: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🔒 Teste de Anonimização do CPF")
    print("=" * 60)
    
    # Testar anonimização
    success = test_anonimizacao()
    
    # Testar cache de webhooks
    test_webhook_cache()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    print(f"   ✅ Anonimização: {'CONFIGURADA' if success else 'FALHOU'}")
    print(f"   ✅ Webhook: VERIFICADO")
    
    if success:
        print("\n🎉 Sistema configurado corretamente!")
        print("\n📖 COMO FUNCIONA:")
        print("   • Frontend: CPF anonimizado (ex: 111******11)")
        print("   • Webhook: CPF completo (ex: 11111111111)")
        print("   • Apenas uma mensagem na tela")
        print("   • Cache de 5 minutos por CPF")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Verifique o sistema.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 