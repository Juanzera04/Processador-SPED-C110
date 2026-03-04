const URL_BACKEND = "https://SEU_BACKEND.onrender.com";

const btnAbrir = document.getElementById("btnAbrir");
const loadingInicial = document.getElementById("loadingInicial");
const appContainer = document.getElementById("appContainer");

const fileInput = document.getElementById("fileInput");
const btnDownload = document.getElementById("btnDownload");
const arquivoInfo = document.getElementById("arquivoInfo");
const statusProcessamento = document.getElementById("statusProcessamento");

let arquivoProcessadoBlob = null;

// ====== ACORDAR BACKEND ======
btnAbrir.addEventListener("click", async () => {
    loadingInicial.classList.add("mostrar");

    try {
        const response = await fetch(`${URL_BACKEND}/wake`);
        await response.json();

        loadingInicial.classList.remove("mostrar");
        document.getElementById("inicial").style.display = "none";
        appContainer.style.display = "flex";
    } catch (error) {
        loadingInicial.classList.remove("mostrar");
        alert("Erro ao conectar com o servidor.");
    }
});

// ====== SELECIONAR ARQUIVO ======
fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    arquivoInfo.textContent = `Arquivo selecionado: ${file.name}`;
    arquivoInfo.classList.add("mostrar");

    statusProcessamento.className = "status processo mostrar";
    statusProcessamento.innerHTML = `<span class="loader"></span> Processando...`;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${URL_BACKEND}/processar`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error();

        arquivoProcessadoBlob = await response.blob();

        statusProcessamento.className = "status sucesso mostrar";
        statusProcessamento.textContent = "Arquivo processado com sucesso!";

        btnDownload.disabled = false;

    } catch {
        statusProcessamento.className = "status erro mostrar";
        statusProcessamento.textContent = "Erro ao processar arquivo.";
    }
});

// ====== DOWNLOAD ======
btnDownload.addEventListener("click", () => {
    const url = window.URL.createObjectURL(arquivoProcessadoBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "SPED_TRATADO.txt";
    a.click();
});