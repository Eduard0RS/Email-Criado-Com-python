from base64 import decode
import socket
host="localhost"
port=50000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))#Conecta no servidor
menu=s.recv(1024)#Recebe a string menu
menu=menu.decode()#Decodifica a string menu para usar na função main
def login(s):#Função que faz o login no servidor.
    email=str(input("Digite seu email: "))
    s.sendall(email.encode())#passa para o servidor o email
    senha=str(input("Digite sua senha: "))
    s.sendall(senha.encode())#passa para o servidor a senha
    dado=s.recv(1024)
    print("-----------------------------------------------------------")
    print(dado.decode())
    print("-----------------------------------------------------------")
    saidaFinal=s.recv(1024)
    if saidaFinal.decode()=="1":#Login efetuado com sucesso.
        pass
    elif saidaFinal.decode()=="0":#Email ou senha incorretos.
        main(s) 
def registrar(s):#Registrar novo email e senha
    print("-----------------------------------------------------------")
    email=str(input("Digite seu email: "))
    print("-----------------------------------------------------------")
    s.sendall(email.encode())
    print("-----------------------------------------------------------")
    senha=str(input("Digite sua senha: "))
    print("-----------------------------------------------------------")
    s.sendall(senha.encode())
    dado=s.recv(1024)#atribui a variavel dado, os dados recebidos do servidor
    print(dado.decode())#Printa na tela cliente o dado recebido do servidor
    main(s)#Chama a função que contém o menu de login e cadastro. 
def main(s):#Função que contem o menu de login e cadastro.
    print("-----------------------------------------------------------")
    print(menu)
    print("-----------------------------------------------------------")
    entrada=input("Digite sua entrada: ")
    s.sendall(entrada.encode())
    if entrada=='1':
        login(s)
    if entrada=='2':
        registrar(s)
    if entrada=='9':
        s.close()
main(s)



