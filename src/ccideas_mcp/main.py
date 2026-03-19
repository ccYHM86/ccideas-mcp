import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EchoServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8888):
        self.host = host
        self.port = port
        self._server = None

    async def handle_echo(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        logger.info(f"Connection from {addr}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                message = data.decode()
                logger.info(f"Received {message!r} from {addr}")
                
                writer.write(data)
                await writer.drain()
        except Exception as e:
            logger.error(f"Error handling connection from {addr}: {e}")
        finally:
            logger.info(f"Closing connection from {addr}")
            writer.close()
            await writer.wait_closed()

    async def start(self):
        self._server = await asyncio.start_server(self.handle_echo, self.host, self.port)
        addr = self._server.sockets[0].getsockname()
        logger.info(f'Serving on {addr}')

        async with self._server:
            await self._server.serve_forever()

    def run(self):
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="A simple async echo server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8888, help="Port to bind to")
    args = parser.parse_args()

    server = EchoServer(host=args.host, port=args.port)
    server.run()

if __name__ == "__main__":
    main()
