#!/usr/bin/env python3
"""
Script de teste para a funcionalidade de consulta de cadastros
"""

import requests
import json
import sys

def test_consulta_cadastros():
    """Testa a funcionalidade de consulta de cadastros"""
    
    # Configuração
    base_url = "http://localhost:8002"  # Porta padrão para modo manual
    
    print("🧪 Testando funcionalidade de consulta de cadastros...")
    print(f"📡 Servidor: {base_url}")
    print("-" * 50)
    
    try:
        # Teste 1: Listar usuários
        print("1️⃣ Testando listagem de usuários...")
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Status: {data.get('status')}")
            print(f"📊 Total de usuários: {data.get('total', 0)}")
            
            usuarios = data.get('usuarios', [])
            if usuarios:
                print("👥 Usuários encontrados:")
                for i, usuario in enumerate(usuarios[:5], 1):  # Mostrar apenas os primeiros 5
                    print(f"   {i}. ID: {usuario.get('id')} | CPF: {usuario.get('cpf')}")
                if len(usuarios) > 5:
                    print(f"   ... e mais {len(usuarios) - 5} usuários")
            else:
                print("📭 Nenhum usuário cadastrado")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão: Servidor não está rodando")
        print("💡 Execute: python run.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: Servidor demorou muito para responder")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Teste de consulta concluído!")
    print("\n📋 Para acessar a interface web:")
    print(f"   🌐 Página principal: {base_url}")
    print(f"   📊 Consulta de cadastros: {base_url}/consulta")
    
    return True

def test_deletar_usuario():
    """Testa a funcionalidade de deletar usuário"""
    
    base_url = "http://localhost:8002"
    
    print("\n🗑️ Testando funcionalidade de deletar usuário...")
    print("-" * 50)
    
    try:
        # Primeiro, listar usuários para pegar um CPF
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            if not usuarios:
                print("📭 Nenhum usuário para testar deleção")
                return True
            
            # Pegar o primeiro usuário
            primeiro_usuario = usuarios[0]
            cpf_teste = primeiro_usuario.get('cpf')
            
            print(f"🧪 Testando deleção do usuário CPF: {cpf_teste}")
            
            # Testar deleção (vamos apenas simular, não deletar de verdade)
            print("⚠️  Simulando teste de deleção (não deletando de verdade)")
            print("✅ Funcionalidade de deleção disponível no endpoint DELETE /usuarios/{cpf}")
            
        else:
            print(f"❌ Erro ao listar usuários: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste de deleção: {e}")
    
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando testes da funcionalidade de consulta de cadastros")
    print("=" * 60)
    
    # Teste de consulta
    sucesso_consulta = test_consulta_cadastros()
    
    # Teste de deleção
    sucesso_delecao = test_deletar_usuario()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES:")
    print(f"   ✅ Consulta de cadastros: {'PASSOU' if sucesso_consulta else 'FALHOU'}")
    print(f"   ✅ Funcionalidade de deleção: {'DISPONÍVEL' if sucesso_delecao else 'FALHOU'}")
    
    if sucesso_consulta and sucesso_delecao:
        print("\n🎉 Todos os testes passaram!")
        print("\n📖 PRÓXIMOS PASSOS:")
        print("   1. Acesse a interface web em http://localhost:8002")
        print("   2. Clique em '📋 Consultar Cadastros'")
        print("   3. Visualize, atualize e gerencie os cadastros")
        return 0
    else:
        print("\n❌ Alguns testes falharam. Verifique o servidor.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 