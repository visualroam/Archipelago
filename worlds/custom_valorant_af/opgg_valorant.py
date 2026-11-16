"""
op.gg-Anbindung für Valorant über den offiziellen OP.GG MCP Server (https://mcp-api.op.gg/mcp).

Kein KI-Bot und kein API-Key: normaler HTTP-POST (JSON-RPC "tools/call") auf das Tool
"valorant_list_player_matches" mit game_name + tag_line. Die Antwort ist eine JSON-Liste der
letzten Spiele (neueste zuerst), pro Spiel u. a.:
    matchId, queueId ("unrated", "competitive", "swiftplay", ...), gameStartDateTime,
    characterId (Agent-UUID), won, draw, kills, deaths, assists, aceCount, multiKills
"""
import json
import ssl
import urllib.error
import urllib.request

MCP_URL = "https://mcp-api.op.gg/mcp"
USER_AGENT = "Custom-Valorant-AF-Client/1.0"

# Agent-UUID (wie op.gg sie liefert) -> Itemname in der APWorld.
# Stand 06.11.2026, aus valorant_list_agents. Wird beim Start zusätzlich live von op.gg ergänzt.
AGENT_IDS = {
    "41FB69C1-4189-7B37-F117-BCAF1E96F1BF": "Astra",
    "5F8D3A7F-467B-97F3-062C-13ACF203C006": "Breach",
    "9F0D8BA9-4140-B941-57D3-A7AD57C6B417": "Brimstone",
    "22697A3D-45BF-8DD7-4FEC-84A9E28C69D7": "Chamber",
    "1DBF2EDD-4729-0984-3115-DAA5EED44993": "Clove",
    "117ED9E3-49F3-6512-3CCF-0CADA7E3823B": "Cypher",
    "CC8B64C8-4B25-4FF9-6E7F-37B4DA43D235": "Deadlock",
    "DADE69B4-4F5A-8528-247B-219E5A1FACD6": "Fade",
    "E370FA57-4757-3604-3648-499E1F642D3F": "Gekko",
    "95B78ED7-4637-86D9-7E41-71BA8C293152": "Harbor",
    "DDD5A15C-4FBE-42FA-3789-11A55CA5EE04": "Hush",
    "0E38B510-41A8-5780-5E8F-568B2A4F2D6C": "Iso",
    "ADD6443A-41BD-E414-F6AD-E58D267F4E95": "Jett",
    "601DBBE7-43CE-BE57-2A40-4ABD24953621": "KAY/O",
    "1E58DE9C-4950-5125-93E9-A0AEE9F98746": "Killjoy",
    "7C8A4701-4DE6-9355-B254-E09BC2A34B72": "Miks",
    "BB2A4828-46EB-8CD1-E765-15848195D751": "Neon",
    "8E253930-4C05-31DD-1B6C-968525494517": "Omen",
    "EB93336A-449B-9C1B-0A54-A891F7921D69": "Phoenix",
    "F94C3B30-42BE-E959-889C-5AA313DBA261": "Raze",
    "A3BFB853-43B2-7238-A4F1-AD90E9E46BCC": "Reyna",
    "569FDD95-4D10-43AB-CA70-79BECC718B46": "Sage",
    "6F2A04CA-43E0-BE17-7F36-B3908627744D": "Skye",
    "320B2A48-4D9B-A075-30F1-1F93A9B638FA": "Sova",
    "B444168C-4E35-8076-DB47-EF9BF368F384": "Tejo",
    "92EEEF5D-43B5-1D4A-8D03-B3927A09034B": "Veto",
    "707EAB51-4836-F488-046A-CDA6BF494859": "Viper",
    "EFBA5359-4016-A1E5-7626-B1AE76895940": "Vyse",
    "DF1CB487-4902-002E-5C17-D28E83E78588": "Waylay",
    "7F94D92C-4234-0A36-9646-3A87EB8B5C89": "Yoru",
}


class OpggError(Exception):
    pass


def _ssl_context():
    try:
        import certifi  # im Archipelago-Paket dabei
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def call_tool(name: str, arguments: dict, timeout: float = 30) -> str:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": arguments}}).encode()
    req = urllib.request.Request(MCP_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": USER_AGENT,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise OpggError(f"op.gg antwortet mit HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise OpggError(f"op.gg nicht erreichbar: {e.reason}") from e
    if raw.lstrip().startswith("{"):
        msg = json.loads(raw)
    else:  # Streamable HTTP kann auch SSE ("data: {...}") liefern
        data = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
        if not data:
            raise OpggError("Unerwartete Antwort von op.gg")
        msg = json.loads(data[-1])
    if "error" in msg:
        raise OpggError("op.gg kennt diese Riot-ID nicht oder hat keine Daten "
                        f"({msg['error'].get('message', 'Fehler')})")
    result = msg.get("result", {})
    texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
    if result.get("isError"):
        raise OpggError(" ".join(texts) or "Unbekannter Fehler")
    return "\n".join(texts)


def fetch_matches(game_name: str, tag_line: str) -> list[dict]:
    """Letzte Spiele (op.gg liefert ~10, neueste zuerst) als Liste von dicts."""
    text = call_tool("valorant_list_player_matches", {"game_name": game_name, "tag_line": tag_line})
    try:
        data = json.loads(text)
    except ValueError as e:
        raise OpggError("op.gg-Antwort nicht lesbar") from e
    if isinstance(data, dict):  # falls op.gg die Liste später einpackt
        data = data.get("data", data.get("matches", []))
    if not isinstance(data, list):
        raise OpggError("op.gg hat keine Match-Liste geliefert")
    return [m for m in data if isinstance(m, dict) and m.get("matchId")]


def fetch_agent_ids() -> dict[str, str]:
    """Aktuelle Agent-UUIDs von op.gg (für Agenten, die nach dem 06.11.2026 erscheinen)."""
    text = call_tool("valorant_list_agents", {})
    return {a["agent_id"].upper(): a["name"] for a in json.loads(text) if a.get("agent_id") and a.get("name")}
