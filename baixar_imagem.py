from icrawler.builtin import GoogleImageCrawler
from icrawler import settings
from PIL import Image
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name='dzqt6j9bj',
    api_key='999688376561143',
    api_secret=os.environ.get("CLOUDINARY_SECRET")
)

def montar_termos(marca, modelo, cor, ano):
    termos = f"{marca} {modelo} {ano} {cor} carro inteiro lateral frente -logo -marca -site"
    return termos

def imagem_valida(caminho):
    try:
        with Image.open(caminho) as img:
            largura, altura = img.size
            if largura < 500 or altura < 300 or largura < altura:
                print(f"[INVALIDA] Tamanho da imagem insuficiente: {largura}x{altura}")
                return False
            return True
    except Exception as e:
        print(f"[ERRO] Não foi possível abrir imagem: {e}")
        return False

def imagem_ja_no_cloudinary(nome_publico):
    try:
        resultado = cloudinary.api.resource(nome_publico)
        return resultado['secure_url']
    except cloudinary.exceptions.NotFound:
        return None

def baixar_e_retornar_cloudinary_url(termos, tentativas=3):
    nome_publico = termos.replace(" ", "_").lower()
    url_existente = imagem_ja_no_cloudinary(nome_publico)
    if url_existente:
        print(f"[INFO] Imagem já no Cloudinary: {url_existente}")
        return url_existente

    os.makedirs("imagens", exist_ok=True)

    for tentativa in range(tentativas):
        print(f"[TENTATIVA {tentativa+1}] Buscando imagem para: {termos}")

        crawler = GoogleImageCrawler(storage={"root_dir": "imagens"})
        # Adicionando User-Agent para evitar 403
        crawler.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        })
        crawler.crawl(keyword=termos, max_num=1, file_idx_offset=0)

        arquivos = sorted(
            os.listdir("imagens"),
            key=lambda x: os.path.getctime(os.path.join("imagens", x)),
            reverse=True
        )

        for arq in arquivos:
            caminho_temp = os.path.join("imagens", arq)

            # ⚠️ Filtro automático por nome de arquivo/dominio problemático
            nome_arquivo = arq.lower()
            if any(site in nome_arquivo for site in ['reddit', 'redd', 'pinterest', 'tumblr', 'blogspot']):
                print(f"[DESCARTADA] Imagem de site indesejado: {arq}")
                os.remove(caminho_temp)
                continue

            if imagem_valida(caminho_temp):
                print(f"[VALIDA] Subindo imagem válida para Cloudinary...")
                resultado = cloudinary.uploader.upload(
                    caminho_temp,
                    public_id=nome_publico,
                    folder="veiculos",
                    overwrite=True,
                    resource_type="image"
                )
                os.remove(caminho_temp)
                print(f"[OK] Imagem enviada com sucesso: {resultado['secure_url']}")
                return resultado['secure_url']
            else:
                os.remove(caminho_temp)

    print(f"[FALHA] Nenhuma imagem válida encontrada para: {termos}")
    return None
