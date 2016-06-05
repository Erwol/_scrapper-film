#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup #sudo apt-get install python-bs4

reload(sys)
sys.setdefaultencoding('utf8')

imdb = "http://www.imdb.com"

def buscar(pelicula):
	peli = unicode(pelicula.replace(" ","%20").strip())
	url = imdb + "/find?q=" + peli + "&s=tt&ttype=ft&exact=true&ref_=fn_tt_ex"
	ua = "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
	h = {"User-Agent": ua}

	peticion = urllib2.Request(url, headers=h)

	#Descargo el recurso para luego leerlo y analizarlo
	try:
		recurso = urllib2.urlopen(peticion)
	except:
		print "imdb: No se ha podido conectar a la web de los resultados"


	#Leo y analizo el recurso
	try:
		doc = BeautifulSoup(recurso.read())
	except:
		print "imdb: No se ha podido analizar correctamente el documento"


	#Busco en primer lugar que haya una pelicula que coincida exactamente con el criterio de busqueda
	#Si no hay coincidencia exacta aborto el script.
	try:
		h1 = doc.find("h1", {"class": "findHeader"})
		if h1.contents[0] == "No results found for ":
			print "imdb: No existe ninguna pelicula que coincida con ese título"
	except:
		pass


	#Llegados a este punto hay peliculas que se llaman como peli (puede haber varias)
	try:
		td = doc.findAll("td", {"class": "result_text"})
		urls = []
		for t in td:
			a = t.find("a")

			#Obtengo solo las urls de aquellas que se llamen exactamente igual
			if a.get_text().lower() == pelicula.lower():
				url = imdb + a['href']
				#print "Obteniendo pagina " + url
				urls.append(url)
	except:
		print "imdb: No se ha podido conseguir la url de la pelicula"


	lista = []

	for url in urls:
		peticion = urllib2.Request(url, headers=h)

		try:
			recurso = urllib2.urlopen(peticion)
		except:
			print "imdb: No se ha podido conectar con la web de la pelicula"
			sys.exit()

		#Analizo el documento
		try:
			doc = BeautifulSoup(recurso.read())
		except:
			print "imdb: No se ha podido leer el documento de la pelicula"
			sys.exit(-1)

		# Obtengo la nota
		try:
			h1 = doc.find("h1", {"itemprop": "name"}).get_text().strip()
			nota = float(doc.find("span", {"itemprop": "ratingValue"}).get_text().strip())
		except AttributeError:
			h1 = doc.find("h1", {"itemprop": "name"}).get_text().strip()
			nota = 0

		lista.append((h1, nota))

	#if not len(lista):
	#	lista.append((pelicula.strip(), -1))

	return lista

if __name__ == "__main__":
	buscar(unicode(sys.argv[1].strip()))
