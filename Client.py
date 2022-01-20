from asyncio.windows_events import NULL
from base64 import decode
import socket
import time
host="localhost"
port=50000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))#Conecta no servidor

def caixa_mensagens(s):
    while True:
        print("-----------------------------------------------------------")
        print("Atenção as opções:\n(1)verificar e ler seus e-mails\n(2) apagar mensagens da sua caixa de entrada\n(3) enviar novas mensagens para outros usuários.\n(4)LogOut ")
        print("-----------------------------------------------------------")
        entrada=input()
        s.sendall(entrada.encode())
        if entrada=='1':#Verificar Email
            existe1=s.recv(1024)
            existe1=existe1.decode()
            if existe1=="True":
                tamanho1=s.recv(1024)
                tamanho1=int(tamanho1.decode())
                cont=0
                while cont<=tamanho1-2:
                    mostrar1=s.recv(1024)
                    print(mostrar1.decode())
                    mostrar1=NULL
                    cont=cont+1
                    time.sleep(0.1)
                    
                print("-----------------------------------------------------------")
                entrada1=input("Digite o numero referente ao email que deseja ler: ")
                print("-----------------------------------------------------------")            
                s.sendall(entrada1.encode())
                if int(entrada1)>=0 and int(entrada1) <= tamanho1-2:
                    emailfinal1=s.recv(2048)
                    emailfinal1=emailfinal1.decode()
                    print(emailfinal1)
                else:
                    print("Você deve inserir um numero valido.")
            if existe1== "False":
                print("O seu email nao possui nenhuma mensagem na caixa de entrada.")
                

            
        if entrada=='2':#Apagar Email
            existe2=s.recv(1024)
            existe2=existe2.decode()
            if existe2=="True":
                tamanho2=s.recv(1024)
                tamanho2=int(tamanho2.decode())
                cont=0
                ###ERRRO ESTA POR AQUI quando ocont ta 0 ele ja printa todas mensagens
                while cont<=tamanho2-2:
                    print(cont)
                    print(tamanho2)
                    print('esperando')
                    mostrar2=s.recv(1024)
                    print(mostrar2.decode())
                    mostrar2=NULL
                    cont=cont+1
                print("-----------------------------------------------------------")
                entrada3=input("Digite o numero referente ao email que deseja apagar: ")
                print("-----------------------------------------------------------") 
                s.sendall(entrada3.encode())
                if int(entrada3) >=0 and int(entrada3) <=tamanho2-2:           
                    emailfinal2=s.recv(2048)
                    emailfinal2=emailfinal2.decode()
                    print(emailfinal2)
                else:
                    print("Voce precisa inserir um numero valido...")
            if existe2== "False":
                print("O seu email nao possui nenhuma mensagem na caixa de entrada.")
            
            
        if entrada=='3':#Enviar Email
            print("------------------Atenção--------------------------")
            end_email=input("Digite o endereço de email do destinatario: ")
            assunto=input("Digite o Assunto do email: ")
            corpo=input("Digite o corpo do email: ")
            print("----------------Resultado Saida--------------------")
            s.sendall(end_email.encode())
            s.sendall(assunto.encode())
            s.sendall(corpo.encode())
            saida=s.recv(1024)
            print(saida.decode())
            
        if entrada=='4':#Sair conta
            main(s)        


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
        caixa_mensagens(s)
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
    while True:
        menu=s.recv(1024)#Recebe a string menu
        menu=menu.decode()#Decodifica a string menu para usar na função main
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
            print("Desconectado....")
            break
main(s)



