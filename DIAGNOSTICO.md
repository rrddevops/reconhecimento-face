# 🔍 Diagnóstico - Problema de Conexão

## 🚨 Problema Reportado
- ❌ "Erro de conexão com o servidor" ao clicar no botão de reconhecimento manual
- ❌ Reconhecimento automático não funcionou

## ✅ Status do Servidor
- ✅ Servidor rodando na porta 8002
- ✅ Endpoints funcionando (testado via curl)
- ✅ Página principal carregando

## 🔧 Passos de Diagnóstico

### 1. **Teste Básico de Conexão**
Acesse: **http://localhost:8002/static/test_server.html**

Clique nos botões para testar:
- **"Testar Status"** - Deve mostrar status do servidor
- **"Testar Reconhecimento"** - Deve mostrar "nao_encontrado"
- **"Testar Cadastro"** - Deve mostrar sucesso

### 2. **Verificar Console do Navegador**
1. Abra **http://localhost:8002**
2. Pressione **F12** para abrir DevTools
3. Vá na aba **"Console"**
4. Tente fazer um reconhecimento manual
5. Procure por mensagens de erro

### 3. **Possíveis Erros e Soluções**

#### ❌ Erro: "Failed to fetch"
**Causa:** Problema de CORS ou servidor não acessível
**Solução:** 
- Verifique se o servidor está rodando: `curl http://localhost:8002/status`
- Teste em modo incógnito
- Verifique se não há firewall bloqueando

#### ❌ Erro: "Network Error"
**Causa:** Servidor parou ou porta bloqueada
**Solução:**
- Reinicie o servidor: `python3 run_simple.py`
- Verifique se a porta 8002 está livre: `lsof -i :8002`

#### ❌ Erro: "CORS policy"
**Causa:** Política de CORS do navegador
**Solução:**
- O servidor já tem CORS configurado
- Teste em outro navegador
- Verifique se está acessando via `http://localhost:8002`

### 4. **Teste Manual via Console**

No console do navegador (F12), execute:

```javascript
// Teste de status
fetch('http://localhost:8002/status')
  .then(r => r.json())
  .then(d => console.log('Status:', d))
  .catch(e => console.error('Erro:', e));

// Teste de reconhecimento
fetch('http://localhost:8002/reconhecer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ imagem_base64: 'teste' })
})
.then(r => r.json())
.then(d => console.log('Reconhecimento:', d))
.catch(e => console.error('Erro:', e));
```

### 5. **Verificar Logs do Servidor**

O servidor mostra logs no terminal. Procure por:
- ✅ "Usuário cadastrado: [CPF]"
- ✅ "Usuário reconhecido (simulado): [CPF]"
- ❌ Erros de conexão ou processamento

## 🎯 Teste Completo

### Passo 1: Cadastro
1. Acesse http://localhost:8002
2. Vá na aba "Cadastro"
3. Digite CPF: `123.456.789-01`
4. Clique em "Capturar Foto"
5. Clique em "Cadastrar Usuário"
6. Verifique se aparece mensagem de sucesso

### Passo 2: Reconhecimento
1. Vá na aba "Reconhecimento"
2. Clique em "Reconhecimento Manual"
3. Verifique se aparece o CPF cadastrado

### Passo 3: Verificar Status
1. Acesse http://localhost:8002/status
2. Deve mostrar `"usuarios_cadastrados": 1`

## 🆘 Se Nada Funcionar

### Opção 1: Reiniciar Tudo
```bash
# Parar servidor (Ctrl+C)
# Reiniciar
source venv/bin/activate
python3 run_simple.py
```

### Opção 2: Usar Porta Diferente
Se a porta 8002 estiver ocupada, mude para 8003:
1. Edite `run_simple.py`
2. Mude `port=8002` para `port=8003`
3. Reinicie o servidor
4. Acesse http://localhost:8003

### Opção 3: Verificar Firewall
```bash
# macOS
sudo pfctl -s all

# Verificar se localhost está bloqueado
ping localhost
```

## 📊 Resultado Esperado

Após os testes, você deve ver:
- ✅ Página carregando sem erros
- ✅ Console sem erros de rede
- ✅ Cadastro funcionando
- ✅ Reconhecimento manual funcionando
- ✅ Status mostrando usuários cadastrados

## 🔄 Próximos Passos

Se o problema persistir:
1. **Screenshot** do console com erros
2. **Logs** do servidor
3. **Resultado** dos testes acima

Com essas informações, posso identificar exatamente onde está o problema! 🎯 