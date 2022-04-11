from typing import List
import uvicorn
import NLP


from fastapi import FastAPI

app = FastAPI()

@app.post("/Tags",response_model=List[str])
async def complete(question:NLP.question):
    return list(NLP.completeTag(question.question))



