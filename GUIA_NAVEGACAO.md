# 🧭 Guia de Navegação - Sistema de Reconhecimento Facial

## 📋 Problemas Comuns de Navegação

### ❌ "Página não encontrada" na consulta de cadastros

**Sintomas:**
- Erro 404 ao acessar `/consulta`
- Link "📋 Consultar Cadastros" não funciona
- Página em branco ou erro de servidor

**Soluções:**

#### 1. **Verificar se o servidor está rodando**
```bash
# Verificar se o servidor está ativo
curl http://localhost:8002/

# Verificar endpoint de consulta
curl http://localhost:8002/consulta
```

#### 2. **Verificar porta correta**
- **Desenvolvimento local**: Porta 8002
- **Docker**: Porta 8000 (mapeada para 8002 externamente)

#### 3. **Acessar URLs diretas**
```
http://localhost:8002/consulta
http://localhost:8002/diagnostico
http://localhost:8002/teste-deteccao
http://localhost:8002/teste-navegacao
```

#### 4. **Usar página de teste de navegação**
Acesse: `http://localhost:8002/teste-navegacao`

Esta página testa automaticamente:
- ✅ Links entre páginas
- ✅ Endpoints da API
- ✅ Conectividade do servidor

### 🔧 **Diagnóstico Automático**

#### Página de Diagnóstico
Acesse: `http://localhost:8002/diagnostico`

Verifica:
- ✅ Status do servidor
- ✅ Endpoints disponíveis
- ✅ Configuração de webhooks
- ✅ Banco de dados

#### Página de Teste de Navegação
Acesse: `http://localhost:8002/teste-navegacao`

Testa:
- ✅ Navegação entre páginas
- ✅ Links da página principal
- ✅ Endpoints da API
- ✅ Conectividade

## 🚀 **Soluções Rápidas**

### **Problema 1: Link não funciona**
```bash
# Solução: Acessar URL direta
http://localhost:8002/consulta
```

### **Problema 2: Erro 404**
```bash
# Verificar se o servidor está rodando
ps aux | grep python

# Reiniciar servidor se necessário
python run.py
```

### **Problema 3: Porta incorreta**
```bash
# Verificar porta em uso
lsof -i :8002
lsof -i :8000

# Ajustar URL conforme necessário
```

## 📱 **Interface de Navegação**

### **Links Disponíveis na Página Principal**
- 🏠 **Página Principal**: `/` ou `index.html`
- 📋 **Consultar Cadastros**: `/consulta`
- 🔧 **Diagnóstico**: `/diagnostico`
- 🤖 **Teste Detecção**: `/teste-deteccao`
- 🧭 **Teste Navegação**: `/teste-navegacao`

### **Endpoints da API**
- `GET /` - Página principal
- `GET /consulta` - Página de consulta
- `GET /diagnostico` - Página de diagnóstico
- `GET /teste-deteccao` - Página de teste de detecção
- `GET /teste-navegacao` - Página de teste de navegação
- `GET /usuarios` - Lista de usuários (API)
- `DELETE /usuarios/{cpf}` - Deletar usuário (API)

## 🔍 **Troubleshooting Detalhado**

### **Passo 1: Verificar Servidor**
```bash
# Verificar se o servidor está rodando
curl -v http://localhost:8002/

# Se não responder, reiniciar:
python run.py
```

### **Passo 2: Testar Endpoints**
```bash
# Testar página principal
curl http://localhost:8002/

# Testar consulta
curl http://localhost:8002/consulta

# Testar API de usuários
curl http://localhost:8002/usuarios
```

### **Passo 3: Verificar Logs**
```bash
# Ver logs do servidor
tail -f logs/app.log

# Ou verificar console onde o servidor está rodando
```

### **Passo 4: Usar Página de Diagnóstico**
1. Acesse: `http://localhost:8002/diagnostico`
2. Verifique todos os status
3. Identifique problemas específicos

## 🐳 **Docker - Problemas Específicos**

### **Problema: Porta incorreta no Docker**
```bash
# Verificar mapeamento de portas
docker ps

# Verificar logs do container
docker logs <container_id>

# Acessar porta correta
http://localhost:8000/consulta  # Docker
http://localhost:8002/consulta  # Desenvolvimento
```

### **Solução: Ajustar URL no frontend**
```javascript
// Determinar porta baseado no ambiente
const isDocker = window.location.hostname === 'localhost' && window.location.port === '8000';
const serverPort = isDocker ? '8000' : '8002';
```

## 📊 **Monitoramento**

### **Endpoints de Status**
- `GET /debug-webhook` - Status completo do webhook
- `GET /webhook-cache/status` - Status do cache de webhooks
- `GET /diagnostico` - Diagnóstico geral do sistema

### **Logs Importantes**
- Carregamento de páginas
- Erros de conexão
- Problemas de roteamento
- Status de endpoints

## ✅ **Checklist de Verificação**

### **Antes de Reportar Problema**
- [ ] Servidor está rodando?
- [ ] Porta correta está sendo usada?
- [ ] URL direta funciona?
- [ ] Página de diagnóstico foi testada?
- [ ] Logs foram verificados?

### **Para Resolver Problema**
- [ ] Reiniciar servidor
- [ ] Verificar porta
- [ ] Testar URL direta
- [ ] Usar página de diagnóstico
- [ ] Verificar logs
- [ ] Testar navegação

## 🆘 **Suporte**

### **Se o problema persistir:**
1. Use a página de diagnóstico: `/diagnostico`
2. Use a página de teste de navegação: `/teste-navegacao`
3. Verifique os logs do servidor
4. Teste URLs diretas
5. Reporte o problema com detalhes específicos

### **Informações para Reportar:**
- URL que não funciona
- Mensagem de erro exata
- Resultado da página de diagnóstico
- Logs do servidor
- Ambiente (Docker ou desenvolvimento local) 