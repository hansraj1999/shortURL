import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "main:start_server", port=8000, host="0.0.0.0", reload=True, factory=True
    )
