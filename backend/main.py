from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

# Libera CORS para frontend do GitHub
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== WAKE (1+1) ======
@app.get("/wake")
def wake():
    return {"resultado": 1 + 1}

# ====== PROCESSAR SPED ======
@app.post("/processar")
async def processar_sped(file: UploadFile = File(...)):
    conteudo = await file.read()
    linhas = conteudo.decode("utf-8").splitlines()

    resultado = []
    codigos_c110 = set()

    for linha in linhas:

        if linha.startswith("|C100|"):
            codigos_c110.clear()
            resultado.append(linha)

        elif linha.startswith("|C110|"):
            partes = linha.split("|")
            codigo = partes[2]

            if codigo not in codigos_c110:
                codigos_c110.add(codigo)
                resultado.append(linha)

        else:
            resultado.append(linha)

    arquivo_final = "\n".join(resultado)
    buffer = io.BytesIO(arquivo_final.encode("utf-8"))

    return StreamingResponse(
        buffer,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=SPED_TRATADO.txt"}
    )