let startBtn = document.querySelector("#startBtn")
let sendBtn = document.querySelector("#sendBtn")
let selectBtn = document.querySelector("#selectBtn")
let uploadBtn = document.querySelector("#fileInput")
let uploadArea = document.querySelector("#box")


let selectedFiles = [];

function removerArquivo(fileContainer) {
    // Remove o contêiner do arquivo do DOM
    fileContainer.parentNode.removeChild(fileContainer);
}


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
                        responseContent.innerHTML = result.message;
                        responseContent.classList.add('response-content');
                        responseBlock.classList.add('response-block');
                        textContent.classList.add('text-content');
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

sendBtn.addEventListener('click', async () => {
    var checkbox = document.getElementById('checkbox');
    var message = document.getElementById('terms-checkbox');
    
    if (!checkbox.checked) {
        event.preventDefault(); 
        message.classList.remove('hidden-loader');
    } else {
        message.classList.add('hidden-loader');
    }

    selectedFiles = Array.from(uploadBtn.files);
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
            sendBtn.src = "./static/img/create-insights.svg";
            sendBtn.id = 'imgBtnInsights';

            setupInsightsBtn();
        } else {
            console.log(result.error);
        }
    } catch (error) {
        console.error('Erro ao enviar os arquivos:', error);
    }})

selectBtn.addEventListener('click', (e) => {
    console.log("selectBtn button clicked!");
    e.preventDefault();
    uploadBtn.click(); 
});

uploadBtn.addEventListener('change', async () => {
    
    uploadArea.innerHTML = "";
    
    for (const file of uploadBtn.files) {
        if (file.type === 'application/pdf') {
            const fileContainer = document.createElement('div');
            fileContainer.classList.add('file-container'); 
            fileContainer.classList.add('file-box'); 
            
            const fileName = document.createElement('div');
            fileName.textContent = file.name;
            
            const removerButton = document.createElement('button');
            removerButton.classList.add('remove-button');
            removerButton.addEventListener('click', function() {
                removerArquivo(fileContainer);
            });

            fileContainer.appendChild(fileName);
            fileContainer.appendChild(removerButton);
            
            uploadArea.appendChild(fileContainer);
        }
    }
});

setupInsightsBtn()
