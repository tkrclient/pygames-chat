import asyncio, json, os, time
from collections import deque, defaultdict
from picows import ws_create_server, WSMsgType, WSTransport, WSListener, WSUpgradeRequest

# Global or module-level
ip_message_log = defaultdict(list)
blocked_ips = {}  # ← Dictionary, not set

def is_spam(ip: str) -> bool:
    now = time.time()
    # Spam: more than 5 messages in 10-second window
    window = 2  # ← spam time window
    # Keep only timestamps from the last 10 seconds for this IP
    ip_message_log[ip] = [t for t in ip_message_log[ip] if now - t < window]
    # Add the current timestamp to the IP's message log
    ip_message_log[ip].append(now)
    # Return True if the IP sent more than 5 messages in 10 seconds
    return len(ip_message_log[ip]) > 3

def websocket():
    class Handler(WSListener):
        def __init__(self, room):
            self.room = room.lstrip("/")
            self.log_file = f"data/logs-{self.room}.json"

        def on_ws_connected(self, transport: WSTransport):
            print("Client connected")

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

            # Create file if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    pass  # Create empty file

            # Give new client the last amount of allotted messages
            try:
                with open(self.log_file, "r") as file:
                    logs = [json.loads(line) for line in file if line.strip()]
                transport.send(WSMsgType.TEXT, json.dumps(logs, separators=(',', ':')).encode('utf-8'))
            except (FileNotFoundError, json.JSONDecodeError):
                transport.send(WSMsgType.TEXT, b"[]")

        def on_ws_frame(self, transport: WSTransport, frame: WSMsgType):
            client_ip = getattr(self, 'client_ip', None)  # Get client IP stored in handler
            if not client_ip:  # If no IP (e.g., missing in transport)
                return  # Exit early

            # Check if IP is blocked
            if client_ip in blocked_ips:
                if time.time() < blocked_ips[client_ip]:
                    return  # Still blocked
                else:
                    del blocked_ips[client_ip]  # Unblock expired

            if frame.msg_type == WSMsgType.TEXT:
                # Block spam
                if is_spam(self.client_ip):
                    block_duration = 60  # ← cooldown/block time (different from spam window)
                    blocked_ips[client_ip] = time.time() + block_duration
                    return

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
                    with open(self.log_file, "r+") as file:
                        lines = file.readlines()
                        lines.append(json.dumps(sendJson) + "\n")
                        lines = lines[-30:] # How many messages to remember
                        file.seek(0) # Move file pointer to beginning
                        file.writelines(lines)
                        file.truncate()
                except json.JSONDecodeError:
                    transport.disconnect()

    async def main():
        def listener_factory(request: WSUpgradeRequest):
            try:
                client_ip = request.transport.peer_addr[0] if request.transport.peer_addr else "0.0.0.0"
            except (AttributeError, IndexError):
                client_ip = "0.0.0.0"

            if request.path in [b"/chatroom1", b"/chatroom2"]:
                handler = Handler(room=request.path.decode('utf-8'))
                handler.client_ip = client_ip  # Attach IP to handler
                return handler
                #return Handler(room=request.path.decode('utf-8'))
            return None

        server = await ws_create_server(listener_factory, "localhost", 8001)
        print("Server started on ws://localhost:8001")
        await server.serve_forever()

    asyncio.run(main())
