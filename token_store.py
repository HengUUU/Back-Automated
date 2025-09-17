token_memory = {
    "token": None  # initially no token
}

# Optional helper functions
def set_token(token: str):
    token_memory["token"] = token

def get_token() -> str | None:
    return token_memory.get("token")