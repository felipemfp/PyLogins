# coding: utf-8
import time
import base64
def Hides(login):
	arqui = open("logins.txt", "a")
	codi = base64.b64encode(login.encode("utf-8", 'replace'))
	codi = str(codi)
	arqui.write(codi + "\n")
	arqui.close

def save():
	rede_social = input("Entre com o nome da rede social: ")
	email = input("Entre com o seu email: ")
	senha = input("entre com a sua senha: ")
	login = ("Rede social: {rede} | Email: {email} | Senha: {senha}".format(rede = rede_social, email = email, senha = senha))
	Hides(login)

def show():
	arqui = open("logins.txt", "r")
	log = "logins"
	while log != "":
		log = arqui.readline()
		log = str(log)
		log = log[1:]
		decodi = base64.b64decode(log)
		print(decodi)
	arqui.close()

def menu(x):
	if (x == 1):
		save()
	if (x == 2):
		show()

def main():
	try:
		with open("logins.txt", "r"):
			print("Okay to start")
	except IOError:
		print("File not found\n*Creating file*")
		time.sleep(5)
		arqui = open("logins.txt", "w")
	opc = 1
	while(opc != 0):
		opc = int(input("1- ADD Logins\n2- View logins\n0- exit\n"))
		if opc == 0:
			print("Thanks!")
		else:
			menu(opc)
if __name__ == '__main__':
	main()
