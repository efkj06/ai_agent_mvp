"""
Local test
==========
Proves that a program calling an IP address over HTTP (exactly what WeCom's
AI model will do through the tunnel) can fetch data from the gateway.

How to use:
  1. Double-click start_server.bat and leave that window open.
  2. Run:  python test_local.py
"""

import socket
import sys

import requests

PORT = 8000


def lan_ip() -> str:
    """Find this machine's address on the local network (LAN)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no data is sent; just picks the right network card
        return s.getsockname()[0]
    finally:
        s.close()


def check(name: str, url: str) -> bool:
    print(f"\n--- Test: {name}")
    print(f"    Calling: {url}")
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print("    RESULT: FAILED - could not reach the server at all.")
        print(f"    Reason: {e}")
        print("    Fix: make sure start_server.bat is running in another window.")
        return False
    if r.status_code != 200:
        print(f"    RESULT: FAILED - server answered with error code {r.status_code}.")
        return False
    print(f"    Server replied: {r.json()}")
    print("    RESULT: PASSED")
    return True


def main():
    ip = lan_ip()
    print("=" * 60)
    print("Testing whether data can be fetched from an IP address")
    print(f"This machine's LAN address is: {ip}")
    print("=" * 60)

    results = [
        check("Server alive (this machine, 127.0.0.1)", f"http://127.0.0.1:{PORT}/"),
        check("Search via loopback IP", f"http://127.0.0.1:{PORT}/search?q=orca"),
        check("Server alive via LAN IP (how another device sees us)", f"http://{ip}:{PORT}/"),
        check("Search via LAN IP", f"http://{ip}:{PORT}/search?q=orca"),
    ]

    print("\n" + "=" * 60)
    if all(results):
        print("ALL TESTS PASSED.")
        print("Data CAN be fetched from this machine through an IP address.")
        print("Next step: run start_tunnel.bat to give WeCom a public URL.")
    else:
        print(f"{results.count(False)} of {len(results)} tests FAILED. See messages above.")
        if results[0] and results[1] and not results[2]:
            print("Note: loopback worked but the LAN IP did not - this is usually")
            print("the Windows Firewall blocking Python. The Cloudflare Tunnel")
            print("will still work, because it connects through 127.0.0.1.")
    print("=" * 60)
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
