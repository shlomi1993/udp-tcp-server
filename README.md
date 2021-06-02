# Client-Server

This repo documents implementation of a simple UDP server and a little more complex TCP server. Those implementation created as part of a solution for a task in Network Communications course I took as part of Computer Science degree at Bar-Ilan University.

## UDP Server - Simple DNS

In this part I've implemented a (very) basic DNS server.

You can find in this repo a dictionary named "simple_client_server" that contains two files:
1. simp_client.py - a very basic UDP client that gets a URL from the user and send it to a server via UDP.
2. simp_server.py - a UDP server that gets a URL from a client and use a local file (which simulates domains DB) to response with the IP. If this server doesn't have this IP in its file, it will pass the request to its parent, which is a similar server but with defferent DB.

## TCP Server - HTTP training

In this part I've implemented a TCP server that get a request and load resources from "resources" dictionary.

This server is a part of a bigger assignments in which we had to analyze communications between clients and server with WireShark.

![Uploading image.png…]()
