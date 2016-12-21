# coding: utf-8
import time
import base64
import argparse
import getpass

def check(pasw):
	sen = getpass.getpass("password again: ")
	while pasw != sen:
		print("Passwords do not match, try again")
		sen = getpass.getpass("password: ")
	return pasw

def Hides(login):
	arqui = open("logins.txt", "a")
	codi = base64.b64encode(login.encode("utf-8", 'replace'))
	codi = str(codi)
	arqui.write(codi + "\n")
	arqui.close()
	print("Saved successfully")

def mold(usr, pasw):
	login = ("Email: {e} | Senha: {s}".format(e = usr, s = pasw))
	Hides(login)

def show():
	arqui = open("logins.txt", "r")
	log = "logins"
	while log != "":
		log = str(arqui.readline())
		log = log[1:]
		decodi = base64.b64decode(log)
		print(decodi)
	arqui.close()

def args():
	log = argparse.ArgumentParser(description = 'Email e senha de um cadastro.')
	log.add_argument("--e", action = "store", dest = "opc",
		               required = False,
		               help = "Enter argument and 'yes' to save logins")
	log.add_argument("--s", action = "store", dest = "escolha",
		               required = False,
		               help = "Enter the argument and 'yes' to view logins")

	data = log.parse_args()
	if data.opc == "yes":
		usr = input("Email: ")
		pasw = getpass.getpass("password: ")
		mold(usr, check(pasw))
	elif data.escolha == "yes":
		show()

def main():
	try:
		open("logins.txt", "r")
	except IOError:
		print("File not found\n*Creating file*")
		time.sleep(5)
		arqui = open("logins.txt", "w")
	args()
if __name__ == '__main__':
	main()
