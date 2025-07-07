let currentStream = null;
let imagemBase64 = "";
let currentTab = 'cadastro';
let faceDetectionInterval = null;
let isProcessingRecognition = false;

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

    // Parar detecção anterior
    stopFaceDetection();

    // Inicializar câmera para a aba ativa
    if (tabName === 'cadastro') {
        initCamera('video');
        startFaceDetection('video', 'canvasCadastro', 'faceIndicatorCadastro', 'cadastro');
    } else {
        initCamera('videoRecon');
        startFaceDetection('videoRecon', 'canvasRecon', 'faceIndicatorRecon', 'reconhecimento');
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

// Função para inicializar face-api.js
async function initFaceAPI() {
    try {
        console.log('Iniciando carregamento do Face-API.js...');
        
        // Verificar se faceapi está disponível
        if (typeof faceapi === 'undefined') {
            console.error('Face-API.js não está carregado');
            return false;
        }
        
        // Carregar modelos com timeout e retry
        const loadModel = async (modelName, modelPath) => {
            const maxRetries = 3;
            for (let i = 0; i < maxRetries; i++) {
                try {
                    console.log(`Carregando ${modelName}... (tentativa ${i + 1})`);
                    await faceapi.nets[modelName].loadFromUri(modelPath);
                    console.log(`${modelName} carregado com sucesso`);
                    return true;
                } catch (error) {
                    console.error(`Erro ao carregar ${modelName} (tentativa ${i + 1}):`, error);
                    if (i === maxRetries - 1) throw error;
                    await new Promise(resolve => setTimeout(resolve, 1000)); // Aguardar 1s antes de tentar novamente
                }
            }
        };
        
        // Tentar diferentes CDNs para carregar modelos
        const cdnUrls = [
            'https://cdn.jsdelivr.net/npm/face-api.js/weights',
            'https://unpkg.com/face-api.js/weights',
            'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights'
        ];
        
        let modelLoaded = false;
        for (const cdnUrl of cdnUrls) {
            try {
                console.log(`Tentando carregar modelos de: ${cdnUrl}`);
                await loadModel('tinyFaceDetector', cdnUrl);
                modelLoaded = true;
                break;
            } catch (error) {
                console.warn(`Falha ao carregar de ${cdnUrl}:`, error);
                continue;
            }
        }
        
        if (modelLoaded) {
            console.log('Face-API.js carregado com sucesso');
            return true;
        } else {
            throw new Error('Não foi possível carregar modelos de nenhuma CDN');
        }
        
    } catch (error) {
        console.error('Erro ao carregar Face-API.js:', error);
        return false;
    }
}

// Função para iniciar detecção facial
async function startFaceDetection(videoId, canvasId, indicatorId, mode) {
    const video = document.getElementById(videoId);
    const canvas = document.getElementById(canvasId);
    const indicator = document.getElementById(indicatorId);
    
    // Aguardar o vídeo carregar
    await new Promise(resolve => {
        video.addEventListener('loadeddata', resolve, { once: true });
    });

    // Configurar canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');

    // Verificar se face-api.js está disponível
    if (typeof faceapi === 'undefined') {
        console.warn('Face-API.js não disponível, usando modo manual');
        indicator.querySelector('.face-status').innerHTML = '⚠️ Modo manual (detecção não disponível)';
        return;
    }

    // Verificar se os modelos foram carregados
    if (!faceapi.nets.tinyFaceDetector.isLoaded) {
        console.warn('Modelos de detecção não carregados, usando modo manual');
        indicator.querySelector('.face-status').innerHTML = '⚠️ Modo manual (modelos não carregados)';
        return;
    }

    // Iniciar detecção contínua
    faceDetectionInterval = setInterval(async () => {
        if (video.paused || video.ended) return;

        try {
            // Detectar rostos com timeout
            const detectionPromise = faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
            const detections = await Promise.race([
                detectionPromise,
                new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 2000))
            ]);

            // Limpar canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (detections && detections.length > 0) {
                // Rosto detectado
                indicator.classList.add('detected');
                indicator.classList.remove('processing');
                indicator.querySelector('.face-status').innerHTML = '✅ Rosto detectado';

                // Desenhar retângulos ao redor dos rostos
                detections.forEach(detection => {
                    const box = detection.box || detection.detection?.box;
                    if (box) {
                        ctx.strokeStyle = '#28a745';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(box.x, box.y, box.width, box.height);
                    }
                });

                // Se estiver no modo reconhecimento e não estiver processando, fazer reconhecimento automático
                if (mode === 'reconhecimento' && !isProcessingRecognition && detections.length === 1) {
                    setTimeout(() => {
                        performAutoRecognition();
                    }, 1000); // Aguardar 1 segundo para estabilizar
                }
            } else {
                // Nenhum rosto detectado
                indicator.classList.remove('detected', 'processing');
                indicator.querySelector('.face-status').innerHTML = '🔍 Procurando rosto...';
            }
        } catch (error) {
            console.error('Erro na detecção facial:', error);
            indicator.classList.remove('detected', 'processing');
            indicator.querySelector('.face-status').innerHTML = '⚠️ Modo manual (detecção falhou)';
        }
    }, 200); // Verificar a cada 200ms (reduzido para melhor performance)
}

