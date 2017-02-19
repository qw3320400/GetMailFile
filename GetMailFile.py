import poplib
import email
import cStringIO
import base64
import getpass
import os
import sys

MAIL_SERVER = "pop.163.com"
MAIL_SERVER_PORT = 110
STORE_PATH = "/Users/fangjianwei/Downloads/"

def GetMailFile():
	#connect server
	pop = poplib.POP3(MAIL_SERVER, MAIL_SERVER_PORT) 
	#login
	account = raw_input("Enter Email: ")
	password = getpass.getpass('Enter password: ') 
	pop.user(account)
	pop.pass_(password)

	#get all mail count
	mailnum, _ = pop.stat()
	for i in range(mailnum, 1, -1):
		mailmessage = pop.retr(i)
		buf = cStringIO.StringIO()
		for j in mailmessage[1]:
			print >> buf, j
		buf.seek(0)
		message = email.message_from_file(buf)
		#read mail
		for part in message.walk():
			filename = part.get_filename()
			#get file
			if filename :
				h = email.Header.Header(filename)
				dh = email.Header.decode_header(h)
				file = os.path.join(STORE_PATH, dh[0][0])

				try:
					with open(file, "wb") as f:
						f.write(part.get_payload(decode=True))
					print(file)
				except Exception as e:
					print("get file error:",e)
				filehasget = True

		if filehasget == True:
			break
	pop.quit()

if __name__ == "__main__" :
	GetMailFile()
