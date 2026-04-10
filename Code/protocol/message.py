
MSG_JOIN  = "JOIN"   
MSG_MSG   = "MSG"  
MSG_LEAVE = "LEAVE"  
DELIMITER = "\n"
SEPARATOR = "|"


def build_join(username: str) -> str:
    return f"{MSG_JOIN}{SEPARATOR}{username}"

def build_message(username: str, text: str) -> str:
    return f"{MSG_MSG}{SEPARATOR}{username}{SEPARATOR}{text}"

def build_leave(username: str) -> str:
    return f"{MSG_LEAVE}{SEPARATOR}{username}"

def encode_message(msg: str) -> bytes:
    return (msg + DELIMITER).encode("utf-8")

def decode_message(raw: str) -> dict:
    parts = raw.split(SEPARATOR, maxsplit=2)
    if not parts:
        return {"type": "UNKNOWN", "raw": raw}

    msg_type = parts[0]  

    if msg_type == MSG_JOIN and len(parts) >= 2:
        return {"type": MSG_JOIN, "username": parts[1]}

    elif msg_type == MSG_MSG and len(parts) >= 3:
        return {"type": MSG_MSG, "username": parts[1], "text": parts[2]}

    elif msg_type == MSG_LEAVE and len(parts) >= 2:
        return {"type": MSG_LEAVE, "username": parts[1]}

    return {"type": "UNKNOWN", "raw": raw}
