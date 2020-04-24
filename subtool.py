# device which could be used to replace the netcat tool

import sys
import getopt
import socket
import subprocess
import time
import threading

#declaring the global variables in the process

target             = ""
execute            = ""
upload             = False
listen             = False
command            = False
upload_destination = ""
port               = 0

#declaring the syntax process which need to be seen in the process


def n():
    
    print("\n")
    
def usage():
    print( "*" * 100)
    print("*                                 netcat substitute tool                                           *")
    print("*                                                                made by:kartik mehta              *")
    print("*" * 100)
    n()
    print("                          Usage: syntax subtool.py -t target_host -p port                            ")
    n()
    print('''                    -l --listen                  -listen on the particular port for the
                                                             incoming connection''')
    
    print('''                    -e --execute-file_to_run     -executing the particular command which
                                                             is being provided for the execution''')

    print('''                    -c --command                 -the command to be provided to the proces
                                                             for the addressing''')

    print('''                    -u --upload_destination      -upon recieving the connection through to
                                                             reverse connection uploading the file the 
                                                             destination accordingly''')
    n()
    print('                     Examples:                                                                  ')
    n()
    print('                     subtool.py -t 192.168.0.126 -p 5555 -l -c                                  ')
    print('                     subtool.py -t 192.168.0.126 -p 5555 -l -u=C:\\target.exe                   ')
    print('                     subtool.py -t 192168.0.126  -p 5555 -l -e=\"cat /etc/passwd\"              ')
    print('                     echo "ABCDEFGHI" | ./subtool.py -t 192.168.0.126 -p 135                    ')
    sys.exit(0)

def main():
    
    global listen
    global target
    global execute
    global command
    global upload_destination
    global port

    if not len(sys.argv[1::]):
               usage()

# the usage function defined will come into the usage

    try:
        opts, args =getopt.getopt(sys.argv[1::],'hle:t:p:cu:',['help','listen','execute','target','command','upload'])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        
        if o in ('-h','--help'):
            usage()
        elif o in ('-e','--execute'):
            execute = a
        elif o in ('-c','--command'):
            command = True
        elif o in ('-u','--upload'):
            upload_destination = a
        elif o in ('-t','--target'):
            target = a
        elif o in ('-p','--port'):
            port = int(a)
        elif o in ('-l','--listen'):
            listen = True
        else:
            assert False,"Unhandles Exception"

#we have changed the value of the global variables accordingly in the process for the execution process which could be used accordingly

    if not listen and len(target) and port >0 :

        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

main()

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while True:
        
            recv_len = 1
            response = " "

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response)

            buffer = raw_input("")
            buffer += '\n'

            client.send(buffer)

    except:

        print(" Exception!! Exiting.")
        client.close()

def server_loop():
    
    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:

        client_socket , addr = server.accept()
        client_thread = threading.Thread(target = client_handler, args =(client_socket,))
        client_thread.start()

def run_command(command):
    
    command = command.rstrip()
    try:
        cmd = subprocess.check_output(command ,stderr = subprocess.STDOUT , shell =True)

    except:
        cmd = 'failed to execute the command!!!!'

    return cmd

def client_handler(client_socket):
    
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer =""

        while True:
            data = client_socket.recv(4096)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor=open(upload_destination,'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("successfully saved the file to %s destination"  %(upload_destination))

        except:
            client_socket.send('Failed to save the file at the destination!!!!')

    if len(execute):
        
        output = run_command(execute)
        client_socket.send(output)


    if command:

        client_socket.send('subtool.py')
        client_buffer = ""

        while "\n" in cmd_buffer:
            data = client_socket.recv(4096)
            client_buffer += data

        response = run_command(client_buffer)

        client_socket.send(response)
        
        
