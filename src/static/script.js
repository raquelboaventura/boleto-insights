// Botões 
let startBtn = document.querySelector("#startBtn")
let sendBtn = document.querySelector("#sendBtn")
let selectBtn = document.querySelector("#selectBtn")
let uploadBtn = document.querySelector("#fileInput")

//teste clicks 
sendBtn.addEventListener('click', async () => {
    console.log("Send button clicked!");})

selectBtn.addEventListener('click', (e) => {
    console.log("selectBtn button clicked!");
    e.preventDefault();
    uploadBtn.click(); // Simula um clique no uploadBtn
});

uploadBtn.addEventListener('change', async () => {
    console.log("uploadBtn opaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
});
