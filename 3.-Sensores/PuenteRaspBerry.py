#Importamos SocketServer para el socket del servidor, pymongo para el cliente
#de mongoDB, Nominatim para obtener las coordenadas de nuestro RPI y time para
#obtener informacion de la hora y fecha en la que se envia al servidor la informacion.

import SocketServer
import base64
from geopy.geocoders import Nominatim
import socket
import time
from Crypto.Cipher import AES

#Clase que nos permite gestionar las conexiones entrantes.
#Hereda de SocketServer.BaseRequestHandler. Basicamente construimos
#un handler capaz de gestionar en un loop infinito todas las conexiones
#entrantes.

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

def encriptarInformacion(data):
	print "Encriptando datos recibidos"
	cipher = AES.new('SISTEMAS DE INFORMACION ', AES.MODE_CFB, 'This is an IV456')
	length = 16 - (len(data) % 16)
	data += bytes([length]) * length
	ciphertext = cipher.encrypt(data)
	print ciphertext
	return ciphertext
			
#Modulo que permite procesar la informacion recibida en el paquete TCP.
def procesarInfo(data):
	#Anadimos informacion adicional al paquete, introduciendo la fecha,
	#hora e informacion de latitud y longitud
	data = data + "#" + str(time.strftime("%d/%m/%Y"))
	data = data + "#" + str(time.strftime("%H:%M:%S"))
	data = data + "#" + str(location.latitude)
	data = data + "#" + str(location.longitude) + "#"
	
	print data
	data = encriptarInformacion(data)
	return data
	#Enviamos la informacion a la maquina virtual de la Universidad	
	
def enviarVM(data):
	CONNECTION = (HOST, 6666)
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect(CONNECTION)	
	data = procesarInfo(data)
	clientsocket.send(data)
	clientsocket.close()

HOST = '158.49.245.179'
LOCALHOST = ''
PORT = 5555

#Geolocalizacion del Raspberry Pi
geolocator = Nominatim()
location = geolocator.geocode("108 General Margallo, Caceres")


#Bucle infinito encargado de volver a crear una conexion TCP en caso de fallar.
while 1:

	#Intentamos conectar y capturamos excepciones que podamos obtener a la hora de
	#realizar la conexion con el servidor.
	try:		
		serversocket = SocketServer.TCPServer((LOCALHOST, PORT), MyTCPHandler)
		serversocket.serve_forever()
		
	except:
		
		print("Servidor no disponible. Error de conexion.")
		print("Reconexion en 160 segundos.")
		time.sleep(10)
        
