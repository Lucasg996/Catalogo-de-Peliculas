import tkinter as tk
from tkinter import ttk  
from model.pelicula_dao import Pelicula, crear_tabla, guardar, listar, editar,eliminar
from tkinter import messagebox

def barra__menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width=300, height= 300)

    menu_inicio = tk.Menu (barra_menu, tearoff=0)
    barra_menu.add_cascade(label= 'Inicio', menu = menu_inicio)

    menu_inicio.add_command(label='Salir', command= root.destroy)

    barra_menu.add_cascade(label= 'Consultas')
    barra_menu.add_cascade(label= 'Configuracion')
    barra_menu.add_cascade(label= 'Ayuda')

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.config(width= 480, height= 320,)
        self.id_pelicula = None
        crear_tabla()
        self.campos_pelicula()
        self.deshabilitar_campos()
        self.tabla_peliculas()
    
    def campos_pelicula(self):
        self.label_titulo = tk.Label(self, text= 'Titulo: ')
        self.label_titulo.config(font= ('Arial', 12,'bold'))
        self.label_titulo.grid(row=0, column=0, padx= 10, pady= 10)

        self.label_duracion = tk.Label(self, text= 'Duracion: ')
        self.label_duracion.config(font= ('Arial', 12,'bold'))
        self.label_duracion.grid(row=1, column=0, padx= 10, pady= 10)

        self.label_genero = tk.Label(self, text= 'Genero: ')
        self.label_genero.config(font= ('Arial', 12,'bold'))    
        self.label_genero.grid(row=2, column=0, padx= 10, pady= 10)

        self.mi_titulo = tk.StringVar()
        self.entry_titulo = tk.Entry(self, textvariable= self.mi_titulo)
        self.entry_titulo.config(width=50, font= ('Arial', 12) )
        self.entry_titulo.grid (row= 0, column=1, padx= 10, pady= 10, columnspan= 2)

        self.mi_duracion = tk.StringVar() 
        self.entry_duracion = tk.Entry(self, textvariable=self.mi_duracion)
        self.entry_duracion.config(width=50, font= ('Arial', 12) )
        self.entry_duracion.grid (row= 1, column=1, padx= 10, pady= 10, columnspan= 2)

        self.mi_genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable= self.mi_genero)
        self.entry_genero.config(width=50, font= ('Arial', 12) )
        self.entry_genero.grid (row= 2, column=1, padx= 10, pady= 10, columnspan= 2)

        self.button_nuevo = tk.Button(self, text= 'Nuevo', command= self.habilitar_campos)
        self.button_nuevo.config(width=20, font= ('Arial',12, 'bold'),fg= 'white',bg='#158645', cursor='hand2',
        activebackground= '#35BD6F')
        self.button_nuevo.grid(row=3, column=0, padx= 10, pady= 10)

        self.button_guardar = tk.Button(self, text= 'Guardar', command = self.guardar_datos)
        self.button_guardar.config(width=20, font= ('Arial',12, 'bold'),fg= 'white',bg='#1658A2', cursor='hand2',
        activebackground= '#3586DF')
        self.button_guardar.grid(row=3, column=1, padx= 10, pady= 10)

        self.button_cancelar = tk.Button(self, text= 'Cancelar', command=self.deshabilitar_campos)
        self.button_cancelar.config(width=20, font= ('Arial',12, 'bold'),fg= 'white',bg='#BD152E', cursor='hand2',
        activebackground= '#E15370')
        self.button_cancelar.grid(row=3, column=2, padx= 10, pady= 10)

    def habilitar_campos(self):
        self.mi_titulo.set('')
        self.mi_duracion.set('')
        self.mi_genero.set('')

        self.entry_titulo.config(state='normal')
        self.entry_duracion.config(state='normal') 
        self.entry_genero.config(state='normal')  
        

        self.button_guardar.config(state='normal')
        self.button_cancelar.config(state= 'normal')

    def deshabilitar_campos(self):
        self.id_pelicula = None
        self.mi_titulo.set('')
        self.mi_duracion.set('')
        self.mi_genero.set('')

        self.entry_titulo.config(state='disabled')
        self.entry_duracion.config(state='disabled') 
        self.entry_genero.config(state='disabled')  
        

        self.button_guardar.config(state='disabled')
        self.button_cancelar.config(state='disabled')

    def guardar_datos(self):
        pelicula = Pelicula(self.mi_titulo.get(),
                            self.mi_duracion.get(),
                            self.mi_genero.get())


        if self.id_pelicula == None:
            guardar(pelicula)
        
        else:
            editar(pelicula, self.id_pelicula)


        self.tabla_peliculas()

        self.deshabilitar_campos()
        

    def tabla_peliculas (self):

        self.lista_peliculas = listar()
        self.lista_peliculas.reverse()
        self.tabla = ttk.Treeview(self, column= ('Nombre','Duracion','Genero'))
        self.tabla.grid(row=4, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self,
        orient='vertical', command= self.tabla.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand= self.scroll.set)


        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='DURACION')
        self.tabla.heading('#3', text='GENERO')

        for p in self.lista_peliculas:
            self.tabla.insert('',0,text=p[0],
            values = (p[1], p[2], p[3]))   

        self.button_editar = tk.Button(self, text= 'Editar', command= self.editar_datos )
        self.button_editar.config(width=20, font= ('Arial',12, 'bold'),fg= 'white',bg='#158645', cursor='hand2',
        activebackground= '#35BD6F')
        self.button_editar.grid(row=5, column=0, padx= 10, pady= 10)

        self.button_eliminar = tk.Button(self, text= 'Eliminar', command=self.eliminar_datos)
        self.button_eliminar.config(width=20, font= ('Arial',12, 'bold'),fg= 'white',bg='#BD152E', cursor='hand2',
        activebackground= '#E15370')
        self.button_eliminar.grid(row=5, column=1, padx= 10, pady= 10)

    def editar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            self.nombre_pelicula = self.tabla.item(self.tabla.selection())['values'][0]
            self.duracion_pelicula = self.tabla.item(self.tabla.selection())['values'][1]
            self.genero_pelicula = self.tabla.item(self.tabla.selection())['values'][2]

            self.habilitar_campos()

            self.entry_titulo.insert(0, self.nombre_pelicula)
            self.entry_duracion.insert(0, self.duracion_pelicula)
            self.entry_genero.insert(0, self.duracion_pelicula)
        except:
            titulo = 'Edicion de datos'
            mensaje = 'No se ha podido editar este registro'
            messagebox.showerror(titulo,mensaje)

    def eliminar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            eliminar(self.id_pelicula)

            self.tabla_peliculas()
            self.id_pelicula = None

        except:
            titulo = 'Eliminar un registro'
            mensaje = 'No se ha seleccionado ningun registro'
            messagebox.showerror(titulo,mensaje)


