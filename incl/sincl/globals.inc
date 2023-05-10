/* Bereckly Sockets System Calls */
.global sysc_open_socket
.global sysc_connect_to_address
.global sysc_bind_to_address
.global sysc_listen_to_incoming_data
.global sysc_accept_incoming_data
.global sysc_write_to_socket
.global sysc_read_from_socket
.global sysc_send_to_socket
.global sysc_receive_from_socket
.global sysc_close_socket

/* Address Conversion */
.global addr_inet_address_to_netbyteorder
.global addr_inet_host_to_netbyteorder
