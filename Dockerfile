FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y binutils patchelf upx

COPY ./pygames-chat/wsind/websocket.py /websocket.py

RUN chmod 1777 /tmp  # Ensure correct permissions

RUN pip install pyinstaller staticx picows
RUN pyinstaller --onefile --distpath /dist /websocket.py
RUN staticx --strip /dist/websocket /dist/python3

FROM scratch
COPY --from=builder /tmp /tmp
COPY --from=builder /dist/python3 /python3
ENTRYPOINT ["/python3"]
