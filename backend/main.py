from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# 🔓 Libera CORS para seu frontend no GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://juanzera04.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "API rodando normalmente 🚀"}


@app.post("/processar")
async def processar_sped(file: UploadFile = File(...)):

    def processar_linhas():
        codigos_c110 = set()

        for linha_bytes in file.file:
            try:
                linha = linha_bytes.decode("utf-8").strip()
            except:
                linha = linha_bytes.decode("latin-1").strip()

            # Novo bloco de nota
            if linha.startswith("|C100|"):
                codigos_c110.clear()
                yield linha + "\n"

            # Registro C110
            elif linha.startswith("|C110|"):
                partes = linha.split("|")

                if len(partes) > 2:
                    codigo = partes[2]

                    # Evita C110 duplicado dentro da mesma nota
                    if codigo not in codigos_c110:
                        codigos_c110.add(codigo)
                        yield linha + "\n"
                else:
                    yield linha + "\n"

            # Qualquer outra linha passa direto
            else:
                yield linha + "\n"

    return StreamingResponse(
        processar_linhas(),
        media_type="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=SPED_TRATADO.txt"
        }
    )