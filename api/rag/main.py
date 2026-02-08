from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.core.rag.rag_manager import RAGManager
import uvicorn

app = FastAPI(title="LOGIK-PROJEKT RAG API")
rag_manager = RAGManager()

class QueryRequest(BaseModel):
    query: str
    n_results: int = 5

class QueryResponse(BaseModel):
    context: str

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Retrieves relevant context for a given query."""
    try:
        context = rag_manager.query_context(request.query, n_results=request.n_results)
        return QueryResponse(context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reindex")
async def reindex_repository():
    """Triggers a full re-indexing of the repository content."""
    try:
        rag_manager.initialize_index()
        return {"message": "Re-indexing completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
