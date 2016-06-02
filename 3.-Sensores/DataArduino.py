#Importamos SocketServer para el socket del servidor, pymongo para el cliente
#de mongoDB, Nominatim para obtener las coordenadas de nuestro RPI y time para
#obtener informacion de la hora y fecha en la que se envia al servidor la informacion.

import SocketServer
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import time

#Clase que nos permite gestionar las conexiones entrantes.
#Hereda de SocketServer.BaseRequestHandler. Basicamente construimos
#un handler capaz de gestionar en un loop infinito todas las conexiones
#entrantes.
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
		self.data = self.request.recv(1024).strip()
		#Mostramos la informacion contenida en nuestro paquete.
		print "{} wrote:".format(self.client_address[0])
		print self.data
		#Procesamos el paquete recibido.
		procesarInfo(self.data)
      
#Modulo que permite procesar la informacion recibida en el paquete TCP.  
def procesarInfo(data):
	#Eliminamos los delimitadores '#' para posteriormente pasar cada elemento a una celda de un vector
	datosrecibidos = data.split('#')
	#Insertamos en la Base de datos de mongodb un nuevo elemento con la informacion del vector junto
	# con datos como son la fecha, hora y coordenadas del raspberry pi	
	db.dataarduinos.insert_one(
	{
		"id_sensor" : datosrecibidos[0],
		"temperature" : datosrecibidos[1],
		"humidity" : datosrecibidos[2],
		"date" : time.strftime("%d/%m/%Y"),
		"hour" : time.strftime("%H:%M:%S"),
		"coord" : {
					"latitude" : location.latitude, 
					"longitude" : location.longitude
					}
	}
	)

HOST = ''
PORT = 5555

#Geolocalizacion del Raspberry Pi
geolocator = Nominatim()
location = geolocator.geocode("108 General Margallo, Caceres")

#Cliente de MongoDB con la direccion de la maquina 1.
client = MongoClient("158.49.245.179:27017");
db = client.dataarduinos

#Bucle infinito encargado de volver a crear una conexion TCP en caso de fallar.
while 1:

	#Intentamos conectar y capturamos excepciones que podamos obtener a la hora de
	#realizar la conexion con el servidor.
	try:		
		serversocket = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

		serversocket.serve_forever()
		
	except:
		
		print("Servidor no disponible. Error de conexion.")
		print("Reconexion en 160 segundos.")
		serversocket.close()
		time.sleep(160)
        
