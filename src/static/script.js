// Botões 
let startBtn = document.querySelector("#startBtn")
let sendBtn = document.querySelector("#sendBtn")
let selectBtn = document.querySelector("#selectBtn")
let uploadBtn = document.querySelector("#fileInput")

// Arquivo
let selectedFiles = [];


function setupInsightsBtn() {
    let insightsBtn = document.querySelector("#imgBtnInsights");
    if (insightsBtn) {
        insightsBtn.addEventListener('click', async () => {
            try {
                console.log("btninsights clicadooooooooooo");
                const response = await fetch('/insights', {
                    method: 'GET'
                });

                const result = await response.json();
                if (response.ok) {
                    console.log("foiiiiiiiiiiiiiiiiiiiiiii");
                    let responseContent = document.querySelector("#service #content #right #response #content");

                    if (responseContent) {
                        // Remove a imagem de fundo
                        responseContent.style.backgroundImage = 'none';

                        // Adiciona o texto ao conteúdo do elemento
                        responseContent.textContent = result.message;
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
    selectedFiles = Array.from(uploadBtn.files);

    // Verifica se nenhum arquivo foi selecionado
    if (selectedFiles.length === 0) {
        console.log("Nenhum arquivo selecionado!");
        return;
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
    }
});

// Evento de clique para selecionar arquivos
selectBtn.addEventListener('click', (e) => {
    console.log("selectBtn button clicked!");
    e.preventDefault();
    uploadBtn.click(); // Simula um clique no uploadBtn
});

// Evento para capturar a mudança no arquivo selecionado
uploadBtn.addEventListener('change', async () => {
    console.log("uploadBtn change event");
});

// Configura o evento de clique para o botão de insights inicial
setupInsightsBtn();
