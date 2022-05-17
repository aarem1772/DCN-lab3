import socket
import pickle
from flask import Flask, request
import logging as log



app = Flask(__name__)
BUFFER_SIZE = 1024

@app.route('/')
def home():
    return "Home page for Fibonacci Server"

def fib(n):
    if(n<0):
        return "Invalid"
    if n in {0, 1}:  # Base case
         return n
    return fib(n - 1) + fib(n - 2)



@app.route('/fibonacci')
def fibonacci():
    n = int(request.args.get('number'))
    return str(fib(n))


@app.route('/register', methods=['PUT'])
def register():
    body = request.json
    log.info(f"/register got body={body!r}")
    if not body:
        raise ValueError("body is None")
    hostname = body["hostname"]
    fs_ip    = body["fs_ip"]
    as_ip    = body["as_ip"]
    as_port  = body["as_port"]
    ttl      = body["ttl"]
    msg = ((hostname, fs_ip, "A", ttl)) 
    msg_bytes = pickle.dumps(msg)
    as_addr = (as_ip, as_port)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    log.info(f"Sending {msg} to {as_addr} via UDP socket")
    udp_socket.sendto(msg_bytes, as_addr)
    return "Registration Successful!"


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=9090,
            debug=True)