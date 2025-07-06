let currentStream = null;
let imagemBase64 = "";
let currentTab = 'cadastro';

// Função para alternar entre abas
function showTab(tabName) {
    // Esconder todas as abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Mostrar aba selecionada
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    currentTab = tabName;

    // Inicializar câmera para a aba ativa
    if (tabName === 'cadastro') {
        initCamera('video');
    } else {
        initCamera('videoRecon');
    }
}

// Função para inicializar câmera
async function initCamera(videoId) {
    try {
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            } 
        });
        
        const video = document.getElementById(videoId);
        video.srcObject = stream;
        currentStream = stream;
        
        updateStatus('Câmera conectada', true);
    } catch (error) {
        console.error('Erro ao acessar câmera:', error);
        showMessage('Erro ao acessar câmera. Verifique as permissões.', 'error');
        updateStatus('Erro na câmera', false);
    }
}

// Função para atualizar status
function updateStatus(text, connected) {
    const statusText = document.getElementById('statusText');
    const statusDot = document.getElementById('statusDot');
    
    if (statusText && statusDot) {
        statusText.textContent = text;
        statusDot.classList.toggle('connected', connected);
    }
}

// Função para mostrar mensagens
function showMessage(text, type = 'info') {
    const mensagem = document.getElementById('mensagem');
    mensagem.innerHTML = `<div class="message ${type}">${text}</div>`;
    
    if (type === 'success') {
        setTimeout(() => {
            mensagem.innerHTML = '';
        }, 5000);
    }
}

// Função para validar CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    
    if (cpf.length !== 11) return false;
    
    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    // Validar primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = 11 - (soma % 11);
    let dv1 = resto < 2 ? 0 : resto;
    
    // Validar segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = 11 - (soma % 11);
    let dv2 = resto < 2 ? 0 : resto;
    
    return cpf.charAt(9) == dv1 && cpf.charAt(10) == dv2;
}

// Função para formatar CPF
function formatarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar câmera para cadastro
    initCamera('video');

    // Máscara para CPF
    const cpfInput = document.getElementById('cpf');
    cpfInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            e.target.value = value;
        }
    });

    // Capturar foto para cadastro
    document.getElementById('capture').addEventListener('click', function() {
        const video = document.getElementById('video');
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        imagemBase64 = canvas.toDataURL('image/jpeg').split(',')[1];
        
        document.getElementById('fotoPreview').src = 'data:image/jpeg;base64,' + imagemBase64;
        document.getElementById('previewContainer').style.display = 'block';
        document.getElementById('submitCadastro').disabled = false;
        
        showMessage('Foto capturada com sucesso!', 'success');
    });

    // Resetar câmera
    document.getElementById('resetCamera').addEventListener('click', function() {
        initCamera('video');
        document.getElementById('previewContainer').style.display = 'none';
        document.getElementById('submitCadastro').disabled = true;
        imagemBase64 = "";
    });

    // Enviar cadastro
    document.getElementById('cadastroForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const cpf = document.getElementById('cpf').value;
        
        if (!validarCPF(cpf)) {
            showMessage('CPF inválido!', 'error');
            return;
        }
        
        if (!imagemBase64) {
            showMessage('Capture uma foto antes de cadastrar!', 'error');
            return;
        }

        const submitBtn = document.getElementById('submitCadastro');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span>Cadastrando...';

        try {
            const response = await fetch('http://localhost:8001/cadastro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    cpf: cpf.replace(/\D/g, ''),
                    imagem_base64: imagemBase64 
                })
            });

            const data = await response.json();
            
            if (data.status === 'recebido') {
                showMessage('Usuário cadastrado com sucesso!', 'success');
                document.getElementById('cadastroForm').reset();
                document.getElementById('previewContainer').style.display = 'none';
                imagemBase64 = "";
            } else {
                showMessage(data.mensagem || 'Erro ao cadastrar usuário.', 'error');
            }
        } catch (error) {
            showMessage('Erro de conexão com o servidor.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '💾 Cadastrar Usuário';
        }
    });

    // Reconhecimento facial
    document.getElementById('reconhecer').addEventListener('click', async function() {
        const video = document.getElementById('videoRecon');
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        const imagemBase64Recon = canvas.toDataURL('image/jpeg').split(',')[1];
        
        const reconBtn = document.getElementById('reconhecer');
        reconBtn.disabled = true;
        reconBtn.innerHTML = '<span class="loading"></span>Reconhecendo...';
        
        updateStatus('Processando reconhecimento...', true);

        try {
            const response = await fetch('http://localhost:8001/reconhecer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ imagem_base64: imagemBase64Recon })
            });

            const data = await response.json();
            
            if (data.status === 'match') {
                updateStatus(`Reconhecido! CPF: ${data.cpf}`, true);
                showMessage(`Usuário reconhecido: ${data.cpf}`, 'success');
            } else if (data.status === 'nao_encontrado') {
                updateStatus('Rosto não encontrado no banco.', false);
                showMessage('Rosto não encontrado no banco de dados.', 'error');
            } else {
                updateStatus('Erro no reconhecimento.', false);
                showMessage(data.mensagem || 'Erro no reconhecimento.', 'error');
            }
        } catch (error) {
            updateStatus('Erro de conexão.', false);
            showMessage('Erro de conexão com o servidor.', 'error');
        } finally {
            reconBtn.disabled = false;
            reconBtn.innerHTML = '🔍 Reconhecer Rosto';
        }
    });

    // Resetar câmera de reconhecimento
    document.getElementById('resetCameraRecon').addEventListener('click', function() {
        initCamera('videoRecon');
        updateStatus('Aguardando reconhecimento...', true);
    });
}); 