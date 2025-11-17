## What this chat actually looks like
![png](screenshots/screenshot.png)

## Features of this chat
- Change username color
- Gives randomized "Guest____" username without a cookie (new user)
- Gives randomized username color without a cookie (new user)
- Remembers the last username color you had
- Remembers the last username you had
- Looks eerily similar to iogames chat (same font)
- Messages always start from the bottom, and every page reload always starts at the bottom of page
- Very fast
- Broadcasts the last 30 or so messages (remembers old messages, even when page reloads)
- Extremely small codebase (less than 200 loc (not including library))
- Exposed websocket protocol, so you can directly connect to the chat with a custom web client
- Based on python (cython) backend
- Is open source so you can customize it to your liking
- When connection is lost, it will reconnect every two seconds

## Chat Example

This application shows how to use the
picows (python3 websocket) package to implement a simple
web chat application.

## Running the example

The example requires a working Python3 development environment.
Once you have Python3 up and running, you can download, build and run the example
using the following commands.

    $ ./run.sh

To use the chat example, open http://127.0.0.1:8001 or http://localhost:8001 in your browser.
