
from base64 import decode
import socket
def verificar_existencia(filePath):#Função para verificar a existencia do arquivo de texto.
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False
def verifica_email(email): # Função para verificar se o email ja existe.
    retorno=verificar_existencia("arquivo_registro.txt")
    print("Verificando Se o Email existe")
    if retorno==1: #Se o arquivo existe então verifica se o email ja é cadastrado
        arq=open("arquivo_registro.txt","r")
        arq=arq.read()
        tam=arq.split("\n")
        
        cont=0
        print(len(tam))
        while cont<len(tam):
            ver=tam[cont].split(";")
            print("testando")
            print(str(ver[0]))
            print(str(email))
            print("42")
            if str(ver[0])==str(email):
                print("Email Existe")
                senha=str(ver[1])
                return ["1",senha]
            cont=cont+1
        print("Nao Existe Email")
        return ["0","ValueError"]
        
    elif retorno==0:#Se o arquivo nao existe então retorna que pode criar um novo cadastro
        return ["0","ValueError"]
def apagar_email():
    pass
def caixa_mensagens(conexao,email):
    while True:
        entrada=conexao.recv(1024)
        entrada=entrada.decode()
        if entrada=="1":#Verificar se existe email para ser ligo
            existe=verificar_existencia(str(email)+".txt")
            existe=str(existe)
            conexao.sendall(existe.encode())
            
            if existe=="True": #Se existe email então passa os emails para o client e espera resposta de qual email quer ver.
                arq=open(str(email)+".txt","r")
                arq=arq.read()
                emails=arq.split("\n")
                tamanho=str(len(emails))
                
                conexao.sendall(tamanho.encode())
                tamanho=int(tamanho)
                print(tamanho)
                cont=0
                while cont<=(tamanho-2):#passando emails para o client
                    email_atual=emails[cont]
                    email_atual=email_atual.split(";")
                    
                    mostrar=("\n("+str(cont)+")"+" "+ str(email_atual[0])+" "+str(email_atual[1]))
                    
                    conexao.sendall(mostrar.encode())
                    cont=cont+1
               
                entrada=conexao.recv(1024)
                entrada=entrada.decode()
                entrada=int(entrada)
                if entrada>=0 and entrada<=tamanho-2:#se a entrada do client contiver algum email, mostra, se nao, volta
                    email_atual=emails[entrada]
                    email_atual=email_atual.split(";")
                    saida=("\n("+str(entrada)+")"+" \n"+ str(email_atual[0])+" \n"+str(email_atual[1])+"\n"+str(email_atual[2]))
                    conexao.sendall(saida.encode())
                else:
                    pass
            else:
                pass

            

            
        if entrada=="2":#Apagar Emails
            
            pass
            
            
        if entrada=="3":#Enviar novo email
            end_email=conexao.recv(1024)
            end_email=end_email.decode()            
            assunto=conexao.recv(1024)
            assunto=assunto.decode()
            corpo=conexao.recv(2048)
            corpo=corpo.decode()
            existe2,senha2=verifica_email(end_email)
            print(existe2)                    
            if existe2=="1":
                print("Criando Arquivo")
                arq=open(str(end_email)+".txt","a")
                lista="Remetente="+str(email)+";Assunto="+str(assunto)+";Corpo="+str(corpo)+"\n"
                arq.write(lista)
                arq.close()
                saida="Email Enviado Com Sucesso."
                conexao.sendall(saida.encode())
                caixa_mensagens(conexao,email)
            if existe2=="0":
                saida="O Email de Destinatario Nao Existe."
                conexao.sendall(saida.encode())
                caixa_mensagens(conexao,email)


            
            
        if entrada=="4":#Sair da conta
            print("aqui4")
            
            


def fazer_login(conexao):#Função para logar no servidor
    email=conexao.recv(1024)
    senha=conexao.recv(1024)
    email=email.decode()
    cod,senha2=verifica_email(email)
    if cod=="1":
        if str(senha.decode())==str(senha2):
            conexao.sendall(str("Login efetuado com sucesso").encode())
            conexao.sendall(cod.encode())
            caixa_mensagens(conexao,email)
        else:        
            conexao.sendall(str("Email ou senha incorretos.").encode())
            dado="0"
            conexao.sendall(dado.encode())                   
    if cod=="0":
        conexao.sendall(str("Email ou senha incorretos.").encode())
        conexao.sendall(cod.encode()) 
    server(conexao)    
def registrar(conexao):#Função para registrar novos clientes
    email=conexao.recv(1024)
    senha=conexao.recv(1024)
    cod,nada=verifica_email(email)
    if cod=="1":
        
        conexao.sendall(str("Seu email ja esta cadastrado").encode())       
    if cod=="0":
        arq=open("arquivo_registro.txt","a")
        arq.write("\n"+str(email.decode())+";"+str(senha.decode()))
        arq.close()
        conexao.sendall(str("Email e senha cadastrados com sucesso").encode())
    server(conexao)
def server(conexao):#Função menu para login registro e sair.
    while True:
        entrada=conexao.recv(1024)
        entrada=entrada.decode()
        if entrada=="1":
            fazer_login(conexao)
        if entrada=="2":
            registrar(conexao)
        if entrada=="9":
            conexao.shutdown()
            
def start(host='localhost',port=50000):#Função que inicia o server
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen()
    print("Aguardando Conexao")
    conexao,endereco =s.accept()
    conexao.sendall(str.encode("Indique qual entrada voce deseja:\n(1)Fazer Login\n(2)Registrar\n(9)Sair  "))
    print("conectado em",conexao)
    server(conexao)    
start()