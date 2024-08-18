import socket


def list_servers(st):
    servers = st.servers
    server_data = []
    for _, server_list in servers.items():
        for server in server_list:
            server_data.append(server)
    return server_data, st.results.server


def get_ip_addresses(all):
    ip_addresses = {"IPv4": [], "IPv6": []}
    for family, _type, _proto, _canonname, sockaddr in socket.getaddrinfo(
        socket.gethostname(), None
    ):
        if family == socket.AF_INET:  # IPv4
            if all or "127." not in sockaddr[0]:  # Skip loopback addresses for IPv4
                ip_addresses["IPv4"].append(sockaddr[0])
        elif family == socket.AF_INET6 and (all or not sockaddr[0].startswith("::1")):
            ip_addresses["IPv6"].append(sockaddr[0])
    return set(ip_addresses["IPv4"]), set(ip_addresses["IPv6"])
