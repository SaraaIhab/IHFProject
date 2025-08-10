from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import schemas
from parser import parse_cp_file
from PlayByPlay import action_page, checker, insert_actions 
from datetime import date
from mongo_database import *
from typing import List

app=FastAPI()


@app.post("/upload-cp-file/")
async def upload_cp_file(file: UploadFile = File(...)):
    file_content = await file.read()
    parsed_data = parse_cp_file(file_content)
    await insert_actions(parsed_data) 

@app.get("/PlayByPlay/matches/{match_id}/page/{page_no}", response_model= List[schemas.Action])
async def get_actions (match_id:str, page_no: int):
    if not await checker(match_id):
        raise HTTPException(status_code=404, detail="Match not found")
    return await action_page(match_id, page_no) 
