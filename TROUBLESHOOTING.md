# 🔧 Troubleshooting - Problemas Comuns

Este guia ajuda a resolver problemas comuns do sistema de reconhecimento facial.

## 🎥 Problemas de Câmera

### ❌ "Erro ao acessar câmera"

**Causas possíveis:**
1. Permissões do navegador bloqueadas
2. Câmera sendo usada por outro aplicativo
3. Driver de câmera não instalado
4. Navegador não suporta getUserMedia

**Soluções:**

#### 1. Verificar Permissões do Navegador
- **Chrome/Edge:** Clique no ícone de câmera na barra de endereços
- **Firefox:** Clique no ícone de câmera na barra de endereços
- **Safari:** Vá em Safari > Preferências > Sites > Câmera

#### 2. Verificar se a Câmera está em Uso
```bash
# macOS
sudo lsof | grep -i camera

# Windows
# Verificar no Gerenciador de Tarefas > Processos
```

#### 3. Testar Câmera em Outro Site
- Acesse: https://webcamtests.com/
- Verifique se a câmera funciona

#### 4. Reiniciar Navegador
- Feche completamente o navegador
- Abra novamente e teste

## 🤖 Problemas de Detecção Facial

### ❌ "Erro ao carregar biblioteca de detecção facial"

**Causas possíveis:**
1. Problema de conectividade com CDN
2. Bloqueio de firewall/proxy
3. Versão incompatível do navegador
4. JavaScript desabilitado

**Soluções:**

#### 1. Verificar Conectividade
```bash
# Testar acesso às CDNs
curl -I https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js
curl -I https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js
```

#### 2. Verificar Console do Navegador
- Pressione F12 para abrir DevTools
- Vá na aba "Console"
- Procure por erros relacionados a:
  - `faceapi`
  - `CORS`
  - `Network`

#### 3. Testar em Modo Incógnito
- Abra o navegador em modo incógnito
- Acesse o sistema
- Verifique se funciona

#### 4. Verificar JavaScript
- Certifique-se de que JavaScript está habilitado
- Desabilite extensões que possam interferir

### ⚠️ "Detecção indisponível"

**O que significa:**
- A biblioteca face-api.js não conseguiu carregar
- O sistema funciona em modo manual

**Como proceder:**
1. Use o botão "Reconhecimento Manual"
2. O sistema ainda funciona, mas sem detecção automática
3. Verifique os logs no console para mais detalhes

## 🌐 Problemas de Rede

### ❌ "Erro de conexão com o servidor"

**Verificar se o servidor está rodando:**
```bash
# Verificar se a porta 8001 está em uso
lsof -i :8001

# Testar conexão
curl http://localhost:8001/
```

**Reiniciar o servidor:**
```bash
# Parar servidor atual (Ctrl+C)
# Executar novamente
python3 run.py
```

## 🔧 Soluções por Sistema Operacional

### macOS

#### Permissões de Câmera
1. **Sistema:** Preferências do Sistema > Segurança e Privacidade > Câmera
2. **Navegador:** Adicione seu navegador à lista de aplicativos permitidos
3. **Reinicie** o navegador após alterações

#### Problemas de Python
```bash
# Verificar versão do Python
python3 --version

# Instalar dependências
pip3 install -r requirements.txt

# Executar com python3
python3 run.py
```

### Windows

#### Permissões de Câmera
1. **Configurações:** Configurações > Privacidade > Câmera
2. **Navegador:** Permitir acesso à câmera
3. **Verificar drivers** da câmera no Gerenciador de Dispositivos

#### Problemas de Python
```bash
# Verificar se Python está no PATH
python --version

# Se não funcionar, tente:
py --version
```

### Linux

#### Permissões de Câmera
```bash
# Verificar dispositivos de vídeo
ls /dev/video*

# Verificar permissões
ls -la /dev/video*

# Se necessário, adicionar usuário ao grupo video
sudo usermod -a -G video $USER
```

## 🧪 Testes de Diagnóstico

### Teste 1: Câmera Básica
```javascript
// No console do navegador
navigator.mediaDevices.getUserMedia({video: true})
  .then(stream => console.log('Câmera OK'))
  .catch(err => console.error('Erro câmera:', err));
```

### Teste 2: Face-API.js
```javascript
// No console do navegador
if (typeof faceapi !== 'undefined') {
  console.log('Face-API.js carregado');
} else {
  console.log('Face-API.js não carregado');
}
```

### Teste 3: Conectividade
```bash
# Testar acesso ao servidor
curl -v http://localhost:8001/

# Testar endpoints da API
curl -X POST http://localhost:8001/test-cpf/12345678901
```

## 📊 Logs Úteis

### Console do Navegador
Procure por estas mensagens:
- ✅ "Face-API.js carregado com sucesso"
- ✅ "Câmera conectada"
- ❌ "Erro ao carregar Face-API.js"
- ❌ "Erro ao acessar câmera"

### Logs do Servidor
```bash
# Executar com logs detalhados
python3 run.py 2>&1 | tee server.log
```

## 🆘 Contato para Suporte

Se os problemas persistirem:

1. **Coletar informações:**
   - Sistema operacional e versão
   - Navegador e versão
   - Logs do console (F12)
   - Logs do servidor

2. **Descrever o problema:**
   - O que estava tentando fazer
   - Mensagens de erro exatas
   - Passos para reproduzir

3. **Anexar screenshots:**
   - Interface do sistema
   - Console do navegador
   - Mensagens de erro

## 🔄 Modo de Emergência

Se nada funcionar, o sistema ainda pode ser usado em modo manual:

1. **Cadastro:** Use o botão "Capturar Foto" manualmente
2. **Reconhecimento:** Use o botão "Reconhecimento Manual"
3. **Funcionalidade:** Todas as funcionalidades principais continuam funcionando

O modo manual é mais lento, mas garante que o sistema funcione mesmo com problemas de detecção automática. 