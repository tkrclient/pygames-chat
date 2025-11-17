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
- Extremely small codebase (more reliable, secure and auditable)
- Exposed websocket protocol, so you can directly connect to the chat with a custom web client
- Based on golang backend
- Is open source so you can customize it to your liking
- When connection is lost, it will reconnect every two seconds

## Chat Example

This application shows how to use the
[websocket](https://github.com/gorilla/websocket) package to implement a simple
web chat application.

## Running the example

The example requires a working Go development environment. The [Getting
Started](http://golang.org/doc/install) page describes how to install the
development environment.

Once you have Go up and running, you can download, build and run the example
using the following commands.

    $ go install
    $ go run *.go

To use the chat example, open http://localhost:8080/home.html in your browser.
