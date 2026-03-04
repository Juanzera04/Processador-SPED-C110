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

    async def processar_linhas():
        codigos_c110 = set()
        c100_ativo = False

        while True:
            linha_bytes = await file.readline()
            if not linha_bytes:
                break

            try:
                linha = linha_bytes.decode("utf-8").strip()
            except:
                linha = linha_bytes.decode("latin-1").strip()

            if linha.startswith("|C100|"):
                codigos_c110.clear()
                c100_ativo = True
                yield linha + "\n"

            elif linha.startswith("|C110|") and c100_ativo:
                partes = linha.split("|")

                if len(partes) > 2:
                    codigo = partes[2]

                    if codigo not in codigos_c110:
                        codigos_c110.add(codigo)
                        yield linha + "\n"
                else:
                    yield linha + "\n"

            else:
                yield linha + "\n"

    return StreamingResponse(
        processar_linhas(),
        media_type="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=SPED_TRATADO.txt"
        }
    )