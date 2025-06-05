import uvicorn
import os

if __name__ == "__main__":
    import traceback

    try:
        uvicorn.run(
            "main:start_server",
            port=8000,
            host="0.0.0.0",
            factory=True,
        )
    except Exception as e:
        print(e)
        traceback.print_exc()
        os._exit(1)
