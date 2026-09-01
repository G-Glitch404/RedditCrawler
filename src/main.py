import os
import uvicorn

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "9091"))


def main() -> None:
    """ entry point for running the service """
    uvicorn.run(
        "src.api:app",
        host=HOST,
        port=PORT,
        reload=False,
    )


if __name__ == '__main__':
    main()
