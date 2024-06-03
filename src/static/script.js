let startBtn = document.querySelector("#startBtn")
let sendBtn = document.querySelector("#sendBtn")
let selectBtn = document.querySelector("#selectBtn")
let uploadBtn = document.querySelector("#fileInput")
let uploadArea = document.querySelector("#box")

// Arquivo
let selectedFiles = [];


function setupInsightsBtn() {
    let insightsBtn = document.querySelector("#imgBtnInsights");
    if (insightsBtn) {
        insightsBtn.addEventListener('click', async () => {
            try {
                // Mostra o loader antes de enviar a solicitação
                document.getElementById('content').classList.add('hidden-loader');
                document.getElementById('loader').classList.remove('hidden-loader');
                document.getElementById('loader').classList.add('loader');
                console.log("btninsights clicado");

                const response = await fetch('/insights', {
                    method: 'GET'
                });

                const result = await response.json();

                // Esconde o loader após receber a resposta
                document.getElementById('loader').classList.remove('loader');
                document.getElementById('loader').classList.add('hidden-loader');

                if (response.ok) {
                    console.log("Response gerada com sucesso.");
                    let textContent = document.querySelector("#service #content #right #response #content #text");
                    let responseBlock = document.querySelector("#service #content #right #response");
                    let responseContent = document.querySelector("#service #content #right #response #content");
                    if (responseContent) {
                        responseContent.style.backgroundImage = 'none';
                        responseContent.textContent = result.message;
                        
                        responseBlock.style.width = '90%';
                        responseBlock.style.overflow = 'auto';
                        
                        textContent.style.display = 'flex';
                        textContent.style.flexDirection = 'row';
                        textContent.style.fontSize = '20px';
                    } else {
                        console.error('Elemento não encontrado!');
                    }

                    console.log(result.message);
                } else {
                    console.log("nao foiii =(");
                    console.log(result.error);
                }
            } catch (error) {
                console.error('Erro ao obter insights:', error);
            }
        });
    }
}

// Evento de clique para enviar arquivos
sendBtn.addEventListener('click', async () => {
    // Verificando se a checkbox está marcada
    var checkbox = document.getElementById('checkbox');
    var message = document.getElementById('terms-checkbox');
    
    if (!checkbox.checked) {
        event.preventDefault(); // Impede o envio do formulário
        message.classList.remove('hidden-loader');
    } else {
        message.classList.add('hidden-loader');
    }

    selectedFiles = Array.from(uploadBtn.files);
    // Verifica se nenhum arquivo foi selecionado
    if (selectedFiles.length === 0) {
        console.log("Nenhum arquivo selecionado!");
    }
    const formData = new FormData();
    for (const file of selectedFiles) {
        formData.append('files[]', file);
    }

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            console.log(result.message);
            // Muda a imagem e o ID do botão após o envio bem-sucedido
            sendBtn.src = "./static/img/create-insights.svg";
            sendBtn.id = 'imgBtnInsights';

            // Configura o evento de clique para o novo botão
            setupInsightsBtn();
        } else {
            console.log(result.error);
        }
    } catch (error) {
        console.error('Erro ao enviar os arquivos:', error);
    }})

// Evento de clique para selecionar arquivos
selectBtn.addEventListener('click', (e) => {
    console.log("selectBtn button clicked!");
    e.preventDefault();
    uploadBtn.click(); // Simula um clique no uploadBtn
});

// Evento para capturar a mudança no arquivo selecionado
uploadBtn.addEventListener('change', async () => {
    // Limpa a pré-visualização anterior
    uploadArea.innerHTML = "";
    
    // Itera sobre os arquivos selecionados
    for (const file of uploadBtn.files) {
        // Verifica se o arquivo é um PDF
        if (file.type === 'application/pdf') {
            // Cria um contêiner para o arquivo
            const fileContainer = document.createElement('div');
            fileContainer.classList.add('file-container');
            
            // Adiciona o ícone de PDF
            const pdfIcon = document.createElement('img');
            pdfIcon.alt = 'PDF';
            pdfIcon.classList.add('preview-pdf-icon');
            fileContainer.appendChild(pdfIcon);
            
            // Adiciona o nome do arquivo
            const fileName = document.createElement('div');
            fileName.textContent = file.name;
            fileContainer.appendChild(fileName);
            
            // Adiciona o contêiner do arquivo à área de pré-visualização
            uploadArea.appendChild(fileContainer);
        }
    }
});

// Configura o evento de clique para o botão de insights inicial
setupInsightsBtn()
