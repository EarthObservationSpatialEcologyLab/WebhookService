import dbCon


def process(payload: dict):
    print("Gate 2")
    if "attribute" in payload.keys():
        dbCon.insert_hardwario_message(payload)
