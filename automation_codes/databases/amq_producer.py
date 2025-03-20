import stomp


# Connection parameters
host = 'localhost'
port = 61613
username = 'admin'
password = 'admin'
destination = '/queue/test'

import stomp

conn = stomp.Connection(([(host, port)]))
conn.connect(username, password, wait=True)

msg = "hello 24"
 
conn.send('/queue/test', 'test message')

# Disconnect
conn.disconnect()
