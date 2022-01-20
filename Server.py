from asyncio.windows_events import NULL
import os
import socket
import time
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
            if str(ver[0])==str(email):
                senha=str(ver[1])
                return ["1",senha]
            cont=cont+1
        return ["0","ValueError"]
        
    elif retorno==0:#Se o arquivo nao existe então retorna que pode criar um novo cadastro
        return ["0","ValueError"]
def apagar_email(email,tamanho,entrada):
    
    os.rename(str(email)+".txt","renomeando"+str(email)+".txt")
    arq=open("renomeando"+str(email)+".txt","r")
    arq=arq.read()
    arq=arq.split("\n")
    
    arq2=open(str(email)+".txt","a")
    cont=0
    while cont<=tamanho:
        if cont !=entrada:
            arq2.write(arq[cont]+"\n")
            
        cont=cont+1
    
    arq2.close()
    os.remove("renomeando"+str(email)+".txt")

    if tamanho-1 < 0:
        
        os.remove(str(email)+".txt")
    else:
        pass
    return


    
def caixa_mensagens(conexao,email):
    while True:
        entrada=conexao.recv(1024)
        entrada=entrada.decode()
        if entrada=="1":#Verificar se existe email para ser logado
            existe1=verificar_existencia(str(email)+".txt")
            existe1=str(existe1)
            conexao.sendall(existe1.encode())
            
            if existe1=="True": #Se existe email então passa os emails para o client e espera resposta de qual email quer ver.
                arq1=open(str(email)+".txt","r")
                arq1=arq1.read()
                emails1=arq1.split("\n")
                tamanho1=str(len(emails1))                
                conexao.sendall(tamanho1.encode())
                tamanho1=int(tamanho1)
                
                cont=0
                while cont<=(tamanho1-2):#passando emails para o client                    
                    email_atual1=emails1[cont]
                    email_atual1=email_atual1.split(";")                  
                    mostrar1=("\n("+str(cont)+")"+" "+ str(email_atual1[0])+" "+str(email_atual1[1]))
                    conexao.sendall(mostrar1.encode())
                    cont=cont+1              
                    time.sleep(0.2)
              
                entrada1=conexao.recv(1024)
                entrada1=entrada1.decode()
                entrada1=int(entrada1)
               
                if entrada1>=0 and entrada1<=tamanho1-2:#se a entrada do client contiver algum email, mostra, se nao, volta
                    email_atual1=emails1[entrada1]
                    email_atual1=email_atual1.split(";")
                    saida1=("\n("+str(entrada1)+")"+" \n"+ str(email_atual1[0])+" \n"+str(email_atual1[1])+"\n"+str(email_atual1[2]))
                    conexao.sendall(saida1.encode())                    
                else:
                    pass
            else:
                pass           

        if entrada=="2":#Apagar Emails
            existe=verificar_existencia(str(email)+".txt")
            existe=str(existe)
            conexao.sendall(existe.encode())
            
            if existe=="True": #Se existe email então passa os emails para o client e espera resposta de qual email quer apagar.
                arq2=open(str(email)+".txt","r")
                arq2=arq2.read()
                emails2=arq2.split("\n")
                tamanho2=str(len(emails2))                
                conexao.sendall(tamanho2.encode())
                tamanho2=int(tamanho2)
                cont=0
                mostrar2=NULL
                while cont<=(tamanho2-2):#passando emails para o client
                    email_atual2=emails2[cont]
                    email_atual2=email_atual2.split(";")                  
                    mostrar2=("\n("+str(cont)+")"+" "+ str(email_atual2[0])+" "+str(email_atual2[1]))
                    conexao.sendall(mostrar2.encode())
                    cont=cont+1   
                    time.sleep(0.2)            
                entrada2=conexao.recv(1024)
                entrada2=entrada2.decode()
                entrada2=int(entrada2)
                
                if entrada2>=0 and entrada2<=tamanho2-2:#se a entrada do client contiver algum email, mostra, se nao, volta
                    apagar_email(email,(tamanho2-2),entrada2)
                    saida2=("Email Apagado com Sucesso")
                    conexao.sendall(saida2.encode())                    
                else:
                    pass
            else:
                pass           
                
           
            
            
        if entrada=="3":#Enviar novo email
            end_email=conexao.recv(1024)
            end_email=end_email.decode()            
            assunto=conexao.recv(1024)
            assunto=assunto.decode()
            corpo=conexao.recv(2048)
            corpo=corpo.decode()
            existe2,senha2=verifica_email(end_email)
                            
            if existe2=="1":#Se existe, então adiciona o email a caixa de entrada do destinatario.
                arq=open(str(end_email)+".txt","a")
                lista="Remetente="+str(email)+";Assunto="+str(assunto)+";Corpo="+str(corpo)+"\n"
                arq.write(lista)
                arq.close()
                saida="Email Enviado Com Sucesso."
                conexao.sendall(saida.encode())
                caixa_mensagens(conexao,email)
            if existe2=="0":#Se não existe informa que o endereço de email n existe.
                saida="O Email de Destinatario Nao Existe."
                conexao.sendall(saida.encode())
                caixa_mensagens(conexao,email)


            
            
        if entrada=="4":#Sair da conta
            server(conexao)
            
            


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
        time.sleep(0.2)
        conexao.sendall(str.encode("Indique qual entrada voce deseja:\n(1)Fazer Login\n(2)Registrar\n(9)Sair  "))
        entrada=conexao.recv(1024)
        entrada=entrada.decode()
        if entrada=="1":
            fazer_login(conexao)
        if entrada=="2":
            registrar(conexao)
        if entrada=="9":
            break

            
def start(host='localhost',port=50000):#Função que inicia o server
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen()
    print("Aguardando Conexao")
    conexao,endereco =s.accept()
    print("conectado em",conexao)
    server(conexao)    

start()