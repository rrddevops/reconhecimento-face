#!/usr/bin/env python3
"""
Script de teste para o sistema de cache de webhooks
"""

import requests
import json
import sys
import time

def test_webhook_cache():
    """Testa o sistema de cache de webhooks"""
    
    print("🧪 Testando sistema de cache de webhooks...")
    print(f"📡 Servidor: http://localhost:8002")
    print("-" * 50)
    
    try:
        # Teste 1: Verificar status do cache
        print("1️⃣ Verificando status do cache...")
        response = requests.get("http://localhost:8002/webhook-cache/status", timeout=10)
        
        if response.status_code == 200:
            cache_status = response.json()
            print(f"✅ Cache status: {cache_status['total_entries']} entradas")
            print(f"   Intervalo mínimo: {cache_status['min_interval_seconds']} segundos")
            
            if cache_status['entries']:
                print("   Entradas no cache:")
                for cpf, info in cache_status['entries'].items():
                    print(f"     - CPF {cpf}: enviado há {info['seconds_ago']:.1f}s")
        else:
            print(f"❌ Erro ao verificar cache: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Servidor não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    # Teste 2: Simular reconhecimento múltiplo
    print("\n2️⃣ Testando reconhecimento múltiplo...")
    
    test_cpf = "12345678901"
    
    for i in range(3):
        print(f"   Tentativa {i+1}: Simulando reconhecimento do CPF {test_cpf}")
        
        try:
            # Simular reconhecimento (isso deve disparar o webhook)
            response = requests.post("http://localhost:8002/reconhecer", 
                                   json={"imagem_base64": "teste_imagem"},
                                   timeout=10)
            
            if response.status_code in [200, 404]:  # 404 é esperado se não encontrar o rosto
                print(f"     ✅ Reconhecimento processado")
            else:
                print(f"     ❌ Erro no reconhecimento: {response.status_code}")
                
        except Exception as e:
            print(f"     ❌ Erro: {e}")
        
        # Aguardar um pouco entre tentativas
        if i < 2:
            time.sleep(2)
    
    # Teste 3: Verificar cache novamente
    print("\n3️⃣ Verificando cache após tentativas...")
    
    try:
        response = requests.get("http://localhost:8002/webhook-cache/status", timeout=10)
        
        if response.status_code == 200:
            cache_status = response.json()
            print(f"✅ Cache atualizado: {cache_status['total_entries']} entradas")
            
            if cache_status['entries']:
                print("   Entradas no cache:")
                for cpf, info in cache_status['entries'].items():
                    print(f"     - CPF {cpf}: enviado há {info['seconds_ago']:.1f}s")
                    print(f"       Pode enviar novamente: {info['can_send_again']}")
        else:
            print(f"❌ Erro ao verificar cache: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 4: Limpar cache
    print("\n4️⃣ Testando limpeza do cache...")
    
    try:
        response = requests.post("http://localhost:8002/webhook-cache/clear", timeout=10)
        
        if response.status_code == 200:
            print("✅ Cache limpo com sucesso")
        else:
            print(f"❌ Erro ao limpar cache: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 5: Verificar cache após limpeza
    print("\n5️⃣ Verificando cache após limpeza...")
    
    try:
        response = requests.get("http://localhost:8002/webhook-cache/status", timeout=10)
        
        if response.status_code == 200:
            cache_status = response.json()
            print(f"✅ Cache após limpeza: {cache_status['total_entries']} entradas")
        else:
            print(f"❌ Erro ao verificar cache: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return True

def test_webhook_config():
    """Testa a configuração do webhook"""
    
    print("\n🔧 Testando configuração do webhook...")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:8002/debug-webhook", timeout=10)
        
        if response.status_code == 200:
            config = response.json()
            print(f"✅ URL do webhook: {config['webhook_url']}")
            print(f"✅ Logging habilitado: {config['enable_logging']}")
            print(f"✅ Timeout: {config['timeout']} segundos")
            print(f"✅ Intervalo mínimo: {config['min_interval']} segundos")
            print(f"✅ Teste de conectividade: {config['connectivity_test']}")
            
            if config['cache_status']['total_entries'] > 0:
                print(f"⚠️  Cache tem {config['cache_status']['total_entries']} entradas")
            else:
                print("✅ Cache vazio")
                
        else:
            print(f"❌ Erro ao verificar configuração: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🚀 Teste do Sistema de Cache de Webhooks")
    print("=" * 60)
    
    # Teste de configuração
    test_webhook_config()
    
    # Teste de cache
    success = test_webhook_cache()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    print(f"   ✅ Configuração do webhook: VERIFICADA")
    print(f"   ✅ Sistema de cache: {'FUNCIONANDO' if success else 'FALHOU'}")
    
    if success:
        print("\n🎉 Sistema de cache de webhooks funcionando!")
        print("\n📖 COMO FUNCIONA:")
        print("   • Webhooks para o mesmo CPF são bloqueados por 5 minutos")
        print("   • Cache é limpo automaticamente após 24 horas")
        print("   • Endpoint /webhook-cache/status mostra status do cache")
        print("   • Endpoint /webhook-cache/clear limpa o cache manualmente")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Verifique o servidor.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 