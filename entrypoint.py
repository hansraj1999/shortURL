import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "main:start_server",
        port=int(os.environ.get("PORT", 8000)),
        host="0.0.0.0",
        factory=True,
    )
