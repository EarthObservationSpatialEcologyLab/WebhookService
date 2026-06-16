import os
import json
import tempfile
import psycopg2
import base64

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


def insert_hardwario_message(payload: dict):
    print("Gate 3")
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as cur:
            print("Ready to execute", payload)
            cur.execute(
                "INSERT INTO ods.hardwario_messages (raw_message_data) VALUES (%s)",
                (json.dumps(payload),),
            )
