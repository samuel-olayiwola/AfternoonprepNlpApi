
import NLP


from fastapi import FastAPI

app = FastAPI()

@app.post("/Tags")
async def complete(question:NLP.question):
    return list(NLP.completeTag(question.question))
