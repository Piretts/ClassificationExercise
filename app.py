import os
import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction
import shutil
from PIL import Image
import sys
import json

directoryData = 'xmldata'
directoryImgs = 'images'
directoryResu = 'results'

#nel caso serva, codice per prendere in ingresso i parametri
#
#directoryData=sys.argv[0]
#directoryImgs=sys.argv[1]
#directoryResu=sys.argv[2]

#costruisco le immagini
for filename in os.listdir(directoryData):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        buildImagesInNewFolder(f, directoryImgs, directoryResu)
        
#creo il file
open(os.path.join(directoryResu, 'CocoResult'),'a').close()
#lo scrivo come json
buildJson(directoryData, os.path.join(directoryResu, 'CocoResult'))


def buildImagesInNewFolder(fileName, directoryImgs, directoryResu):
    #parsing xml
    tree = ET.parse(fileName)
    annotation = tree.getroot()
    #imgPath = tree.find('path') non lo uso per comodità nel mio esercizio
    filename = tree.find('filename').text
    imgPath = os.path.join(directoryImgs, filename)
    #controllo dimensione
    size = tree.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    #controllo se devo ridimensionare l'immagine
    modified=1
    if(width > 800 or height > 450):
        resizeImage(imgPath, os.path.join(directoryResu, filename))
        modified = 0
    else:
        copyImage(imgPath, os.path.join(directoryResu, filename)) 
    #setto le proprietà dei bound se l'immagine è stata compressa
    if(modified == 0):
        for obj in tree.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            xmax = float(bndbox.find('xmax').text)
            ymin = float(bndbox.find('ymin').text)
            ymax = float(bndbox.find('ymax').text)
            bndbox.remove(bndbox.find('xmin'))
            bndbox.remove(bndbox.find('xmax'))
            bndbox.remove(bndbox.find('ymin'))
            bndbox.remove(bndbox.find('ymax'))
            xmin = round((xmin*800)/width)
            xmax = round((xmax*800)/width)
            ymin = round((ymin*450)/height)
            ymax = round((ymax*450)/height)
            elXmin = ET.Element('xmin')
            elXmin.text = str(str(xmin))
            elXmax = ET.Element('xmax')
            elXmax.text = str(str(xmax))
            elYmin = ET.Element('ymin')
            elYmin.text = str(str(ymin))
            elYmax = ET.Element('ymax')
            elYmax.text = str(str(ymax))
            bndbox.append(elXmin)
            bndbox.append(elXmax)
            bndbox.append(elYmin)
            bndbox.append(elYmax)
        size.remove(size.find('width'))
        size.remove(size.find('height'))
        widthEl = ET.Element('width')
        heightEl = ET.Element('height')
        widthEl.text = '800'
        heightEl.text = '450'
        size.append(widthEl)
        size.append(heightEl)
        tree.write(fileName)
        
def resizeImage(fileName, directoryResu):
    im = Image.open(fileName)
    width, height = im.size
    im = im.resize((800,450),Image.ANTIALIAS)
    im.save(directoryResu)

def copyImage(fileName, directoryResu):
    shutil.copy(fileName, directoryResu)
            
#
# Non mi è chiaro molto bene il formato del json, cosa si intende per categoria (immagino siano qualcosa relativo agli object delle immagini, non so però come costruire tali informazioni dagli xml)
# e per annotazione (immagino sia un'associazione fra oggetti ed immagini). A questo punto costruirei una categoria per ogni oggetto (cane, gatto, persona, macchina, palla, magari in maniera dinamica cercando in ogni file),
# costruirei un'immagine per ogni jpg nella cartella di destinazione e creerei un'associazione per ogni oggetto nelle foto (associando per id). Trasformerei poi tutte queste liste di oggetti utilizzando un parser json e scrivendo il risultato 
# nel file creato nell'istruzione precedente
#
            
def buildJson(directoryData, CocoResu):
    #parsing xml
    categories = []
    images = []
    annotations = []
    for filename in os.listdir(directoryData):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print("Ciao :D")
            #to do -> creare categorie, immagini e annotazioni nelle apposite liste
    cocoFormat = CocoFormat(categories, images, annotations)
    file = open(CocoResu, "w")
    file.write(json.dumps(cocoFormat.__dict__, indent = 4))
    file.close()

class Category:
    def __init__(self, id, name, supercategory):
        self.id = id
        self.name = name,
        self.supercategory = supercategory
        
class Image:
    def __init__(self, id, width, height, file_name):
        self.id = id
        self.width = width
        self.height = height,
        self.file_name = file_name
        
class Annotation:
    def __init__(self, id, image_id, category_id, bbbox):
        self.id = id
        self.image_id = image_id
        self.category_id = categlory_id
        self.bbbox = bbbox

class CocoFormat:
    def __init__(self, categories, images, annotations):
        self.categories = categories
        self.images = images
        self.annotations = annotations

