import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "main:start_server",
        port=os.environ.get("PORT", 8080),
        host="0.0.0.0",
        reload=True,
        factory=True,
    )
