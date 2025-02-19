import asyncio
from duckduckgo_search import AsyncDDGS
from fastapi import FastAPI, Query

app = FastAPI()

async def asearch(word, max_results: int = 2):
    async with AsyncDDGS() as ddgs:
        return await ddgs.atext(word, max_results=max_results)

@app.get("/get_asearch")
async def get_asearch(words: str = Query(description="Danh sách từ khóa, cách nhau bằng dấu `,`"), max_results : int = 2):
    words = [w.strip() for w in words.split(",")] 
    tasks = [asearch(w, max_results) for w in words]
    results = await asyncio.gather(*tasks)
    return {"results": dict(zip(words, results))} 





async def AI_chat(sentence):
    async with AsyncDDGS() as ddgs:  
        return await ddgs.achat(sentence, model='gpt-4o-mini')
    
@app.get("/get_ai_chat")
async def get_ai_chat(sentences: str = Query(description="Các câu, cách nhau bằng dấu `,`")):
    sentences = [s.strip() for s in sentences.split(",")] 
    tasks = [AI_chat(s) for s in sentences]
    answers = await asyncio.gather(*tasks)
    return {"answers" : dict(zip(sentences, answers))}
    

# if __name__ == "__main__":
#     asyncio.run(get_asearch("Sơn tùng, Jack", 2))
# print(asyncio.run(AI_chat("Sơn tùng mtp là ai")))
