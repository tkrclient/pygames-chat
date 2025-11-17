import asyncio, json
from collections import deque
from picows import ws_create_server, WSMsgType, WSTransport, WSListener, WSUpgradeRequest

def websocket():
    class Handler(WSListener):
        def on_ws_connected(self, transport: WSTransport):
            print("Client connected")
            # Give new client the last amount of allotted messages
            try:
                with open("data/logs.json", "r") as file:
                    #logs = file.read()
                    logs = [json.loads(line) for line in file if line.strip()]
                #transport.send(WSMsgType.TEXT, logs.encode('utf-8'))
                transport.send(WSMsgType.TEXT, json.dumps(logs, separators=(',', ':')).encode('utf-8'))
            except FileNotFoundError:
                # Send empty response if file doesn't exist (apparently client expects message even if nothing?)
                # transport.send(WSMsgType.TEXT, b"[]")
                print("Log file not found.")

        def on_ws_frame(self, transport: WSTransport, frame: WSMsgType):
            if frame.msg_type == WSMsgType.TEXT:
                # Read incoming JSON
                message = frame.get_payload_as_ascii_text()
                try:
                    receiveJson = json.loads(message)
                    print(f"Received: {receiveJson}")

                    # Create response
                    sendJson = receiveJson

                    # Send JSON response
                    transport.send(WSMsgType.TEXT, json.dumps(sendJson).encode('utf-8'))

                    # Write to file
                    with open("data/logs.json", "r+") as file:
                        lines = file.readlines()
                        lines.append(json.dumps(sendJson) + "\n")
                        lines = lines[-30:] # How many messages to remember
                        file.seek(0) # Move file pointer to beginning
                        file.writelines(lines)
                        file.truncate()
                except json.JSONDecodeError:
                    transport.send_close(1007)  # Invalid data
                    transport.disconnect()

    async def main():
        def listener_factory(req: WSUpgradeRequest):
            return Handler()

        server = await ws_create_server(listener_factory, "localhost", 8001)
        print("Server started on ws://localhost:8001")
        await server.serve_forever()

    asyncio.run(main())

