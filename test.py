import socket
import threading

path = input("Ingresar ruta al archivo que se quiere enviar: ")


class Cliente:

	def __init__(self):
		self.host = '127.0.0.1'
		self.port = 8001
		self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
            self.chat = ChatUI.Chat(usuario)
            self.thread_wait_server = threading.Thread(target=self.wait_server)
            self.thread_wait_server.start()
            self.chat.inicializar_interfaz()

        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()

    def wait_server(self):
        self.conectar()
        while(True):
            if self.chat.subir_pressed():
                self.enviar(self.chat.get_path())

    def conectar(self):
        self.s_cliente.connect((self.host,self.port))
        self.escuchador = threading.Thread(target=self.escuchar, args=())
        self.escuchador.daemon = True
        self.escuchador.start()

    def escuchar(self):
        while True:
            data = self.s_cliente.recv(1024)
            with open("./foto_cliente.jpg",'wb+') as f:
                while data:
                    f.write(data)
                    ready = select.select([self.s_cliente], [], [], 0)
                    if(ready[0]):
                        data = self.s_cliente.recv(1024)
                    else:
                        data = b''
                        self.chat.update_image("./foto_cliente.jpg")

    def enviar(self,path):
        with open(path,'rb') as f:
            data = f.read()
            self.s_cliente.send(data)
        self.chat.update_image(path)
