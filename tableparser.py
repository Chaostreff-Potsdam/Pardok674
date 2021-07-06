#!/usr/bin/env pyhton3
#FCKAFD
from lxml import etree as et

result_data = []

def parse_page(tree, page):
	is_default_table = True

	pagetree = page

	ressort_header = pagetree.xpath('text[text()="Ressort"]')
	zuwendungsempfaenger_header = pagetree.xpath('text[text()="Zuwendungsempfänger"]')
	zweck_header = pagetree.xpath('text[text()="Zweck"]')	
	art_header = pagetree.xpath('text[text()="Art der Förderung "]')
	betrag_header = pagetree.xpath('text[text()="Betrag (in €)"]')
	
	#Rückzahlungs type pages skip for now
	rueckzahlung_header = pagetree.xpath('text[text()=" Höhe der "]')
	if (len(rueckzahlung_header) == 1) : return False

	if (len(ressort_header) != 1) : return False 
	if (len(zuwendungsempfaenger_header) != 1) : return False 
	if (len(zweck_header) != 1) : return False 
	if (len(art_header) != 1) : return False 
	if (len(betrag_header) != 1) : return False 
	
	ressort_left = ressort_header[0].attrib["left"]
	zuwendungsempfaenger_left = zuwendungsempfaenger_header[0].attrib["left"]
	zweck_left = zweck_header[0].attrib["left"]
	art_left = art_header[0].attrib["left"]
	betrag_left = betrag_header[0].attrib["left"]


	#extract all page children
	children = page.getchildren()
	child_it = iter(children)

	#skip forward to first datapoint
	while (next(child_it).text != "Betrag (in €)"): pass 


	datapoint={"Ressort":"", "Zuwendungsempfänger":"", "Zweck":"", "Art":"", "Betrag":""}

	while (child := next(child_it, None)) is not None:
		child_left = child.attrib["left"]
		if (child_left == ressort_left): datapoint["Ressort"] += child.text + " "
		if (child_left == zuwendungsempfaenger_left): datapoint["Zuwendungsempfänger"] += child.text+" "
		if (child_left == zweck_left): datapoint["Zweck"] += child.text + " "
		if (child_left == art_left): datapoint["Art"] += child.text + " "
		#after betrag close datapoint and make new one
		if (" €" in child.text): 
			datapoint["Betrag"] += child.text
			datapoint_stripped = { k:v.strip() for k, v in datapoint.items()}
			result_data.append(datapoint_stripped)
			datapoint = {"Ressort":"", "Zuwendungsempfänger":"", "Zweck":"", "Art":"", "Betrag":""}

	return True


#read file
tree = et.parse("674.xml")
pages = tree.findall('page')

#print how many pages we can parse 
print("Es gibt ", len(pages), " Seiten")
parsable_pages = 0

#iterate all pages
for page in pages: 
	if parse_page(tree, page):
		parsable_pages = parsable_pages + 1

print("Wir können ", parsable_pages, " Seiten (zunächst ohne Rückzahlungs-Einträge) verstehen")
#output result dict to console
for datapoint in result_data:
	print(datapoint)

print("Wir können ", len(result_data)," Datensätze erzeugen")

