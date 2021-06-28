__doc__ = """
Subir archivos al respaldo externo de la empresa, mediante el api de mega
Use:
   python uploadToMega.py --empresa "Empresa" --ruta "c:\\python\\"
"""
import argparse
import contextlib
import sys
import datetime
import time
import zipfile
import os, subprocess
#import pprint
from mega import Mega

@contextlib.contextmanager
def stopwatch(message):
    """Context manager para saber cuanto tiempo se ejecuta un bloque de codigo en especifico."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Tiempo en ejecucion %s: %.3f' % (message, t1 - t0))

parser = argparse.ArgumentParser(description='Realiza respaldos de carpetas o archivos en la cuenta dropbox')
parser.add_argument('--empresa',dest="empresa",type=str,nargs='+',help='Empresa')
parser.add_argument('--ruta',dest='ruta',nargs='+',help='Carpetas a copiar FULLPATH')
args = parser.parse_args()
nombre_empresa = args.empresa[0]
carpeta = args.ruta[0]

with stopwatch('Comprimir_Carpeta'):
    zip_file = zipfile.ZipFile(nombre_empresa + '.zip','w')
    for f in os.listdir(carpeta):
        zip_file.write(carpeta + '\\'  + f, compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

mega = Mega()
m = mega.login("diegominetti@fewlines.com.ar","Ab.+63200")

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#print('archivo:', archivo)

empresa = m.find(nombre_empresa)
#print(empresa)
if empresa is None :
    print("Crea carpeta de Empresa " + nombre_empresa)
    m.create_folder(nombre_empresa)
    empresa = m.find(nombre_empresa)
#details = m.get_user()
#print(details)
#file = m.find(archivo)
#m.delete(file[0])
#print((m.delete(file[0])))
#m.empty_trash()
#print((m.empty_trash()))

ahora = datetime.datetime.now()
anteriores_a = ahora - datetime.timedelta(days = 30)
#anteriores_a = ahora - datetime.timedelta(minutes = 5)

files = m.get_files()
for file in files:
    if files[file]['p']==empresa[0]:
        #archivos adentro de la carpeta de la empresa
        if (datetime.datetime.fromtimestamp(files[file]['ts']) <= anteriores_a):
            #print(files[file]['h'])
            m.delete(files[file]['h'])
        #print(files[file]['a']['n'])
#pprint.pprint(files)
m.empty_trash()

print("Sube el archivo " + ahora.strftime('%d_%m_%Y_%H_%M_%S')+"_"+nombre_empresa+".zip")
with stopwatch('Subir_Archivo'):
    file = m.upload(nombre_empresa+".zip", empresa[0], dest_filename=ahora.strftime('%d_%m_%Y_%H_%M_%S')+"_"+nombre_empresa+".zip")
print("Archivo subido con exito!!")
#print(file)
m.get_upload_link(file)
