# Sistema de Reconhecimento Facial

Sistema completo de cadastro e reconhecimento facial usando FastAPI, PostgreSQL e face_recognition, com sistema de webhook para notificações.

## 🚀 Como Executar com Docker

### Opção 1: Docker Compose (Recomendado)
```bash
# Construir e executar todos os serviços
docker-compose up --build

# Para executar em background
docker-compose up -d --build
```

### Opção 2: Execução Local
```bash
# 1. Instalar Dependências
pip install -r requirements.txt

# 2. Configurar PostgreSQL
# Crie um banco de dados chamado `reconhecimento`
# Ajuste a URL de conexão no arquivo `app/database.py`:
DATABASE_URL = 'postgresql://usuario:senha@localhost:5432/reconhecimento'

# 3. Executar a Aplicação
python run.py
```

## 🌐 Acessos
- **Aplicação:** http://localhost:8001
- **Documentação da API:** http://localhost:8001/docs
- **PostgreSQL:** localhost:5433

## 🔧 Endpoints da API
- `POST /cadastro` - Cadastra usuário com CPF e foto
- `POST /reconhecer` - Reconhece rosto e retorna CPF
- `POST /webhook` - Recebe notificações de reconhecimento
- `GET /test-webhook` - Testa o webhook manualmente

## 🔔 Sistema de Webhook

O sistema envia webhooks automaticamente quando:

### **Reconhecimento Facial**
Quando um usuário é reconhecido, o sistema envia:
```json
{
    "cpf": "12345678901"
}
```

### **Novo Cadastro**
Quando um novo usuário é cadastrado:
```json
{
    "cpf": "12345678901"
}
```

### **Configuração do Webhook**

#### Variáveis de Ambiente:
- `WEBHOOK_URL`: URL para onde enviar os webhooks (padrão: http://localhost:8000/webhook)
- `WEBHOOK_LOGGING`: Habilitar logs do webhook (true/false, padrão: true)
- `WEBHOOK_TIMEOUT`: Timeout em segundos (padrão: 10)

#### Exemplo de uso:
```bash
# Testar webhook manualmente
curl --location 'http://localhost:8000/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "cpf": "11111111111"
}'

# Testar envio de webhook
curl --location 'http://localhost:8001/test-webhook'
```

## 📁 Estrutura do Projeto
```
sistema-reconhecimento/
├── app/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Modelos do banco
│   ├── database.py          # Conexão PostgreSQL
│   ├── face_utils.py        # Processamento facial
│   ├── webhook_handler.py   # Gerenciamento de webhooks
│   └── static/              # Interface web
│       ├── index.html
│       ├── css/style.css
│       └── js/app.js
├── docker-compose.yml       # Configuração Docker
├── Dockerfile              # Imagem da aplicação
├── requirements.txt
├── run.py
└── README.md
```

## 🐳 Comandos Docker Úteis
```bash
# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Reconstruir apenas a aplicação
docker-compose up --build app

# Acessar container da aplicação
docker-compose exec app bash
```

## 🔧 Integração com Outros Sistemas

O webhook pode ser usado para:
- ✅ Registrar entrada/saída de funcionários
- ✅ Atualizar dashboards em tempo real
- ✅ Enviar notificações por email/SMS
- ✅ Integrar com sistemas de controle de acesso
- ✅ Logs de auditoria
- ✅ Análise de dados de presença 