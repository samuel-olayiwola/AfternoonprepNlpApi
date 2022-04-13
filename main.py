from typing import List
import uvicorn
import NLP


from fastapi import FastAPI

app = FastAPI()

@app.post("/Question2Tags",response_model=List[str])
async def complete(question:NLP.question):
    return list(NLP.completeTag(question.question))



@app.post("/Tags2Questions",response_model=dict)
async def Tags2Questions(tags:NLP.tags):
    return NLP.tagsToQuestions(tags.tags)


@app.post("/TheoryAnswer",response_model=str)
async def TheoryAnswer(question:NLP.question):
    return NLP.getTheoryAnswer(question.question)



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8050, log_level='debug')






