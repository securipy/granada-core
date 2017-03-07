#!/usr/bin/python3
#-*-coding:utf-8-*-
#- utilidades class

#- Copyright (C) 2014 GoldraK & Interhack 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
# You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>

# WebSite: http://adminserver.org/
# Email: contacto@adminserver.org
# Facebook: https://www.facebook.com/pages/Admin-Server/795147837179555?fref=ts
# Twitter: https://twitter.com/4dminserver

import sys, os, datetime
sys.path.append('model')

class salida(object):
    @staticmethod

    #- Metodo de salida por defecto y de error
    def default(mensaje):
        sys.stdout.write(str(mensaje) + '\n')
    @staticmethod
    def error(mensaje):
        sys.stderr.write(str(mensaje) + '\n')

class system(object):
    @staticmethod
    def promptInit():
        return """ 
-----------------------------------------------------------------------------                         
| JarJar Copyright (C) 2014  GoldraK & Interhack                              |
| This program comes with ABSOLUTELY NO WARRANTY; for details type 'help'.  |
| This is free software, and you are welcome to redistribute it             |
| under certain conditions; type 'license' for details.                     |
-----------------------------------------------------------------------------
        """
    @staticmethod
    #- Recorre el archivo modules y devuelve los archivos .py
    def explore(path='.', search='py'):
        mod_list = {}
        counter = 0
        for root,dirs,files in os.walk(path):
            #modules just need to know the directory names
            if search == 'modules':
                for dir in dirs:
                    # avoid __cache__ dirs
                    if not dir.startswith("__"):
                        mod_list[counter] = dir
                        counter += 1
            # looking for extensions, keep GUI_*.py
            else:
                for file in [f for f in files if f.lower().endswith(search)]:
                    if 'GUI' in file:
                        #previously was [1]
                        name = root.split('/')[0]
                        module = (file.split('.py')[0]).split('GUI_')[1]
                        counter += 1
                        mod_list[counter] = module
        return mod_list
    @staticmethod
    #- Obtiene el usuario con el que ha ejecutado el programa
    def userSystem(output):
        import getpass
        user = getpass.getuser()
        if user != 'root':
            output.error(color('rojo', 'You need root user'))
            sys.exit(0)

    @staticmethod
    def license(output):
        license = open('model/info', 'r')
        for line in license:
            output.default(line)
    @staticmethod
    def version(output):
        output.default("Version: 0.1")
        output.default("CodaName: JarJar")
        output.default("Authors: GoldraK <https://twitter.com/goldrak> & Interhack <https://twitter.com/interh4ck>")
        output.default("Email: contacto@adminserver.org")

class installer(object):
    
    def __init__(self, output, translate, log):
        self.output = output
        self.translate = translate
        self.log = log
        self.system = 'debian'
    
    def install(self, package):
        print(package)

class log(object):
    @staticmethod

    #- Funcion que escribe en el log
    def write(mensaje, control=''):
        #- Obtenmos el dia actual
        dia = str(datetime.datetime.now()).split(' ')[0]

        #- Si es un error abrimos el log de error y escribimos el mensaje de error
        if control == 1:
            logError = open('logs/error.log', 'a')
            #-Escribimos el mensaje en el log de error
            mensajeError = "[" + str(datetime.datetime.now()).split('.')[0] + "]: " + mensaje
            #- Escribir el mensaje en el archivo
            logError.write(mensajeError + "\n")
            #- Cerramos el log de Error
            logError.close()

        #- Abrimos el log general
        log = open('logs/general.log', 'a')

        #- Si el mensaje esta vacio escribe un salto de linea, sino escribe la fecha con el mensaje
        if mensaje != '\n':
            mensaje = "[" + str(datetime.datetime.now()).split('.')[0] + "]: " + mensaje
            #- Escribir el mensaje en el archivo
            log.write(mensaje + "\n")
        else:
            log.write("\n")
        #- Cerramos el archivo log
        log.close()
