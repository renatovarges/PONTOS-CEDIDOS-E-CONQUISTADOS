"""Atualiza o mercado oficial do Cartola usado para elegibilidade do ranking."""
import json
import os
import urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "cartola_mercado.json")
MARKET_URL = "https://api.cartola.globo.com/atletas/mercado"
STATUS_URL = "https://api.cartola.globo.com/mercado/status"
ELIGIBLE_STATUS = {2: "duvida", 7: "provavel"}


def _get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache", "Pragma": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def atualizar():
    market = _get_json(MARKET_URL)
    market_status = _get_json(STATUS_URL)
    clubs = market.get("clubes", {})
    by_id = {}
    for athlete in market.get("atletas", []):
        status_id = int(athlete.get("status_id") or 0)
        if status_id not in ELIGIBLE_STATUS:
            continue
        athlete_id = str(athlete.get("atleta_id") or "")
        club_id = str(athlete.get("clube_id") or "")
        if not athlete_id or not club_id:
            continue
        club = clubs.get(club_id) or clubs.get(int(club_id), {})
        by_id[athlete_id] = {
            "id": athlete_id,
            "club_id": club_id,
            "team": club.get("nome", ""),
            "position_id": int(athlete.get("posicao_id") or 0),
            "status_id": status_id,
            "status": ELIGIBLE_STATUS[status_id],
            "name": athlete.get("apelido") or athlete.get("nome") or "",
        }
    if len(by_id) < 150:
        raise RuntimeError("Cobertura insuficiente na API oficial do Cartola")
    payload = {
        "round": int(market_status.get("rodada_atual") or 0),
        "market_status": int(market_status.get("status_mercado") or 0),
        "closing": market_status.get("fechamento", {}),
        "source": MARKET_URL,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "eligible_status": {"2": "duvida", "7": "provavel"},
        "by_id": by_id,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("Cartola atualizado: rodada {} ({} elegíveis)".format(payload["round"], len(by_id)))
    return payload


if __name__ == "__main__":
    atualizar()
