'''
Author: Oscar Gutierrez
Email: o.guty66@gmail.com
Date: 2021-04-22
Python Version: 3.6.9
Version: 0.1.14
'''

# -*- coding: utf-8 -*-

# __LIBRARIES__ #
import sqlite3
from sqlite3 import Error

# __MAIN CODE__ #


class SQL:
    def __init__(self, name):
        self.db_name = name + '.db'
        self.create_connetion()
        self.cursorObj = self.conn.cursor()

    def create_connetion(self):  # crea la conexion a la BDD o la propia BDD
        self.conn = None  # creamos el objeto connect
        try:  # caso de omitir la ruta se crea en el directorio actual
            self.conn = sqlite3.connect(self.db_name)  # crea la BD en la ruta
        except Error as e:
            return(e)

    def find_tables(self):  # busca y almacena el nombre d ls tablas de la BDD
        self.table_names = list()
        self.cursorObj.execute(
            'SELECT name FROM sqlite_master WHERE type="table";')
        for name in self.cursorObj.fetchall():
            self.table_names.append(str(name)[2:-3])
        return self.table_names

    def create_table(self, name, p_key, typ):  # crea tablas nuevas en la BDD
        self.cursorObj.execute(
            f'CREATE TABLE {name}({p_key} {typ} PRIMARY KEY)'
        )
        self.table_names.append(name)
        
    def get_p_key(self, table, index=False): 
        p_k = self.cursorObj.execute(
        f'PRAGMA table_info({table})'
        )
        for item in p_k.fetchall():
            if item[-1] == 1 and not index:
                return item[1]
            elif item[-1] == 1 and index:
                return item[0:2]
            
    def get_column_names(self, table):
        point = self.cursorObj.execute(f'SELECT * FROM {table}')
        names = [description[0] for description in point.description]
        return names

    def insert_column(self, table, column, type):  # inserta columnas a la BDD
        self.cursorObj.execute(
            f'ALTER TABLE {table} ADD COLUMN {column} {type}'
        )
        self.commit()

    def insert_info(self, table, column, info):
        value = (str(info),)
        self.cursorObj.execute(
            f'INSERT INTO {table}({column}) VALUES(?)', value
        )
        self.commit()

    def update(self, table, column, key, info):
        self.cursorObj.execute(
            f'UPDATE {table} SET {column} = ? WHERE {key} = ?', info
        )  # UPDATE Replicas SET Modelo = val1 WHERE SN = val2
        self.commit()
        
    def insert_row(self, table, info, columns=''):
        key = self.get_p_key(table)
        self.insert_info(table, key, info[0])
        if columns == '':
            columns = self.get_column_names(table)
        n = 1
        for column in columns[1:]:
            try:
                self.update(table, column, key, (info[n], info[0]))
            except IndexError:
                pass
            n += 1

    def get_all_rows(self, table, dictionary=False, key_ind=False):
        self.cursorObj.execute(
                f'SELECT * FROM {table}'
        )
        if not dictionary:
            return self.cursorObj.fetchall()
        else:
            if not key_ind:    
                try:
                    key_ind = self.get_p_key(table, True)[0]
                except TypeError:
                        key_ind = 0
            cols = self.get_column_names(table)
            D = dict()
            for item in self.cursorObj.fetchall():
                d = dict()
                for info in item:
                    if not item.index(info) == key_ind:
                        d[cols[item.index(info)]] = info
                D[item[key_ind]] = d
            return D         

    def show_one_row(self, table, column, info):
        ind = self.get_column_names(table).index(column)
        row = [elem for elem in self.show_all_rows(table) if info == elem[ind]]
        return row

    def delete_row(self, table, column, info):
        if type(info) is not tuple:
            value = (info,)
        else:
            value = info
        self.cursorObj.execute(
            'DELETE FROM %s WHERE %s = ?' % (table, column), value
        )
        self.commit()

    def commit(self):
        self.conn.commit()


'''
    def delete_repeated(self, table):
        Permite verificar y eliminar los registros duplicados en la tabla especificada
    
    def search_info(self, table, item):
        Dos casos:
            1) Sabemos en que tabla(s) buscar
            2) No sabemos en que tabla buscar
        Busca la el/los registros que coincidan con la información facilitada.
        Retorna todo aquel registro que haya tenido coincidencia.
            
    def list(self):

    def delete(self):
'''


def run():
    db = SQL('test')
    D = db.get_all_rows('Makro', True, 1)
    for item in D:
        print(f'{item}\n \t{D[item]}')


if __name__ == '__main__':
    run()

# __NOTES__ #
'''
    __init__(name):
        {name}  hace referencia a la variable que almacena el nombre de la base
                de datos.

    create_connetion():
        Crea la conexion con la base de datos.
        
    find_tables()
        Devuelve una lista con los nombres de todas las tablas

    create_tables(name, p_key, typ):
        crea una tabla con una unica columna.
        {name}  hace referencia al nombre de la tabla a crear.
        {p_key} hace referencia al valor clave de la fila.
        {typ}   almacena el tipo de dato del valor clave.
    
    get_column_names(self, table):
        Devuelve los nombres de las columnas de table a crear
        {table} tabla de la que queremos obtener las columnas

    insert_column():
        Inserta columnas nuevas en la tabla establecida
        {table}  Nombre de la tabla
        {column} Nombre de la columna
        {type}   Establece el tipo de caracter almacenado en la columna.

    insert_info(self, table, column, info):
        Se emplea para insertar informacion en la tabla seleccionada
        en la columna establecida.
        {table}  Nombre de la tabla empleada
        {column} Columna en la que introducir la informacion
        {info}   infromacion a introducir en la columna

    update(self, table, column, key, info):
        actualiza la infromacion en la columna especificada de una cierta tabla
        {table}  Nombre de la tabla empleada
        {column} nombre de la columna a actualizar
        {key}    Nombre de la columna que almacena el key
        {info}   Tupla con la siguiente estructura:
            (val, key)
                {val} Valor nuevo a introducir en la columna establecida
                {key} Key de la fila a modificar.
    
    insert_row(self, table, key, info, columns=''):
        Inserta una fila completa de informacion
        {table} Tabla con la que trabajaremos
        {key}   Nombre de la columna key
        {info}  lista con la información a introducir en la BBDD
                la lista debe seguir el orden de las columnas
                si la lista es mas corta se cumplimenta con None
        {columns} Si esta vacia empleará el orden establecido en la
                  tabla para las columnas
                  ha de ser una lista.

    get_all_rows(self, table, dictionary=False, key_ind=False):
        Devuelve toda la infromacion de una tabla dada.
        {table} Nombre de la tabla de la que se desea saber la informacion.
        {dictionary}
            {True}  Nos devuelve la informacion en forma de diccionario con 
                    el siguiente formato:
                        {p_key : {
                            col_a : value,
                            col_b : value,
                            ...
                        }} 
            {False} Nos devuelve la infromacion en forma de lista de tuplas
        {key_ind}
            {False} emplea la primary key como key principal del programa
                    o la primera columna en caso de no tener p_key
            {n}     emplea la columna en la posición n como primary key
                    del diccionario.

    show_one_row(self, table, column, info):
        Devuelve la informacion de la fila seleccionada
        {table}  Nombre de la tabla en la que buscar la infromacion
        {column} Nombre de la columna de referencia
        {info}   Infromacion a buscar en la columna.

    list_complete():
        nos permite ver toda la informacion en una base de datos
    delete():
        eliminara la informacion especificada.

'''
# __BIBLIOGRAPHY__ #
