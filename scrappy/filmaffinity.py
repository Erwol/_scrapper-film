#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup  # sudo apt-get install python-bs4

reload(sys)
sys.setdefaultencoding('utf8')

filmaffinity = "http://www.filmaffinity.com"

def buscar(pelicula):
	peli = unicode(pelicula.replace(" ", "%20").strip())
	url = filmaffinity + "/es/advsearch.php?stext=" + peli + "&stype%5B%5D=title&country=&genre=&fromyear=&toyear="
	ua = "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
	h = {"User-Agent": ua}

	peticion = urllib2.Request(url, headers=h)

	# Descargo el recurso para luego leerlo y analizarlo
	try:
		recurso = urllib2.urlopen(peticion)
	except:
		print "filmaffinity: No se ha podido conectar a la web de los resultados"

	# Leo y analizo el recurso
	try:
		doc = BeautifulSoup(recurso.read())
	except:
		print "filmaffinity: No se ha podido analizar correctamente el documento"

	# Busco en primer lugar que haya una pelicula que coincida exactamente con el criterio de busqueda
	# Si no hay coincidencia exacta aborto el script.

	try:
		div = doc.find("div", {"id": "adv-search-no-results"})
		if div.b.get_text() == "No se han encontrado coincidencias.":
			print "filmaffinity: No existe ninguna pelicula que coincida con ese título"
	except:
		pass

	# Llegados a este punto hay peliculas que se llaman como peli (puede haber varias)
	try:
		div = doc.findAll("div", {"class": "mc-title"})
		urls = []

		for t in div:
			a = t.find("a")
			# Obtengo solo las urls de aquellas que se llamen exactamente igual
			if a.get_text().lower().strip() == pelicula.lower():
				url = filmaffinity + a['href']
				#print "Obteniendo pagina " + url
				urls.append(url)
	except:
		print "filmaffinity: No se ha podido conseguir la url de la pelicula"

	lista = []

	for url in urls:
		peticion = urllib2.Request(url, headers=h)

		try:
			recurso = urllib2.urlopen(peticion)
		except:
			print "filmaffinity: No se ha podido conectar con la web de la pelicula"

		# Analizo el documento
		try:
			doc = BeautifulSoup(recurso.read())
		except:
			print "filmaffinity: No se ha podido leer el documento de la pelicula"

		# Obtengo la nota
		try:
			nombre = doc.find("span", {"itemprop": "name"}).get_text().strip()
			year = doc.find("dd", {"itemprop": "datePublished"}).get_text().strip()
			nombre += " (" + year + ")"
			nota = float(doc.find("div", {"itemprop": "ratingValue"})['content'].strip())
		except:
			nombre = doc.find("span", {"itemprop": "name"}).get_text().strip()
			year = doc.find("dd", {"itemprop": "datePublished"}).get_text().strip()
			nombre += " (" + year + ")"
			nota = 0

		lista.append((nombre, nota))

	#if not len(lista):
	#	lista.append((pelicula.strip(), -1))

	return lista

if __name__ == "__main__":
	buscar(unicode(sys.argv[1].strip()))