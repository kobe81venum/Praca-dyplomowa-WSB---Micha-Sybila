import os
from fileinput import close
import paramiko #importujemy modół PARAMIKO do obsługi SSH
import time
from datetime import datetime

def fping():
    # router = '192.168.121.136'
    routers = open("routers")
    for line in routers:
        router_IP = line.strip()
        cmd = ('fping ' + router_IP)
        os.system(cmd)
        print(cmd, '\n')


    servers = open("servers")
    for line in servers:
        server_IP = line
        cmd = ('fping ' + server_IP)
        os.system(cmd)        
        print(cmd, '\n')


def ntp():
    czas = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    routers = open("routers")

    for line in routers:
        print(czas)
        print("logujemy sie na router " + (line))
        router_IP = line.strip()
        login = open("hasla")

        for line1 in login:
            username = line1.strip()

            for line2 in login:
                password = line2.strip()

                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=router_IP, username=username, password=password)
                print("Successfull connection to " + (router_IP) +"\n")

                remote_connection = ssh_client.invoke_shell()
                output1 = remote_connection.recv(3000)

                remote_connection.send("configure terminal\n")
                print("Configuring NTP server")
                remote_connection.send("ntp server 192.168.121.131\n")
                remote_connection.send("end\n")
                remote_connection.send("write\n")
                print()

                time.sleep(3)
                output2 = remote_connection.recv(65535)
                print((output2).decode('ascii'))

                print(("Successfully configured your device & Disconnecting from ") + (router_IP))

                ssh_client.close()
                time.sleep(3)

    routers.close()
    login.close()

def ntp_rm():
    czas = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    routers = open("routers")

    for line in routers:
        print(czas)
        print("logujemy sie na router " + (line))
        router_IP = line.strip()
        login = open("hasla")

        for line1 in login:
            username = line1.strip()

            for line2 in login:
                password = line2.strip()

                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=router_IP, username=username, password=password)
                print("Successfull connection to " + (router_IP) +"\n")

                remote_connection = ssh_client.invoke_shell()
                output1 = remote_connection.recv(3000)

                remote_connection.send("configure terminal\n")
                print("Configuring NTP server")
                remote_connection.send("no ntp server 192.168.121.131\n")
                remote_connection.send("end\n")
                remote_connection.send("write\n")
                print()

                time.sleep(3)
                output2 = remote_connection.recv(65535)
                print((output2).decode('ascii'))

                print(("Successfully configured your device & Disconnecting from ") + (router_IP))

                ssh_client.close()
                time.sleep(3)

    routers.close()
    login.close()

def backup():
    czas = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    routers = open("routers")

    for line in routers:
        print(czas)
        print("logujemy sie na router " + (line))
        router_IP = line.strip()
        login = open("hasla")

        for line1 in login:
            username = line1.strip()

            for line2 in login:
                password = line2.strip()

                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=router_IP, username=username, password=password)
                print("Successfull connection to " + (router_IP) +"\n")

                remote_connection = ssh_client.invoke_shell()
                output1 = remote_connection.recv(3000)

                print("Now making running-config backup of " + (router_IP) + "\n") # Comment for user information
                time.sleep(3)
                remote_connection.send("copy running-config tftp\n")
                remote_connection.send("192.168.121.131\n")
                remote_connection.send((router_IP)+ ".bak@" + (czas+ "\n"))
                time.sleep(3)
                print()
                time.sleep(3)

                output2 = remote_connection.recv(65535)
                print((output2).decode('ascii'))

                print(("Successfully configured your device & Disconnecting from ") + (router_IP))

                ssh_client.close()
                time.sleep(3)

    routers.close()
    login.close()
    return()

menu=True
while menu:

    print ("""
    1.connectivity check
    2.configure NTP
    3.rollback NTP
    4.backup configuration to TFTP
    5.Exit/Quit
    """)
    menu=input("What would you like to do? ") 
    if menu=="1": 
        print("\n fping started")
        fping()
    elif menu=="2":
        print("\n NTP started")
        ntp()
    elif menu=="3":
        print("\n NTP removing") 
        ntp_rm()
    elif menu=="4":
        print("\n backing up configuration") 
        backup()
    elif menu=="5":
        print("\n EXIT")
        break
    elif menu !="":
        print("\n Try again")