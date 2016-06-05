#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup  # sudo apt-get install python-bs4

reload(sys)
sys.setdefaultencoding('utf8')

fotogramas = "http://www.fotogramas.es"

def buscar(pelicula):
	peli = unicode(pelicula.replace(" ", "%20").strip())
	url = fotogramas + "/content/search?SearchText=\"" + peli + "\"&filter[]=contentclass_id:49&activeFacets[contentclass_id:49:PELÍCULAS]="
	ua = "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
	h = {"User-Agent": ua}

	peticion = urllib2.Request(url, headers=h)

	# Descargo el recurso para luego leerlo y analizarlo
	try:
		recurso = urllib2.urlopen(peticion)
	except:
		print "fotogramas: No se ha podido conectar a la web de los resultados"
		sys.exit()

	# Leo y analizo el recurso
	try:
		doc = BeautifulSoup(recurso.read())
	except:
		print "fotogramas: No se ha podido analizar correctamente el documento"
		sys.exit(-1)

	# Busco en primer lugar que haya una pelicula que coincida exactamente con el criterio de busqueda
	# Si no hay coincidencia exacta aborto el script.

	try:
		div = doc.find("div", {"class": "warning"})
		if div.h2.get_text() == "No se han encontrado resultados al buscar \"" + pelicula + "\"":
			print "fotogramas: No existe ninguna pelicula que coincida con ese título"
			sys.exit(-1)
	except:
		pass

	# Llegados a este punto hay peliculas que se llaman como peli (puede haber varias)
	# pero el buscador de fotogramas puede buscar no sólo en el título de la pelicula
	# sino que incluso puede buscar la cadena en el compositor de la banda sonora...
	try:
		div = doc.findAll("div", {"class": "teaser_text"})
		urls = []

		for t in div:
			a = t.find("a")
			# Obtengo solo las urls de aquellas que se llamen exactamente igual
			if a.h1 != None and a.h1.get_text().lower().strip() == pelicula.lower():
				url = fotogramas + a['href']
				#print "Obteniendo pagina " + url
				urls.append(url)
	except:
		print "fotogramas: No se ha podido conseguir la url de la pelicula"
		sys.exit()

	lista = []

	for url in urls:
		peticion = urllib2.Request(url, headers=h)

		try:
			recurso = urllib2.urlopen(peticion)
		except:
			print "fotogramas: No se ha podido conectar con la web de la pelicula"
			sys.exit()

		# Analizo el documento
		try:
			doc = BeautifulSoup(recurso.read())
		except:
			print "fotogramas: No se ha podido leer el documento de la pelicula"
			sys.exit(-1)

		# Obtengo la nota
		nota = 0
		try:
			h1 = doc.find("h1", {"itemprop": "name"}).get_text().strip()
			year = doc.find("time", {"itemprop": "dateCreated"}).get_text().strip()
			h1 += " (" + year + ")"
			nota = 2 * float(doc.find("span", {"class": "starValue"}).get_text().strip())
		except:
			pass

		lista.append((h1, nota))

	#if not len(lista):
	#	lista.append((pelicula.strip(), -1))

	return lista

if __name__ == "__main__":
	buscar(unicode(sys.argv[1].strip()))