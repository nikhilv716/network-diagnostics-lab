"""Run the loopback-only DNS or HTTP service for the Milestone 1 lab."""

import argparse
import ipaddress
import socketserver
import struct
from http.server import BaseHTTPRequestHandler, HTTPServer

ADDRESS = "127.0.0.1"
HOSTNAME = "orders.test"
DNS_PORT = 15353
HTTP_PORT = 8765
DNS_HEADER = struct.Struct("!6H")


class DNSHandler(socketserver.BaseRequestHandler):
    """Serve one IPv4 A record over UDP without forwarding queries."""

    def handle(self):
        packet, connection = self.request
        if len(packet) < DNS_HEADER.size:
            return
        txid, flags, questions, _, _, _ = DNS_HEADER.unpack_from(packet)
        if questions != 1 or flags & 0xF800:
            return

        offset = DNS_HEADER.size
        labels = []
        while offset < len(packet) and packet[offset]:
            size = packet[offset]
            offset += 1
            if size > 63 or offset + size >= len(packet):
                return
            labels.append(packet[offset:offset + size])
            offset += size
        question_end = offset + 5
        if question_end > len(packet):
            return

        name = b".".join(labels).lower()
        query_type, query_class = struct.unpack_from("!HH", packet, offset + 1)
        response_flags = 0x8400 | (flags & 0x0100)
        answer = b""
        if query_class != 1:
            response_flags |= 4  # Not implemented
        elif name != HOSTNAME.encode("ascii"):
            response_flags |= 3  # NXDOMAIN
        elif query_type == 1:
            address = ipaddress.IPv4Address(ADDRESS).packed
            answer = struct.pack("!HHHIH", 0xC00C, 1, 1, 30, len(address)) + address

        header = DNS_HEADER.pack(txid, response_flags, 1, bool(answer), 0, 0)
        connection.sendto(header + packet[DNS_HEADER.size:question_end] + answer,
                          self.client_address)
        name_text = name.decode("ascii", errors="backslashreplace")
        print(f"DNS {name_text} type={query_type} rcode={response_flags & 15} "
              f"answer={ADDRESS if answer else '-'}", flush=True)


class HealthHandler(BaseHTTPRequestHandler):
    """Serve the lab health endpoint."""

    def do_GET(self):
        if self.path != "/health":
            self.send_error(404)
            return
        body = b'{"status":"ok","service":"order-entry"}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", choices=("dns", "http"))
    service = parser.parse_args().service
    if service == "dns":
        server = socketserver.UDPServer((ADDRESS, DNS_PORT), DNSHandler)
    else:
        server = HTTPServer((ADDRESS, HTTP_PORT), HealthHandler)
    with server:
        print(f"READY {service} {ADDRESS}:{server.server_address[1]}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
