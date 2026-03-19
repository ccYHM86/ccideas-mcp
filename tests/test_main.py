import asyncio
import pytest
from ccideas_mcp.main import EchoServer

@pytest.mark.asyncio
async def test_echo_server_functional():
    """Test that the server actually echoes back what is sent."""
    host = "127.0.0.1"
    port = 8889  # Use a different port for testing
    server = EchoServer(host=host, port=port)
    
    # Start the server in the background
    # We use a task so we can cancel it later
    server_task = asyncio.create_task(server.start())
    
    # Give the server a moment to start
    await asyncio.sleep(0.1)
    
    try:
        # Connect a client
        reader, writer = await asyncio.open_connection(host, port)
        
        test_message = b"Hello, Echo Server!"
        writer.write(test_message)
        await writer.drain()
        
        # Read the response
        data = await reader.read(1024)
        assert data == test_message
        
        # Close connection
        writer.close()
        await writer.wait_closed()
        
    finally:
        # Shutdown the server
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

def test_echo_server_init():
    """Test initialization of the EchoServer class."""
    server = EchoServer(host="1.2.3.4", port=9999)
    assert server.host == "1.2.3.4"
    assert server.port == 9999
