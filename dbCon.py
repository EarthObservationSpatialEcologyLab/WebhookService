import os
import json
import tempfile
import base64
import asyncpg

DSN = os.environ.get("DATABASE_URL", "")

# If CA_CERT env var is set, write it to a temp file
# and append sslrootcert to the DSN so it works inside Docker without volume mounts.
_ca_cert = base64.b64decode(os.environ.get("CA_CERT", "")).decode()
if _ca_cert and "sslrootcert" not in DSN:
    _f = tempfile.NamedTemporaryFile(delete=False, suffix=".pem", mode="w")
    _f.write(_ca_cert)
    _f.close()
    sep = "&" if "?" in DSN else "?"
    DSN += f"{sep}sslrootcert={_f.name}"

_pool: asyncpg.Pool | None = None


async def init_pool():
    global _pool
    _pool = await asyncpg.create_pool(dsn=DSN, min_size=1, max_size=5)


async def insert_hardwario_message(payload: dict):
    assert _pool is not None
    print("Gate 3")
    await _pool.execute(
        "INSERT INTO ods.hardwario_messages (raw_message_data) VALUES ($1)",
        json.dumps(payload),
    )
