# Sistema de Reconhecimento Facial

Um sistema completo de reconhecimento facial com detecção automática de rostos, desenvolvido em Python com FastAPI e JavaScript.

## 🚀 Funcionalidades

### ✨ Recursos Principais
- **Detecção Automática de Rostos**: O sistema detecta automaticamente rostos na câmera usando face-api.js
- **Reconhecimento Automático**: Realiza reconhecimento facial automaticamente quando um rosto é detectado
- **Cadastro de Usuários**: Interface para cadastrar novos usuários com CPF e foto
- **Consulta de Cadastros**: Tela para visualizar, gerenciar e deletar usuários cadastrados
- **Validação de CPF**: Validação completa de CPF brasileiro
- **Interface Moderna**: Design responsivo e intuitivo
- **Webhooks**: Sistema de notificações para reconhecimentos

### 🔍 Detecção Automática
- **Detecção em Tempo Real**: Monitora continuamente a câmera para detectar rostos
- **Indicadores Visuais**: Mostra status de detecção em tempo real
- **Reconhecimento Inteligente**: Aguarda estabilização do rosto antes de processar
- **Retângulos de Detecção**: Desenha retângulos ao redor dos rostos detectados

### 📱 Interface do Usuário
- **Abas Separadas**: Cadastro e reconhecimento em abas distintas
- **Indicadores de Status**: Feedback visual do estado do sistema
- **Mensagens Informativas**: Notificações claras sobre o que está acontecendo
- **Design Responsivo**: Funciona em diferentes tamanhos de tela

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **face_recognition**: Biblioteca Python para reconhecimento facial
- **OpenCV**: Processamento de imagens
- **PostgreSQL**: Banco de dados (configurável)

### Frontend
- **JavaScript**: Lógica da interface
- **face-api.js**: Detecção facial no navegador
- **HTML5/CSS3**: Interface moderna e responsiva
- **Canvas API**: Processamento de vídeo em tempo real

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- Node.js (opcional, para desenvolvimento)
- PostgreSQL (opcional, SQLite por padrão)

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd reconhecimento-face
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente (opcional)
```bash
# Para webhooks
export WEBHOOK_URL="https://seu-webhook.com/webhook"
export WEBHOOK_LOGGING="true"
export WEBHOOK_TIMEOUT="5"

# Para banco de dados PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

### 4. Execute o sistema
```bash
python run.py
```

O sistema estará disponível em `http://localhost:8001`

## 🎯 Como Usar

### Cadastro de Usuários
1. Acesse a aba "Cadastro"
2. Digite o CPF do usuário
3. Posicione o rosto na área de captura
4. O sistema detectará automaticamente o rosto
5. Clique em "Capturar Foto" para confirmar
6. Clique em "Cadastrar Usuário"

### Reconhecimento Automático
1. Acesse a aba "Reconhecimento"
2. Posicione o rosto na área de captura
3. **O sistema detectará automaticamente o rosto e fará o reconhecimento**
4. Aguarde o resultado do reconhecimento
5. O CPF do usuário será exibido se reconhecido

### Reconhecimento Manual
- Use o botão "Reconhecimento Manual" para forçar um reconhecimento
- Útil quando a detecção automática não funcionar como esperado

### Consulta de Cadastros
1. Clique em "📋 Consultar Cadastros" na página principal
2. Visualize todos os usuários cadastrados no sistema
3. Veja estatísticas de cadastros
4. Delete usuários se necessário
5. Atualize a lista com o botão "🔄 Atualizar Lista"

### Páginas de Teste e Diagnóstico
- **🔧 Diagnóstico**: `/diagnostico` - Verifica status do sistema
- **🤖 Teste Detecção**: `/teste-deteccao` - Testa detecção automática
- **🧭 Teste Navegação**: `/teste-navegacao` - Verifica links e navegação

### Sistema de Cache de Webhooks
- **Prevenção de Duplicatas**: Webhooks para o mesmo CPF são bloqueados por 5 minutos
- **Cache Inteligente**: Entradas antigas são removidas automaticamente após 24 horas
- **Monitoramento**: Endpoints para verificar status do cache:
  - `GET /webhook-cache/status` - Ver status do cache
  - `POST /webhook-cache/clear` - Limpar cache manualmente
  - `GET /debug-webhook` - Debug completo da configuração

### Privacidade e Anonimização
- **CPF Anonimizado na Tela**: Exibe apenas primeiros 3 e últimos 2 dígitos (ex: 111******11)
- **CPF Completo no Webhook**: Envia o CPF completo para notificações
- **Mensagem Única**: Apenas uma notificação na tela por reconhecimento

## 🔧 Configuração

### Webhooks
O sistema pode enviar notificações quando um usuário é reconhecido:

```bash
# Configurar URL do webhook
export WEBHOOK_URL="https://seu-servico.com/webhook"

# Habilitar logs de webhook
export WEBHOOK_LOGGING="true"

# Timeout para webhooks (segundos)
export WEBHOOK_TIMEOUT="5"
```

### Banco de Dados
Por padrão, o sistema usa SQLite. Para usar PostgreSQL:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## 📊 Estrutura do Projeto

```
reconhecimento-face/
├── app/
│   ├── main.py              # API FastAPI
│   ├── database.py          # Configuração do banco
│   ├── models.py            # Modelos SQLAlchemy
│   ├── face_utils.py        # Utilitários de reconhecimento
│   ├── webhook_handler.py   # Gerenciador de webhooks
│   └── static/              # Arquivos estáticos
│       ├── index.html       # Interface principal
│       ├── consulta.html    # Tela de consulta de cadastros
│       ├── css/style.css    # Estilos
│       └── js/app.js        # JavaScript da interface
├── requirements.txt         # Dependências Python
├── run.py                  # Script de execução
├── test_consulta.py        # Script de teste da consulta
└── README.md               # Documentação
```

## 🚀 Funcionalidades Avançadas

### Detecção Automática
- **Monitoramento Contínuo**: Verifica a cada 100ms por rostos
- **Estabilização**: Aguarda 1 segundo após detecção antes de processar
- **Prevenção de Duplicatas**: Evita processamento simultâneo
- **Indicadores Visuais**: Feedback em tempo real do status

### Performance
- **Otimização de Memória**: Limpeza automática de recursos
- **Processamento Assíncrono**: Não bloqueia a interface
- **Cache de Detecção**: Evita reprocessamento desnecessário

## 🔍 Troubleshooting

### Problemas Comuns

**Câmera não funciona:**
- Verifique as permissões do navegador
- Certifique-se de que a câmera não está sendo usada por outro aplicativo

**Detecção não funciona:**
- Verifique se o face-api.js carregou corretamente
- Certifique-se de que há boa iluminação
- Posicione o rosto no centro da área de captura

**Reconhecimento falha:**
- Verifique se o usuário está cadastrado
- Certifique-se de que a foto de cadastro é clara
- Tente reposicionar o rosto

### Logs
O sistema gera logs detalhados no console para debug:
- Carregamento de bibliotecas
- Detecção de rostos
- Processamento de reconhecimento
- Envio de webhooks

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através dos canais disponíveis. 