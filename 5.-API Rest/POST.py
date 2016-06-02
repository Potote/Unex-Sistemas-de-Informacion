import SocketServer
import base64
from geopy.geocoders import Nominatim
import socket
import time
from Crypto.Cipher import AES

KEY = 'SISTEMAS DE INFORMACION'
length = 16 - (len(KEY) % 16)
KEY += bytes([length]) * length

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
		# self.request is the TCP socket connected to the client
		#Esperamos a que llegue alguna peticion.
		print "Esperando informacion"
		self.data = self.request.recv(1024).strip()
		#Mostramos la informacion contenida en nuestro paquete.
		print "{} wrote:".format(self.client_address[0])
		print self.data
		#Procesamos el paquete recibido.
		procesarInfo(self.data)
		enviarVM(self.data)
		
def recibirPaquete(serversocket):
	conn, addr = serversocket.accept();
	print "Esperando Paquete"
	message = conn.recv(1024)
	message = procesarInfo(message)
	print message
	conn.close()

def desencriptarInformacion(data):
	cipher = AES.new('SISTEMAS DE INFORMACION ', AES.MODE_CFB, 'This is an IV456')
	data = cipher.decrypt(data)
	return data
			
#Modulo que permite procesar la informacion recibida en el paquete TCP.
def procesarInfo(data):

	#Desencriptamos el mensaje
	data = desencriptarInformacion(data)
	print data
	#Eliminamos los delimitadores '#' para posteriormente pasar cada elemento a una celda de un vector
	datosrecibidos = data.split('#')
	#Insertamos en la Base de Datos de mongodb un nuevo elemento con la información del vector junto 
	#con datos como son la fecha, hora y coordenadas del rasberry pi
	
	#Coger las siete posiciones del vector
	db.dataarduinos.inerst_one(
	{
		"id.sensor" : datosrecibidos[0],
		"temperature" : datosrecibidos[1],
		"humidity" : datosrecibidos[2],
		"date" : datosrecibidos[3],
		"hour" : datosrecibidos[4],
		"coord" : {
			"latitude" : datosrecibidos[5],
			"longitude" : datosrecibidos[6],
		}
	}
	)



HOST = ''
PORT = 6666

#Cliente de MongoDB con la direccion de la maquina 1.
cliente = MongoClient("localhost:27017")
db = client.dataarduinos
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "binding"
serversocket.bind((HOST,PORT))
serversocket.listen(5)


#Bucle infinito encargado de volver a crear una conexion TCP en caso de fallar.
while 1:
	recibirPaquete(serversocket)
        
