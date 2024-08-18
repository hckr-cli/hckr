def list_servers(st):
    servers = st.servers
    server_data = []
    for _, server_list in servers.items():
        for server in server_list:
            server_data.append(server)
    return server_data, st.results.server
