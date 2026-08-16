"""Process-wide determinism and outbound-network guard for cookbook tests."""

import os
import random
import socket


random.random = lambda: 0.9

if os.environ.get("CASKADA_COOKBOOK_TEST") == "1":
    _real_connect = socket.socket.connect

    def _local_only_connect(sock, address):
        host = address[0] if isinstance(address, tuple) else ""
        if host not in {"127.0.0.1", "localhost", "::1"}:
            raise RuntimeError(f"Cookbook smoke tests block outbound network access: {host}")
        return _real_connect(sock, address)

    socket.socket.connect = _local_only_connect