// Função para parar detecção facial
function stopFaceDetection() {
    if (faceDetectionInterval) {
        clearInterval(faceDetectionInterval);
        faceDetectionInterval = null;
    }
}

// Variável para controlar reconhecimento automático
let lastAutoRecognitionTime = 0;
const AUTO_RECOGNITION_COOLDOWN = 5000; // 5 segundos de cooldown

// Função para reconhecimento automático
async function performAutoRecognition() {
    if (isProcessingRecognition) return;
    
    // Verificar cooldown para evitar múltiplas chamadas
    const now = Date.now();
    if (now - lastAutoRecognitionTime < AUTO_RECOGNITION_COOLDOWN) {
        console.log('⏰ Cooldown ativo, ignorando reconhecimento automático');
        return;
    }
    
    lastAutoRecognitionTime = now;
    isProcessingRecognition = true;
    const indicator = document.getElementById('faceIndicatorRecon');
    const reconBtn = document.getElementById('reconhecer');
    
    try {
        console.log('🔄 Iniciando reconhecimento...');
        indicator.classList.remove('detected');
        indicator.classList.add('processing');
        indicator.querySelector('.face-status').innerHTML = '🔄 Processando...';
        
        const video = document.getElementById('videoRecon');
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        const imagemBase64Recon = canvas.toDataURL('image/jpeg').split(',')[1];
        console.log('📸 Imagem capturada, tamanho:', imagemBase64Recon.length);
        
        updateStatus('Processando reconhecimento...', true);

        // Usar porta 8002 para o Docker
        const url = 'http://localhost:8002/reconhecer';
        console.log('🌐 Enviando para:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ imagem_base64: imagemBase64Recon })
        });

        console.log('📡 Resposta recebida, status:', response.status);
        const data = await response.json();
        console.log('📊 Dados recebidos:', data);
        
        if (data.status === 'match') {
            const cpfAnonimizado = anonimizarCPF(data.cpf);
            updateStatus(`Reconhecido! CPF: ${cpfAnonimizado}`, true);
            indicator.querySelector('.face-status').innerHTML = '✅ Reconhecido!';
        } else if (data.status === 'nao_encontrado') {
            updateStatus('Rosto não encontrado no banco.', false);
            showMessage('Rosto não encontrado no banco de dados.', 'error');
            indicator.querySelector('.face-status').innerHTML = '❌ Não encontrado';
        } else {
            updateStatus('Erro no reconhecimento.', false);
            showMessage(data.mensagem || 'Erro no reconhecimento.', 'error');
            indicator.querySelector('.face-status').innerHTML = '❌ Erro';
        }
    } catch (error) {
        console.error('❌ Erro no reconhecimento:', error);
        updateStatus('Erro de conexão.', false);
        showMessage(`Erro de conexão com o servidor: ${error.message}`, 'error');
        indicator.querySelector('.face-status').innerHTML = '❌ Erro de conexão';
    } finally {
        isProcessingRecognition = false;
        indicator.classList.remove('processing');
        
        // Resetar após 3 segundos
        setTimeout(() => {
            if (currentTab === 'reconhecimento') {
                indicator.classList.remove('detected');
                indicator.querySelector('.face-status').innerHTML = '🔍 Procurando rosto...';
            }
        }, 3000);
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
    // Remover caracteres não numéricos
    cpf = cpf.replace(/[^\d]/g, '');
    
    console.log('Validando CPF:', cpf);
    
    // Verificar se tem 11 dígitos
    if (cpf.length !== 11) {
        console.log('CPF inválido: não tem 11 dígitos');
        return false;
    }
    
    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) {
        console.log('CPF inválido: todos os dígitos são iguais');
        return false;
    }
    
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
    
    const isValid = cpf.charAt(9) == dv1 && cpf.charAt(10) == dv2;
    console.log(`CPF ${cpf}: DV1=${cpf.charAt(9)}, DV2=${cpf.charAt(10)}, Calculado: DV1=${dv1}, DV2=${dv2}, Válido: ${isValid}`);
    
    return isValid;
}

// Função para formatar CPF
function formatarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

