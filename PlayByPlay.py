from mongo_database import mongo_db, collection
from typing import List
import json
from parser import parse_cp_file
from schemas import Action

async def insert_actions(parsed: dict[str,dict[str, str]]): 
    count_mongo = await collection.count_documents({"Game": parsed["gameinfo"][0]["Game"]})
    actions_to_process =parsed["actions"][count_mongo:]
    for action in actions_to_process:
        exists = await collection.find_one({
            "Game": action["Game"],
            "Team": action["Team"],
            "Name": action["Name"],
            "Nr": action["Nr"],
            "Text": action["Text"],
            "PLTime": action["PLTime"]
        })
        if not exists:
            try:
                await collection.insert_one(action)
            except Exception as e:
                print("Insert failed:", e)

async def checker (match_id:str)->bool:
    if await collection.find_one({"Game": match_id}):
        return True
    else:
        return False

async def action_page(match_id:str, page_no:int)-> List [Action]:
    skip_count = (page_no - 1) * 5
    cursor = collection.find({"Game": str(match_id)}).sort("_id", -1).skip(skip_count).limit(5)
    results = await cursor.to_list(length=5)
    return [Action(**r) for r in results]