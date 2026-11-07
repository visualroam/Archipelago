"""
op.gg-Anbindung über den offiziellen OP.GG MCP Server (https://mcp-api.op.gg/mcp).

Kein KI-Bot: Das ist ein ganz normaler HTTP-POST (JSON-RPC "tools/call"), kein API-Key nötig.
Die Antwort ist Text in einer Konstruktor-Notation, z. B.

    class GameHistory: id,game_type
    class Stats: kill,result

    LolListSummonerMatches(Data([GameHistory("abc","NORMAL",...)]))

parse_opgg() macht daraus normale dicts/listen.
"""
import json
import re
import ssl
import urllib.error
import urllib.request

MCP_URL = "https://mcp-api.op.gg/mcp"
USER_AGENT = "AF-LoL-Winstreak-Client/0.2"

MATCH_FIELDS = [
    "data.game_history[].{id,created_at,game_map,game_type,game_length_second}",
    "data.game_history[].participants[].{champion_name,position,items_names[]}",
    "data.game_history[].participants[].summoner.{game_name,tagline}",
    "data.game_history[].participants[].stats.{kill,death,assist,result,largest_multi_kill}",
    "data.game_history[].participants[].rune.{primary_rune_id}",
]


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
    # Streamable HTTP kann JSON oder SSE ("data: {...}") liefern
    if raw.lstrip().startswith("{"):
        msg = json.loads(raw)
    else:
        data = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
        if not data:
            raise OpggError("Unerwartete Antwort von op.gg")
        msg = json.loads(data[-1])
    if "error" in msg:
        raise OpggError(msg["error"].get("message", "Unbekannter Fehler"))
    result = msg.get("result", {})
    texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
    if result.get("isError"):
        raise OpggError(" ".join(texts) or "Unbekannter Fehler")
    return "\n".join(texts)


# ---------------------------------------------------------------- Parser

_TOKEN = re.compile(r'\s*(?:(?P<str>"(?:[^"\\]|\\.)*")|(?P<num>-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)'
                    r'|(?P<name>[A-Za-z_][A-Za-z0-9_]*)|(?P<sym>[()\[\],]))')


def parse_opgg(text: str):
    """Wandelt die op.gg-MCP-Textantwort in dicts/listen um."""
    classes: dict[str, list[str]] = {}
    body_lines = []
    for line in text.splitlines():
        m = re.match(r"^class (\w+):\s*(.*)$", line)
        if m:
            classes[m.group(1)] = [f.strip() for f in m.group(2).split(",") if f.strip()]
        elif line.strip():
            body_lines.append(line)
    body = "\n".join(body_lines)
    tokens = []
    pos = 0
    while pos < len(body):
        if body[pos].isspace():
            pos += 1
            continue
        m = _TOKEN.match(body, pos)
        if not m:
            raise OpggError(f"op.gg-Antwort nicht lesbar bei Zeichen {pos}")
        tokens.append((m.lastgroup, m.group(m.lastgroup)))
        pos = m.end()

    i = 0

    def value():
        nonlocal i
        kind, tok = tokens[i]
        i += 1
        if kind == "str":
            return json.loads(tok)
        if kind == "num":
            return float(tok) if any(c in tok for c in ".eE") else int(tok)
        if kind == "sym" and tok == "[":
            items = []
            while tokens[i][1] != "]":
                items.append(value())
                if tokens[i][1] == ",":
                    i += 1
            i += 1
            return items
        if kind == "name":
            if tok in ("true", "True"):
                return True
            if tok in ("false", "False"):
                return False
            if tok in ("null", "None"):
                return None
            # Konstruktor: Name(arg, arg, ...)
            if i < len(tokens) and tokens[i][1] == "(":
                i += 1
                args = []
                while tokens[i][1] != ")":
                    args.append(value())
                    if tokens[i][1] == ",":
                        i += 1
                i += 1
                fields = classes.get(tok)
                if fields and len(fields) == len(args):
                    return dict(zip(fields, args))
                return {"_type": tok, "_args": args}
            return tok
        raise OpggError(f"op.gg-Antwort nicht lesbar ({tok!r})")

    if not tokens:
        return None
    return value()


def fetch_matches(game_name: str, tag_line: str, region: str, limit: int = 20) -> list[dict]:
    """Letzte Spiele (neueste zuerst) als Liste von dicts."""
    text = call_tool("lol_list_summoner_matches", {
        "game_name": game_name, "tag_line": tag_line, "region": region.upper(),
        "limit": limit, "desired_output_fields": MATCH_FIELDS,
    })
    parsed = parse_opgg(text)
    try:
        return parsed["data"]["game_history"] or []
    except (TypeError, KeyError):
        raise OpggError("op.gg hat keine Match-Liste geliefert")