// Função para anonimizar CPF (mostra apenas primeiros 3 e últimos 2 dígitos)
function anonimizarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    if (cpf.length === 11) {
        return cpf.substring(0, 3) + '******' + cpf.substring(9, 11);
    }
    return cpf;
}

// Event listeners
document.addEventListener('DOMContentLoaded', async function() {
    // Aguardar carregamento da página e bibliotecas
    await new Promise(resolve => {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', resolve);
        } else {
            resolve();
        }
    });

    // Aguardar face-api.js carregar
    let faceAPILoaded = false;
    let attempts = 0;
    const maxAttempts = 15; // Aumentado para dar mais tempo

    // Tentar carregar face-api.js de múltiplas fontes se não estiver disponível
    if (typeof faceapi === 'undefined') {
        console.log('Face-API.js não encontrado, tentando carregar...');
        
        const cdnSources = [
            'https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js',
            'https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js',
            'https://cdn.jsdelivr.net/npm/face-api.js/dist/face-api.min.js',
            'https://unpkg.com/face-api.js/dist/face-api.min.js'
        ];
        
        for (const cdnUrl of cdnSources) {
            try {
                console.log(`Tentando carregar Face-API.js de: ${cdnUrl}`);
                const script = document.createElement('script');
                script.src = cdnUrl;
                script.async = true;
                
                await new Promise((resolve, reject) => {
                    script.onload = resolve;
                    script.onerror = reject;
                    document.head.appendChild(script);
                });
                
                console.log('Face-API.js carregado com sucesso de:', cdnUrl);
                break;
            } catch (error) {
                console.warn(`Falha ao carregar de ${cdnUrl}:`, error);
                continue;
            }
        }
    }

    while (!faceAPILoaded && attempts < maxAttempts) {
        if (typeof faceapi !== 'undefined') {
            faceAPILoaded = await initFaceAPI();
            if (faceAPILoaded) {
                console.log('Face-API.js inicializado com sucesso');
                break;
            }
        }
        
        console.log(`Aguardando face-api.js... (tentativa ${attempts + 1}/${maxAttempts})`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        attempts++;
    }

    if (!faceAPILoaded) {
        console.warn('Face-API.js não pôde ser carregado, usando modo manual');
        showMessage('⚠️ Detecção automática indisponível. O sistema funcionará em modo manual - use os botões para captura e reconhecimento.', 'warning');
        
        // Atualizar indicadores para modo manual
        const indicators = document.querySelectorAll('.face-status');
        indicators.forEach(indicator => {
            indicator.innerHTML = '⚠️ Modo manual (modelos não carregados)';
        });
    }

    // Inicializar câmera para cadastro
    initCamera('video');
    startFaceDetection('video', 'canvasCadastro', 'faceIndicatorCadastro', 'cadastro');

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
        stopFaceDetection();
        initCamera('video');
        startFaceDetection('video', 'canvasCadastro', 'faceIndicatorCadastro', 'cadastro');
        document.getElementById('previewContainer').style.display = 'none';
        document.getElementById('submitCadastro').disabled = true;
        imagemBase64 = "";
    });

    // Enviar cadastro
    document.getElementById('cadastroForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const cpf = document.getElementById('cpf').value;
        const cpfLimpo = cpf.replace(/\D/g, '');
        
        console.log('CPF original:', cpf);
        console.log('CPF limpo:', cpfLimpo);
        
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
            const payload = { 
                cpf: cpfLimpo,
                imagem_base64: imagemBase64 
            };
            console.log('📤 Enviando cadastro:', { cpf: payload.cpf, imagem_size: payload.imagem_base64.length });
            
            const url = 'http://localhost:8002/cadastro';
            console.log('🌐 Enviando para:', url);
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            console.log('📡 Resposta recebida, status:', response.status);
            const data = await response.json();
            console.log('📊 Dados recebidos:', data);
            
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

    // Reconhecimento facial manual (botão)
    document.getElementById('reconhecer').addEventListener('click', async function() {
        if (isProcessingRecognition) return;
        
        const reconBtn = document.getElementById('reconhecer');
        reconBtn.disabled = true;
        reconBtn.innerHTML = '<span class="loading"></span>Reconhecendo...';
        
        await performAutoRecognition();
        
        reconBtn.disabled = false;
        reconBtn.innerHTML = '🔍 Reconhecer Rosto';
    });

    // Resetar câmera de reconhecimento
    document.getElementById('resetCameraRecon').addEventListener('click', function() {
        stopFaceDetection();
        initCamera('videoRecon');
        startFaceDetection('videoRecon', 'canvasRecon', 'faceIndicatorRecon', 'reconhecimento');
        updateStatus('Aguardando reconhecimento...', true);
    });
}); 