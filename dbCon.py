import os
import json
import logging
import asyncpg

DSN = os.environ.get("DATABASE_URL", "")

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
