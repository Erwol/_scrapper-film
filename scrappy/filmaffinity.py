# -*- coding: utf-8 -*-

import sys
# http://stackoverflow.com/questions/34475051/need-to-install-urllib2-for-python-3-5-1
import urllib.request as urllib2
import importlib.reload as reload
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

filmaffinity = "http://www.filmaffinity.com"

pelicula = unicode(sys.argv[1].strip())
peli = unicode(pelicula.replace(" ", "%20").strip())
url = filmaffinity + "/es/advsearch.php?stext=" + peli + "&stype%5B%5D=title&country=&genre=&fromyear=&toyear="
ua = "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
h = {"User-Agent": ua}

peticion = urllib2.Request(url, headers=h)

# Descargo el recurso para luego leerlo y analizarlo
try:
	recurso = urllib2.urlopen(peticion)
except:
	print "No se ha podido conectar a la web de los resultados"
	sys.exit()

# Leo y analizo el recurso
try:
	doc = BeautifulSoup(recurso.read())
except:
	print "No se ha podido analizar correctamente el documento"
	sys.exit(-1)

# Busco en primer lugar que haya una pelicula que coincida exactamente con el criterio de busqueda
# Si no hay coincidencia exacta aborto el script.

try:
	div = doc.find("div", {"id": "adv-search-no-results"})
	if div.b.get_text() == "No se han encontrado coincidencias.":
		print "No existe ninguna pelicula que coincida con ese título"
		sys.exit(-1)
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
	print "No se ha podido conseguir la url de la pelicula"
	sys.exit()

for url in urls:
	peticion = urllib2.Request(url, headers=h)

	try:
		recurso = urllib2.urlopen(peticion)
	except:
		print "No se ha podido conectar con la web de la pelicula"
		sys.exit()

	# Analizo el documento
	try:
		doc = BeautifulSoup(recurso.read())
	except:
		print "No se ha podido leer el documento de la pelicula"
		sys.exit(-1)
	# Obtengo la nota

	try:
		nombre = doc.find("span", {"itemprop": "name"})
		year = doc.find("dd", {"itemprop": "datePublished"})
		nota = doc.find("div", {"itemprop": "ratingValue"})
		print ("Nota filmaffinity para: %s (%s) %s " % (nombre.get_text(), year.get_text(), nota['content']))
	except:
		nombre = doc.find("span", {"itemprop": "name"})
		year = doc.find("dd", {"itemprop": "datePublished"})
		nota = doc.find("div", {"class": "rate-wrapper"})
		print ("Nota filmaffinity para: %s (%s) SIN NOTA " % (nombre.get_text(), year.get_text()))

