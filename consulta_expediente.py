import PySimpleGUI as sg
from buscar import buscar_dados, buscar_todos
import csv
from csv import writer
from site_url import url
import os

class TelaDados:
    def __init__(self):
            size = os.path.getsize('datos.csv')
            if size == 0:
                with open('datos.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    clientes = csv.reader(csvfile, delimiter=',', quotechar='|')
                    cliente = ['Nombre','nie','numero','año']
                    writer_object = writer(csvfile)
                    writer_object.writerow(cliente)

            with open('datos.csv', 'r', newline='', encoding='utf8') as csvfile:
                clientes = csv.reader(csvfile, delimiter=',', quotechar='|')                    
                for row in clientes:
                    nombre = str((row[0]))
                    nie = str((row[1]))
                    numero = str((row[2]))
                    ano = str((row[3]))
           
            layout = [
                [sg.Text('Consulta telemática de expediente de nacionalidad española por residencia')], [sg.HSeparator()],
                [sg.Text('Nombre:', size=(7,0)), sg.VSeperator(), sg.Input(f'{nombre}', size=(40,0), key='nombre'), sg.Text('Nombre completo', size=(20,0))],
                [sg.Text('NIE:', size=(7,0)),sg.VSeperator(), sg.Input(f'{nie}', size=(40,0), key='nie'), sg.Text('Su NIE', size=(6,0))],
                [sg.Text('Número:', size=(7,0)),sg.VSeperator(), sg.Input(f'{numero}',size=(40,0), key='numero'), sg.Text('Ejemplo: R *500001* /2015', font=('Arial', 10, 'bold'), size=(25,0))],
                [sg.Text('Año:', size=(7,0)),sg.VSeperator(), sg.Input(f'{ano}', size=(40,0), key='ano'), sg.Text('Ejemplo: R500001 / *2015*', font=('Arial', 10, 'bold'), size=(25,0))],
                [sg.HSeparator()],
                [sg.Button('Guardar'),sg.Button('Buscar'), sg.Button('Buscar todos'), sg.Button('Limpiar campos'), sg.Cancel('Cancelar')]
            ]
            
            self.janela = sg.Window('Busca Expediente V1.0',icon="espana.ico", auto_size_buttons=True, size = (750,250), finalize=True).layout(layout)
            
    def salvar(self):
        if self.values['nombre'] == 'Nombre' or self.values['nombre'] == '':
            sg.Popup('El nombre no está rellenado')   
        elif self.values['nie'] == 'nie' or self.values['nie'] == '':
            sg.Popup('El NIE no está rellenado')   
        elif self.values['numero'] == 'numero' or self.values['numero'] == '':
            sg.Popup('El número no está rellenado')   
        elif self.values['ano'] == 'ano' or self.values['ano'] == 'año':
            sg.Popup('El año no está rellenado')
        else:
            with open('datos.csv', newline='', encoding='utf8') as csvfile:
                clientes = csv.reader(csvfile, delimiter=',', quotechar='|')                    
                for row in clientes:
                    nombre = str((row[0]))
                    nie = str((row[1]))
                    numero = str((row[2]))
                    ano = str((row[3]))
            if nombre == 'Nombre' or nie == 'nie' or numero == 'numero' or ano == 'año':
                with open('datos.csv','w', newline='', encoding='utf8') as csvfile:
                    cliente = [self.values['nombre'],
                        self.values['nie'], 
                        self.values['numero'], 
                        self.values['ano'],
                    ]
                    writer_object = writer(csvfile)
                    writer_object.writerow(cliente)
                    sg.Popup('Datos guardados exitosamente')   
            else:
                with open('datos.csv', 'a', newline='', encoding='utf8') as csvfile:
                    cliente = [self.values['nombre'],
                                self.values['nie'], 
                                self.values['numero'], 
                                self.values['ano'],
                            ]
                    
                    writer_object = writer(csvfile)
                    writer_object.writerow(cliente)
                    sg.Popup('Datos guardados exitosamente')   


    def clear_input(self):
        self.janela['nombre'].update('') 
        self.janela['nie'].update('') 
        self.janela['numero'].update('') 
        self.janela['ano'].update('') 

    def Iniciar(self): 
        while True:
            url = 'https://sede.mjusticia.gob.es/eConsultas/inicioNacionalidad'             
            self.event, self.values = self.janela.Read()
            nie = self.values['nie']
            numero = self.values['numero']
            ano = self.values['ano']
            

            if self.event == 'Guardar':
                self.salvar()

            if self.event == 'Buscar':
                buscar_dados(url, nie, numero, ano)

            if self.event == 'Buscar todos':
                buscar_todos()

            if self.event == 'Limpiar campos':
                self.clear_input()
                              
            
            if self.event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if self.event == sg.WINDOW_CLOSED:
                break

        self.janela.close()

if __name__ == '__main__':
    tela = TelaDados()
    tela.Iniciar()


