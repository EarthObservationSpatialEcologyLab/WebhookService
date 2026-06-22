import os
import json
import logging
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
_known_station_ids: set[int] = set()

log = logging.getLogger(__name__)


async def init_pool():
    global _pool
    _pool = await asyncpg.create_pool(dsn=DSN, min_size=1, max_size=5)
    await reload_devices()


async def reload_devices():
    global _known_station_ids
    assert _pool is not None
    rows = await _pool.fetch("SELECT id FROM ods.station")
    _known_station_ids = {r["id"] for r in rows}
    log.info("Loaded %d known stations", len(_known_station_ids))


async def validate_station(station_id: int) -> bool:
    return station_id in _known_station_ids


async def insert_hardwario_message(payload: dict):
    assert _pool is not None
    print("Gate 3")

    station_id = int(payload["attribute"]["serial_number"])

    if not await validate_station(station_id):
        await reload_devices()
        if not await validate_station(station_id):
            log.warning("Unknown station %s, dropping message", station_id)
            return

    await _pool.execute(
        "INSERT INTO ods.hardwario_messages (received_at, raw_message_data) VALUES (NOW(), $1)",
        json.dumps(payload),
    )
