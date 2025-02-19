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





# async def AI_chat(sentence):
#     async with AsyncDDGS() as ddgs:  
#         return await ddgs.achat(sentence, model='gpt-4o-mini')
# print(asyncio.run(AI_chat("Sơn tùng mtp là ai")))
# if __name__ == "__main__":
#     asyncio.run(get_asearch("Sơn tùng, Jack", 2))