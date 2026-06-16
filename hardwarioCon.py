import dbCon


def process(payload: dict):
    dbCon.insert_hardwario_message(payload)
