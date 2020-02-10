import smtpd
import asyncore

IP, PORT = '127.0.0.1', 1025

server = smtpd.DebuggingServer((IP, PORT), None)
print('Debugging SMTP server is listening at: %s:%s' % (IP, str(PORT)))

asyncore.loop()

