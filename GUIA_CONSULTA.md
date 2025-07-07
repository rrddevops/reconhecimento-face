# 📋 Guia de Consulta de Cadastros

Este guia explica como usar a nova funcionalidade de consulta e gerenciamento de cadastros do sistema de reconhecimento facial.

## 🚀 Como Acessar

### Opção 1: Pela Interface Web
1. Acesse a página principal: `http://localhost:8002`
2. Clique no botão **"📋 Consultar Cadastros"**
3. Você será redirecionado para a tela de consulta

### Opção 2: Acesso Direto
- URL direta: `http://localhost:8002/consulta`

## 📊 Funcionalidades Disponíveis

### 1. Visualização de Cadastros
- **Lista Completa**: Todos os usuários cadastrados no sistema
- **Fotos dos Usuários**: Miniaturas das fotos de cadastro
- **Informações Detalhadas**: CPF, ID e preview da imagem
- **Layout Responsivo**: Funciona em desktop e mobile

### 2. Estatísticas
- **Total de Cadastros**: Contador em tempo real
- **Atualização Automática**: Dados sempre atualizados

### 3. Gerenciamento
- **Deletar Usuários**: Remover cadastros desnecessários
- **Confirmação de Deleção**: Evita exclusões acidentais
- **Feedback Visual**: Mensagens de sucesso/erro

### 4. Navegação
- **Voltar à Página Principal**: Link para retornar
- **Atualizar Lista**: Botão para recarregar dados

## 🎯 Como Usar

### Visualizando Cadastros
1. A página carrega automaticamente todos os cadastros
2. Cada usuário é exibido em uma linha com:
   - Foto do usuário (miniatura)
   - CPF formatado (ex: 123.456.789-00)
   - ID do cadastro
   - Preview da imagem base64
   - Botão de deletar

### Deletando um Usuário
1. Localize o usuário na lista
2. Clique no botão **"🗑️ Deletar"**
3. Confirme a ação na janela de confirmação
4. O usuário será removido e a lista atualizada

### Atualizando a Lista
- Clique em **"🔄 Atualizar Lista"** para recarregar os dados
- Útil após cadastros ou deleções feitas em outras abas

## 🔧 Endpoints da API

### Listar Usuários
```http
GET /usuarios
```

**Resposta:**
```json
{
  "status": "success",
  "usuarios": [
    {
      "id": 1,
      "cpf": "12345678901",
      "imagem_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
    }
  ],
  "total": 1
}
```

### Deletar Usuário
```http
DELETE /usuarios/{cpf}
```

**Resposta:**
```json
{
  "status": "success",
  "mensagem": "Usuário 12345678901 deletado com sucesso"
}
```

## 🧪 Testando a Funcionalidade

### Script de Teste Automático
Execute o script de teste para verificar se tudo está funcionando:

```bash
python test_consulta.py
```

### Teste Manual via cURL
```bash
# Listar usuários
curl http://localhost:8002/usuarios

# Deletar usuário (substitua CPF_EXEMPLO pelo CPF real)
curl -X DELETE http://localhost:8002/usuarios/CPF_EXEMPLO
```

## 🎨 Interface Visual

### Design Responsivo
- **Desktop**: Layout em grid com todas as informações visíveis
- **Mobile**: Layout adaptado para telas menores
- **Cores**: Gradiente azul/roxo para elementos principais

### Elementos Visuais
- **Cards de Estatísticas**: Fundo branco com sombra
- **Tabela de Usuários**: Cabeçalho colorido e linhas alternadas
- **Botões**: Efeitos hover e transições suaves
- **Ícones**: Emojis para melhor usabilidade

### Estados da Interface
- **Carregando**: Indicador de loading
- **Vazio**: Mensagem quando não há cadastros
- **Erro**: Alertas vermelhos para problemas
- **Sucesso**: Mensagens verdes para ações bem-sucedidas

## 🔍 Troubleshooting

### Problemas Comuns

**Lista não carrega:**
- Verifique se o servidor está rodando
- Confirme a porta correta (8002 para modo manual, 8000 para Docker)
- Verifique o console do navegador para erros

**Erro de conexão:**
- Teste a conectividade: `curl http://localhost:8002/usuarios`
- Verifique se não há firewall bloqueando
- Confirme que o servidor está na porta correta

**Fotos não aparecem:**
- Verifique se as imagens estão em formato base64 válido
- Confirme que o formato da imagem é suportado (JPEG/PNG)

**Deleção falha:**
- Verifique se o CPF existe no sistema
- Confirme que não há erros no console
- Teste via cURL para isolar o problema

### Logs Úteis
- **Console do Navegador**: Erros de JavaScript e requisições
- **Logs do Servidor**: Erros de backend e operações de banco
- **Network Tab**: Requisições HTTP e respostas

## 📱 Compatibilidade

### Navegadores Suportados
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Dispositivos
- ✅ Desktop (Windows, macOS, Linux)
- ✅ Tablet (iPad, Android)
- ✅ Mobile (iPhone, Android)

## 🔒 Segurança

### Considerações
- **CPF Exposto**: Os CPFs são visíveis na interface
- **Imagens Base64**: Dados de imagem podem ser grandes
- **Deleção Permanente**: Não há recuperação automática

### Recomendações
- Use HTTPS em produção
- Implemente autenticação se necessário
- Faça backup regular do banco de dados
- Considere paginação para muitos registros

## 🚀 Próximas Melhorias

### Funcionalidades Planejadas
- [ ] Paginação para grandes volumes
- [ ] Busca e filtros
- [ ] Exportação de dados
- [ ] Edição de cadastros
- [ ] Histórico de alterações
- [ ] Autenticação de usuários

### Otimizações
- [ ] Lazy loading de imagens
- [ ] Cache de dados
- [ ] Compressão de imagens
- [ ] Índices de banco de dados

---

**📞 Suporte**: Para dúvidas ou problemas, consulte a documentação principal ou abra uma issue no repositório. 