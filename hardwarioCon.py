import dbCon


async def process(payload: dict):
    print("Gate 2")
    if "attribute" in payload.keys():
        await dbCon.insert_hardwario_message(payload)
