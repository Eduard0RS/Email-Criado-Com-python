
import socket
def caixa_de_entrada():
    pass
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
    if retorno==1: #Se o arquivo existe então verifica se o email ja é cadastrado
        arq=open("arquivo_registro.txt","r")
        arq=arq.read()
        tam=arq.split("\n")
        cont=0
        while cont<len(tam):
            ver=tam[cont].split(";")
            if str(ver[0])==str(email.decode()):
                senha=str(ver[1])
                return ["1",senha]
            cont=cont+1
        return ["0","ValueError"]
    elif retorno==0:#Se o arquivo nao existe então retorna que pode criar um novo cadastro
        return ["0","ValueError"]
def fazer_login(conexao):#Função para logar no servidor
    email=conexao.recv(1024)
    senha=conexao.recv(1024)
    cod,senha2=verifica_email(email)

    if cod=="1":
        if str(senha.decode())==str(senha2):
            conexao.sendall(str("Login efetuado com sucesso").encode())
            conexao.sendall(cod.encode()) 
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