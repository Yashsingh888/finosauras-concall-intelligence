import asyncio
import websockets


async def test_connection():

    uri = "ws://127.0.0.1:8000/ws/updates"

    try:
        async with websockets.connect(uri) as websocket:

            print("WebSocket connected successfully!")
            print("Waiting for live notifications...")

            while True:
                message = await websocket.recv()

                print("\nLIVE NOTIFICATION:")
                print(message)

    except Exception as error:
        print("WebSocket error:", error)


if __name__ == "__main__":
    asyncio.run(test_connection())