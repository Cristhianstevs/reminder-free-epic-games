import requests
import os
from datetime import datetime, timezone

# ==============================
# CONFIGURAÇÕES
# ==============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("Variáveis TELEGRAM_TOKEN ou CHAT_ID não definidas.")

EPIC_URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

# ==============================
# TRADUÇÃO
# ==============================

def traduzir_texto(texto, destino="pt"):
    if not texto:
        return ""

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "en",
        "tl": destino,
        "dt": "t",
        "q": texto
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        resultado = response.json()
        traducao = "".join([parte[0] for parte in resultado[0]])
        return traducao

    except Exception as e:
        print("Erro ao traduzir:", e)
        return texto

# ==============================
# BUSCAR JOGOS GRÁTIS
# ==============================

def buscar_jogos_gratis():
    try:
        response = requests.get(EPIC_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Erro ao buscar dados da Epic:", e)
        return []

    elements = data.get("data", {}) \
                   .get("Catalog", {}) \
                   .get("searchStore", {}) \
                   .get("elements", [])

    jogos_ativos = []
    now = datetime.now(timezone.utc)

    for jogo in elements:

        price_info = jogo.get("price", {}).get("totalPrice", {})
        discount_price = price_info.get("discountPrice")

        if discount_price is None or discount_price != 0:
            continue

        promotions = jogo.get("promotions")
        if not promotions:
            continue

        offers = promotions.get("promotionalOffers")
        if not offers:
            continue

        offer_data = offers[0].get("promotionalOffers")
        if not offer_data:
            continue

        start_date = offer_data[0].get("startDate")
        end_date = offer_data[0].get("endDate")

        if not start_date or not end_date:
            continue

        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

        if not (start <= now <= end):
            continue

        # 🔥 Melhor imagem
        image_url = None
        for img in jogo.get("keyImages", []):
            if img.get("type") == "OfferImageWide":
                image_url = img.get("url")
                break

        if not image_url and jogo.get("keyImages"):
            image_url = jogo["keyImages"][0].get("url")

        # 🔥 Link direto
        page_slug = None
        mappings = jogo.get("catalogNs", {}).get("mappings", [])

        if mappings:
            page_slug = mappings[0].get("pageSlug")

        if not page_slug:
            page_slug = jogo.get("productSlug")

        link = f"https://store.epicgames.com/pt-BR/p/{page_slug}" if page_slug else None

        # 🔥 Preço original
        original_price = price_info.get("originalPrice", 0)
        currency = price_info.get("currencyCode", "BRL")
        preco_original = original_price / 100 if original_price else 0

        # 🔥 Desenvolvedor
        seller = jogo.get("seller", {}).get("name", "Desconhecido")

        jogos_ativos.append({
            "title": jogo.get("title"),
            "image": image_url,
            "endDate": end,
            "description": jogo.get("description"),
            "link": link,
            "preco_original": preco_original,
            "currency": currency,
            "seller": seller
        })

    jogos_unicos = {j["title"]: j for j in jogos_ativos}
    return list(jogos_unicos.values())

# ==============================
# TELEGRAM
# ==============================

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)


def enviar_foto(image_url, legenda):
    if not image_url:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": legenda
    }

    try:
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print("Erro ao enviar foto:", e)

# ==============================
# EXECUÇÃO
# ==============================

def main():
    print("Buscando jogos gratuitos...")
    jogos = buscar_jogos_gratis()

    if not jogos:
        print("Nenhum jogo gratuito ativo.")
        return

    hoje = datetime.now().strftime("%d/%m")

    enviar_mensagem(
        f"🎮 Jogos grátis da semana – {hoje}\n\n"
        "A Epic Games liberou novos jogos temporariamente gratuitos.\n\n"
        "🔎 Ver todos os jogos grátis:\n"
        "https://store.epicgames.com/pt-BR/free-games\n\n"
        "Confira os destaques abaixo 👇"
    )

    for jogo in jogos:

        print(f"Traduzindo descrição de {jogo['title']}...")
        descricao_traduzida = traduzir_texto(jogo["description"])[:800]

        preco_formatado = (
            f"{jogo['currency']} {jogo['preco_original']:.2f}"
            if jogo["preco_original"] > 0 else "Indisponível"
        )

        legenda = (
            f"🎮 Jogo: {jogo['title']}\n"
            f"🏢 Desenvolvedor: {jogo['seller']}\n"
            f"💰 De: {preco_formatado}\n"
            f"🔥 Agora: GRÁTIS\n"
            f"⏰ Grátis até: {jogo['endDate'].strftime('%d/%m/%Y')}\n\n"
            f"📝 Sobre:\n{descricao_traduzida}\n\n"
            f"🎁 Resgatar agora:\n{jogo['link']}"
        )

        print(f"Enviando {jogo['title']}...")
        enviar_foto(jogo["image"], legenda)

    print("Mensagens enviadas com sucesso!")

if __name__ == "__main__":
    main()
