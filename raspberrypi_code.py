import gps 
import time 
import requests

print("Starting session...")

session = gps.gps(host="127.0.0.1", port="2947") 
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
 
print("Session successfully started!")

# Colocar URL do servidor DJANGO:
url = 'http://URL-DO-DJANGO/api/coordinates/'

# um contador pra salvar uma localização antiga a cada 10 envios:
counter = 1

while True:
	try:
		raw_data = session.next()
		
		time.sleep(5)

		if raw_data['class'] == 'TPV':
			print("Latitude is = "+str(raw_data.lat))
			print("Longitude is = "+str(raw_data.lon))
			print("Vehicle is moving at = "+str(raw_data.speed)+" KPH")
			print("The altitude is = "+str(raw_data.alt)+" m")
			print("The current date and time is = "+str(raw_data.time)+"\n")
			
			data = {
				'latitude': raw_data.lat,
				'longitude': raw_data.lon,
				'speed': raw_data.speed,
				'altitude': raw_data.alt,
				'time': raw_data.time,
			}

			response = requests.post(url, json=data)
			counter += 1

			if response.status_code == 200:
				print('Data sent successfully.')
			else:
				print("Error sending data. Code ", response.status_code)
		else:
			print("Trying to establish connection to GPS...")
	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print("No incoming data from the GPS module")
