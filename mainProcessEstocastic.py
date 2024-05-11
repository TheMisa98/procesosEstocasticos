from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
from scipy.optimize import linprog as opt
matplotlib.use('TkAgg')

#PONER ACENTOS A DECISIÓN

class AppProcesos(object):
    #Estos son las variables que usan todos los métodos

    #COLORES
    #main_color="misty rose" #color de frame
    main_color = "#1A5276"
    titulo_c = "#2ECC71" #color del título, lo uso para el fondo

    #FUENTES
    f= ('Helvetica', 18) #fuente para titulos
    btn_f= ('Helvetica', 12) #fuente para botones

    #FRAMES
    root=Tk() #root es la ventana principal
    frame= Frame(root, bg=main_color, height=40) #frame principal que cambia con cada método
    titulo_f = Frame(root, bg=titulo_c, height=50) #frame que guarda el título
    titulo_txt = Label(titulo_f, text="PROCESOS ESTOCÁSTICOS", bg=titulo_c, font=f) #texto del título


    #VARIABLES
    min = False #Si el problema minimiza
    edos = 1 #número de estados
    dec = 0 #número de decisiones
    dict_decisiones = dict() #diccionario que guarda las matrices de decisiones
    dict_costos = dict() #diccionario que guarda los costos

    """
    Es importante saber que dict_decisiones es un diccionario de diccionarios de arreglos,
    al llamar a:
    #   dict_decisiones[A] devuelve las decisiones disponibles en el estado A
    #   dict_decisiones[A][B] devuelve el arreglo asignado a las probabilidades de A en la
        decisión B
    #  dict_decisiones[A][B][C] devuelve la probabilidad de pasar del estado A
        al estado C en la decisión B.
    El diccionario se armó de esta manera para simplificar el encontrar la matriz
    de cada política
    """

    """Métodos de AppProcesos():
        crearGUI: Abre la portada, define las posiciones de la barra, titulo, creditos y el frame principal
    """

    def __init__(self):
        self.crearGUI()

    def crearGUI(self):
        """tk.set_appearence_mode("dark")
        tk.set_default_color_theme("dark-blue")"""
        root=self.root
        root.geometry("600x400")

        f=self.f
        btn_f = self.btn_f
        #root.geometry("500x500")
        #print("\nPara root\n")
        #print(root.configure().keys(    ))
        #COLORES DE FONDO

        creditos_c = "#1A5276"
        barra_c = "#D5DBDB"


        titulo_f=self.titulo_f
        creditos_f= Frame(root, bg=creditos_c, height=40)
        portada_f= self.frame
        barra_f= Frame(root, bg=barra_c, width=60)
        titulo_c=self.titulo_c
        barra_f.pack(side="left", fill="y")
        titulo_f.pack(side="top", fill="x")
        creditos_f.pack(side="bottom", fill="x")
        portada_f.pack(side="top", fill="both", expand=True)


        self.inicio()
        #Título del programa
        label=self.titulo_txt
        label.pack(pady=12, padx=20)

        """menu = Menu(root)
        item = Menu(menu)
        item.add_command(label='Caminata')
        menu.add_cascade(label='Modo', menu=item)"""

        #Integrantes en portada_f


        #BOTONES DE LA barra_f

        inicio_btn = Button(
            barra_f,
            text='Inicio',
            font=btn_f,
            command=lambda:self.inicio(),
            bg=barra_c,
            fg='black',
            width=8,
            relief="flat",
            highlightbackground=barra_c,
            activebackground=titulo_c
            )


        decisiones_btn = Button(
            barra_f,
            text='Decisiones',
            font=btn_f,
            command=lambda:self.decisiones(),
            bg=barra_c,
            fg='black',
            width=8,
            relief="flat",
            highlightbackground=barra_c,
            activebackground=titulo_c
            )

        prueba_btn = Button(
            barra_f,
            text='Prueba',
            font=btn_f,
            command=lambda:self.prueba(),
            bg=barra_c,
            fg='black',
            width=8,
            relief="flat",
            highlightbackground=barra_c,
            activebackground=titulo_c
            )

        inicio_btn.pack()
        decisiones_btn.pack()
        prueba_btn.pack()

        #root.config(menu=menu)
        root.mainloop()

    # def prueba(self):
    #     self.edos = 3
    #     self.dec = 3
    #     self.min = 0

        """self.dict_decisiones = {'0': {'0': [0.0, 0.875, 0.0625, 0.0625]},
            '1': {'0': [0.0, 0.75, 0.125, 0.125], '2': [1.0, 0.0, 0.0, 0.0]},
            '2': {'0': [0.0, 0.0, 0.5, 0.5], '1': [0.0, 1.0, 0.0, 0.0], '2': [1.0, 0.0, 0.0, 0.0]},
            '3': {'2': [1.0, 0.0, 0.0, 0.0]}}
        self.dict_costos = {'0': {'0': 0.0},
            '1': {'0': 0.1, '2': 0.6},
            '2': {'0': 0.3, '1': 0.4, '2': 0.6},
            '3': {'2': 0.6}}"""

        """self.dict_decisiones = {'0': {'0': [0.0, 0.875, 0.0625, 0.0625]},
            '1': {'0': [0.0, 0.75, 0.125, 0.125], '2': [1.0, 0.0, 0.0, 0.0]},
            '2': {'0': [0.0, 0.0, 0.5, 0.5], '1': [0.0, 1.0, 0.0, 0.0], '2': [1.0, 0.0, 0.0, 0.0]},
            '3': {'2': [1.0, 0.0, 0.0, 0.0]}}
        self.dict_costos = {'0': {'0': 0.0},
            '1': {'0': 1000.0, '2': 6000.0},
            '2': {'0': 3000.0, '1': 4000.0, '2': 6000.0},
            '3': {'2': 6000.0}}"""



        # self.dict_decisiones = {'0': {'0': [0.4, 0.5, 0.1], '1': [0.7, 0.2, 0.1], '2': [0.2, 0.5, 0.3]},
        #     '1': {'0': [0.1, 0.7, 0.2], '1': [0.3, 0.6, 0.1], '2': [0.0, 0.7, 0.3]},
        #     '2': {'0': [0.1, 0.2, 0.7], '1': [0.1, 0.7, 0.2], '2': [0.0, 0.2, 0.8]}}
        # self.dict_costos = {'0': {'0': 280.0, '1': 220.0, '2': 258.0},
        #     '1': {'0': 250.0, '1': 110.0, '2': 255.0},
        #     '2': {'0': 220.0, '1': -130.0, '2': 300.0}}


        """
        {'0': {'0': [0.0, 0.875, 0.0625, 0.0625]},
            '1': {'0': [0.0, 0.75, 0.125, 0.125], '2': [1.0, 0.0, 0.0, 0.0]},
            '2': {'0': [0.0, 0.0, 0.5, 0.5], '1': [0.0, 1.0, 0.0, 0.0], '2': [1.0, 0.0, 0.0, 0.0]},
            '3': {'2': [1.0, 0.0, 0.0, 0.0]}}
        {'0': {'0': 0.0},
            '1': {'0': 1000.0, '2': 6000.0},
            '2': {'0': 3000.0, '1': 4000.0, '2': 6000.0},
            '3': {'2': 6000.0}}
        """

        """
        {'0': {'0': [0.4, 0.5, 0.1], '1': [0.7, 0.2, 0.1], '2': [0.2, 0.5, 0.3]},
            '1': {'0': [0.1, 0.7, 0.2], '1': [0.3, 0.6, 0.1], '2': [0.0, 0.7, 0.3]},
            '2': {'0': [0.1, 0.2, 0.7], '1': [0.1, 0.7, 0.2], '2': [0.0, 0.2, 0.8]}}
        {'0': {'0': 280.0, '1': 220.0, '2': 258.0},
            '1': {'0': 250.0, '1': 110.0, '2': 255.0},
            '2': {'0': 220.0, '1': -130.0, '2': 300.0}}
        """

        #decisiones = {'0': {'0': [0.875, 0.125], '1': [0.125, 0.875]}, '1': {'0': [0.875, 0.125], '1': [0.125, 0.875]}}
        #costos = {'0': {'0': 14.0, '1': 0.0}, '1': {'0': 14.0, '1': 75.0}}

        # self.menuDecisiones()

    def inicio(self):
        root=self.root
        frame=self.frame
        c=self.main_color
        for widget in frame.winfo_children():
            widget.destroy()
        #frame=Frame(root, bg=c)
        frame.pack(side="top", fill="both", expand=True)
    def decisiones(self):
        root=self.root
        frame=self.frame
        c=self.main_color
        label = self.titulo_txt

        self.dict_decisiones=dict()
        self.dict_costos= dict()
        label['text'] = "CADENAS CON DECISIONES"
        validation = root.register(only_numbers)
        edos = 0
        dec = 0

        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)

        for widget in frame.winfo_children():
            widget.destroy()
        #frame=Frame(root, bg="Misty rose")
        frame.pack(side="top", fill="both", expand=True)
        edos_label = Label(frame, text="Número de estados: ", width=25,height=1, bg=c)
        dec_label = Label(frame, text="Número de decisiones: ", width=25, height=1, bg = c)
        edos_txt = Entry(frame, bg=c)
        dec_txt = Entry(frame, bg=c)
        edos_txt.bind("Entry", "<Down>", self.next_widget)
        edos_txt.bind("Entry", "<Up>", self.prev_widget)
        dec_txt.bind("Entry", "<Down>", self.next_widget)
        dec_txt.bind("Entry", "<Up>", self.prev_widget)

        aux_bool = BooleanVar()
        min = Checkbutton(frame, text="Minimizar", onvalue=1, offvalue=0, bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            variable=aux_bool)

        ant_btn= Button(frame, text="Regresar", bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.inicio())
        sig_btn = Button(
            frame,
            text="Siguiente",
            bg= c,
            relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.decision(0, edos_txt.get(), dec_txt.get(), aux_bool.get())
        )

        edos_label.grid(row=1, column=1)
        edos_txt.grid(row=1, column=2)
        dec_label.grid(row=2, column=1)
        dec_txt.grid(row=2, column=2)
        ant_btn.grid(row=4, column=1)
        sig_btn.grid(row=4, column=2)
        min.grid(row= 3, column=1)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(3, weight=1)


    def decision(self, n, edos, dec, min=0 , regreso=False):

        if not self.validateInt(edos) or not self.validateInt(dec):
            return False
        edos=int(edos)
        dec=int(dec)

        dic=self.dict_decisiones
        costos = self.dict_costos

        if n==0 and not regreso:
            self.min = min
            self.edos = edos
            self.dec = dec
            for i in range(edos):
                d = dict()
                co = dict()
                dic.update({str(i) : d})
                costos.update({str(i) : co})
        print(n)
        print(edos)
        print(dic)
        print(costos)
        #print(frame.winfo_children())
        root=self.root
        frame=self.frame
        c=self.main_color
        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = f"DECISIÓN {n}"
        txt = Label(frame, bg=c, text=f"Selecciona los estados para los cuales la decisión {n} aplica")
        txt.pack()
        check= []
        checked = []

        for i in range(edos):
            aux_bool = BooleanVar()
            aux_btn = Checkbutton(frame, text=f'Estado {i}', onvalue=1, offvalue=0, bg=c, relief="flat",
                highlightbackground=c,
                activebackground=c,
                variable=aux_bool)
            aux_btn.pack()
            checked.append(aux_bool)
            check.append(aux_btn)

        sig_btn= Button(frame, text="Siguiente", bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.matrizDecision(checked, n))
        ant_btn= Button(frame, text="Regresar", bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.matrizDecision(checked, n-1, regreso = True))
        ant_btn.pack(side="left")
        sig_btn.pack(side="right")

    def matrizDecision(self,mat, decision, regreso=False):
        if decision < 0:
            self.decisiones()
            return False
        print("matdec")
        dic = self.dict_decisiones
        cos = self.dict_costos
        decisiones=[]
        index=0
        edos = self.edos
        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Down>", self.next_widget)
        root.bind_class("Entry", "<Up>", self.prev_widget)
        dec=0
        print(dic)
        if regreso:
            for i in dic:
                try:
                    print(dic[i][str(decision)])
                    if dic[i][str(decision)] == []:
                        del dic[i][str(decision)]
                    else:
                        index+=1
                        decisiones.append(int(i))
                        print("entra")
                except:
                    pass
        if(index==0):
            for btn in mat:
                if btn.get():
                    decisiones.append(index)
                    dec = dec+1
                index=index+1
            print(decisiones)
        dec=index
        for widget in frame.winfo_children():
            widget.destroy()
        """frame=Frame(frameO, bg=c)
        frame.pack(side="top", fill="both", expand=True)"""

        #Label(frame, text="Ingresa la matriz de transiciones", bg=c, relief="flat").grid(row=0, column=0)
        self.reiniciarGrid(frame)
        """for i in range(edos+3):
            frame.grid_rowconfigure(i, weight=0)
            frame.grid_columnconfigure(i, weight=0)"""

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(index+3, weight=1)
        frame.grid_columnconfigure(edos+3, weight=1)


        for i in range(edos):
            indice_cols = Label(frame, text=str(i), bg="White", relief="flat", width=5)
            indice_cols.grid(row=1, column=i+2)
            """frame.grid_rowconfigure(i+1, weight=1)
            frame.grid_columnconfigure(i+1, weight=1)"""

        mat= dict()
        costos = dict()

        Label(frame, text="Costo", bg=c).grid(row=1, column=edos+2)

        for i in decisiones:

            ##AQUÍ MISMO SE DEBE PEDIR EL INGRESO DE LA MATRIZ CON LOS VALORES DE P
            Label(frame, text=str(i), bg="white", width=5).grid(row=i+2, column=1)
            vector=[]
            for j in range(edos):
                proba_ent = Entry(frame, bg="white", relief="flat", width=5)
                try:
                    if regreso:
                        print(dic[str(i)][str(decision)][j])
                        proba_ent.insert(0, str(dic[str(i)][str(decision)][j]))
                except:
                    pass
                proba_ent.bind("Entry", "<Down>", self.next_widget)
                proba_ent.bind("Entry", "<Up>", self.prev_widget)
                proba_ent.grid(row=i+2, column=j+2)
                vector.append(proba_ent)

            costo_ent = Entry(frame, bg="white", relief="flat", width=5)
            costo_ent.bind("Entry", "<Down>", self.next_widget)
            costo_ent.bind("Entry", "<Up>", self.prev_widget)
            costo_ent.grid(row=i+2, column=edos+2)
            try:
                print(cos[str(i)][str(decision)])
                costo_ent.insert(0, str(cos[str(i)][str(decision)]))
            except:
                print("vacio")
            costos.update({str(i) : costo_ent})
            mat.update({str(i): vector}) #Guarda la matriz de Entry en un diccionario

            vector= None
            aux_array = [] #ESTE ARRAY DEBE GUARDAR LAS PROBAS DE TRANS

            d = dic[str(i)]
            co = cos[str(i)]

            d.update({str(decision):aux_array})
            co.update({str(decision): 0})

            dic.update({str(i) : d})
            cos.update({str(i) : co})


        sig_btn = Button(frame, text="Siguiente", bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.comprobar(mat, dic, decision, costos, cos),
            width=5)
        sig_btn.grid(row=index+3, column=edos+3)

        ant_btn = Button(frame, text="Anterior", bg=c, relief="flat",
            highlightbackground=c,
            activebackground=self.titulo_c,
            command=lambda:self.decision(decision, str(self.edos), str(self.dec),regreso=True),
            width=5)
        ant_btn.grid(row=index+3, column=0)

        #self.frame=frame
        print(dic)

    def next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def prev_widget(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def comprobar(self, matriz, dicc, dec, costos_ent, costos):
        print(matriz)
        for row in matriz:
            print(matriz[row])
            sum = 0
            vector=[]
            costo = 0
            if not self.validateFloat(costos_ent[row].get()):
                print("El costo no es un número")
                return False
            costo= self.Float(costos_ent[row].get())
            for proba in matriz[row]:
                print(proba.get())
                if not self.validateFloat(proba.get()):
                    print("No es número")
                    return False
                num = self.Float(proba.get())
                if num<0 or num>1:
                    print("No está entre 0 y 1")
                    return False
                sum+= num
                vector.append(num)
            if round(sum,6)!= 1:
                print("La suma no es 1")
                return False
            costos[str(row)].update({str(dec) : costo})
            dicc[str(row)].update({str(dec): vector})
        print(dicc)
        print(costos)
        self.dict_decisiones = dicc
        self.dict_costos = costos
        if dec+1>=self.dec:
            self.menuDecisiones()
        else:
            self.decision(dec+1, str(self.edos), str(self.dec))
        return True

    def menuDecisiones(self):
        print("Menu decisiones")
        root=self.root
        frame=self.frame
        c=self.main_color
        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = f"MENÚ DECISIONES"
        altura = 2

        #Botones de opciones
        btn_enum = Button(frame, bg=c, text="Enumeración", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.enumeracion())

        btn_simplex = Button(frame, bg=c, text="PPL", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.simplex())

        btn_mejor = Button(frame, bg=c, text="Mejoramiento", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.mejoramiento())

        btn_desc = Button(frame, bg=c, text="Mejoramiento con Descuentos", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.descuentos())

        btn_aprox = Button(frame, bg=c, text="Aproximaciones Sucesivas", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.aproximaciones())
        btn_ant = Button(frame, bg=c, text="Regresar", height=altura,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.inicio())
        btn_enum.pack(fill='x')
        btn_simplex.pack(fill='x')
        btn_mejor.pack(fill='x')
        btn_desc.pack(fill='x')
        btn_aprox.pack(fill='x')
        btn_ant.pack(fill='x')

    def enumeracion(self):
        root=self.root
        frame=self.frame
        c=self.main_color


        for widget in frame.winfo_children():
            widget.destroy()

        label = self.titulo_txt
        label['text'] = "Enumeracion exhaustiva"

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")
        pols = Text(frame, wrap=WORD, bg=c, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0)
        side_scroll.config(command = pols.yview)
        pols.pack(padx=5, pady=5)

        print("Enumeraciones")
        edos = self.edos

        politica = np.zeros(edos)
        matriz = np.zeros((edos, edos))
        costos = np.zeros(edos)
        self.numero=0
        self.optimo=0
        self.genPolitica(0, politica, matriz, costos, pols)

        pols.tag_config(str(self.optimo), background= self.titulo_c)
        pols.config(state=DISABLED)

    def genPolitica(self, estado, politica, matriz, costos, pols):
        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos
        if estado>=edos:
            print("La política es: ", politica)
            self.numero+=1
            self.solveEnum(matriz, costos, politica, pols)
            return True
        for i in dicc[str(estado)]:
            politica[estado] = int(i)

            """print(f"cost[str({estado})]")
            print(cost[str(estado)])
            print(f"dicc[str({estado})]")
            print(dicc[str(estado)])"""
            costos[estado]= cost[str(estado)][i]
            matriz[estado]= dicc[str(estado)][i]
            #print("La matriz generada es: ", matriz)
            #print("El costo generado es: ", costos)
            self.genPolitica(estado+1, politica, matriz, costos, pols)

    def solveEnum(self, mat, costos, politica, pols):
        edos= self.edos
        #print("Se encuentra Pi")
        matriz=mat.copy()
        matriz = matriz.transpose()

        for i in range(edos):
            matriz[i][i] = matriz[i][i]-1

        matriz[-1] = np.ones(edos)

        b = np.zeros(edos)
        b[-1] = 1
        #print("Matriz a resolver")
        #print(matriz)
        sol = np.linalg.solve(matriz, b )
        print("Solución: ")
        print(sol)
        print("Costo esperado")
        esperado = np.dot(sol, costos)
        print(esperado)
        self.agregar(politica, esperado, pols)

    def agregar(self, politica, costo, pols):
        frame = self.frame
        c=self.main_color
        string=""
        for i in politica:
            string = string + str(int(i)) + ", "
        string= string[:-2]
        if self.numero==1:
            self.optimo = round(costo, 4)
        if self.min:
            if self.optimo > round(costo, 4):
                self.optimo = round(costo, 4)
        else:
            if self.optimo < round(costo, 4):
                self.optimo = round(costo, 4)
        pols.insert(END, f"{self.numero}.- Política ("+string + f") = {round(costo, 4)}\n")
        pols.tag_add(f"{round(costo, 4)}", f"{self.numero}.0", f"{self.numero}.100")

    def simplex(self):
        print("Simplex")

        root=self.root
        frame=self.frame
        c=self.main_color
        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = "PPL"

        btn_ant = Button(frame, bg=c, text="Regresar", height=1,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        btn_resolver = Button(frame, bg=c, text="Resolver", height=1,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.metodoSimplex(A, B, C))
        btn_resolver.pack(side="bottom",fill='x')

        #fig = matplotlib.figure.Figure(figsize=(6, 5), dpi=100, facecolor=c)
        fig = matplotlib.figure.Figure(facecolor=c, figsize=[10,10]) #, figsize=[10,10]
        ax = fig.add_subplot(111, facecolor=c, frame_on = False)


        #CAMBIAR pols
        canvas = FigureCanvasTkAgg(fig, master=frame)
        frame.configure(height=500, width = 700)
        canvas.get_tk_widget().configure(height=500, width = 700)


        axfreq = fig.add_axes([0.1, 0, 0.85, 0.05])
        spos = Slider(axfreq, label='Pos', valmin= 0, valmax= 1, valinit=0)

        self.spos = spos
        self.ax= ax

        spos.on_changed(self.updateAxis)
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)


        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos


        Z = ""
        dir=""
        if self.min:
            dir="min"
            Z= Z+"Min z ="
        else:
            dir="max"
            Z= Z+"Max z ="

        sa = ""
        """
        Se va a resolver el sistema
        Opt C^T Y
        s.a. A Y = B
        """
        #Vector de costos C
        C=[]
        #Matriz A
        A=[]
        #Vector de disponibilidad B
        B=[]
        #Restricción arbitraria
        R=[]
        #Diccionario de indices
        ind=dict()
        indice=0

        if self.min:
            signo=1
        else:
            signo=-1

        for estado in dicc:
            ind.update({estado: dict()})
            for decision in dicc[estado]:
                #Se arma el vector de costos
                C.append(signo * cost[estado][decision])
                #Se arma la primer restricción sum(yik)=1
                R.append(1)
                #Se agrega el indice asignado a y_ik
                ind[estado].update({decision: indice})
                indice += 1
                Z=Z+f"{cost[estado][decision]}  y_ {{ {estado} {decision} }} + "
                sa = sa + f" y_{{ {estado}{decision} }} +"
        #Agregamos la disponibilidad 1 de sum(yik)=1
        B.append(1)
        #Agregamos la primer restricción
        A.append(R)


        sa = sa[ : -2]
        Z= Z[ :-2]
        Z= "$" + Z + "$"
        print(Z)
        ax.clear()
        ax.text(0, 0.95, Z, fontsize=10)


        print(sa+ " = 0")
        ax.text(0, 0.85, "s.a.", fontsize=10)
        ax.text(0.1, 0.85, "$" + sa + " = 1$", fontsize=10)


        for estado in dicc:
            #Se reinicia la restricción en ceros
            R=np.zeros(indice)

            print(f"\n\t Estado {estado}")
            Y = ""
            for decision in dicc[estado]:
                Y = Y+ f"y_{{ {estado}{decision} }} + "
                #Agregamos y_jk a la restricción
                R[ind[estado][decision]] = 1
            Y= Y[ : -2]

            PkY = "" #P_ij (k) y_ik
            for estado2 in dicc:
                for decision in dicc[estado2]:
                    if dicc[estado2][decision][int(estado)] != 0:
                        #Restamos  P_ij(k) y_ik a la restricción
                        R[ind[estado2][decision]] -= dicc[estado2][decision][int(estado)]
                        if dicc[estado2][decision][int(estado)] != 1:
                            PkY = PkY + f"{dicc[estado2][decision][int(estado)]} y_{{ {estado2}{decision} }} + "
                        else:
                            PkY = PkY + f"y_{{ {estado2}{decision} }} + "
            #Agregamos la restricción a la matriz A
            A.append(R)
            B.append(0)
            PkY = PkY[ : -2]

            print(Y+ " = " + PkY)
            ax.text(0.1, 0.85-0.1*(int(estado)+1), "$" + Y+ " = " + PkY + "$", fontsize=10)

        canvas.draw()

    def metodoSimplex(self, A, B, C):
        print("Metodo Simplex")

        if self.min:
            signo=1
        else:
            signo=-1

        result = opt(method="highs", A_eq = A, b_eq = B, c=C)
        print("Las variables básicas son")
        print(result.x)
        print("Con un costo asignado de")
        print(signo*result.fun)
        y = result.x
        optimo = result.fun

        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos


        root=self.root
        frame=self.frame
        c=self.main_color
        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = "PPL"

        btn_ant = Button(frame, bg=c, text="Regresar", height=1,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        Label(frame, bg=c, text=f"Con un costo asignado de: {signo*round(optimo,4)}").pack(side="top")
        textopol = Label(frame, bg=c, text="")
        textopol.pack(side="top", fill="x")

        """side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")"""
        side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")

        frame2 = Frame(frame, bg=c)
        frame2.pack(fill="both", expand=False)
        self.acomodarGrid(frame2)
        """
        self.reiniciarGrid(frame2)

        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(2, weight=1)
        frame2.grid_columnconfigure(2, weight=1)
        frame2.grid_columnconfigure(4, weight=1)

        Label(frame2, text=" ").grid(row=0, column=0)
        Label(frame2, text=" ").grid(row=2, column=2)
        Label(frame2, text=" ").grid(row=2, column=4)"""

        pols = Text(frame2, wrap=WORD, bg=c, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0, width=20)
        side_scroll.config(command = pols.yview)

        pols2 = Text(frame2, wrap=WORD, bg=c, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0)


        #indice auxiliar
        ind_aux = 0

        politica = []
        for estado in dicc:
            sum=0
            for decision in dicc[estado]:
                espacio=""
                if int(round(y[ind_aux],4)==0): espacio="\t"
                pols.insert(END, f"y{estado}{decision}= {round(y[ind_aux],4)}\t \n")
                pols2.insert(END, f"Entonces D{estado}{decision} = {int(round(y[ind_aux],4)!=0)}\n")
                if round(y[ind_aux],4)!=0 :
                    sum+=1
                    politica.append(int(decision))
                #Label(frame, bg=c, text=).pack()
                ind_aux += 1
                ultimo=decision
            if sum==0:
                politica.append(int(ultimo))
        textopol.config(text=f"La política óptima es: {politica}\n")


        pols.pack(side="left")
        pols2.pack()
        pols.config(state=DISABLED)
        pols2.config(state=DISABLED)

    def reiniciarGrid(self, frame):
        for row_num in range(10):
            frame.rowconfigure(row_num, weight = 0)
            frame.columnconfigure(row_num, weight = 0)

    def acomodarGrid(self, frame):
        for row_num in range(frame.grid_size()[1]):
            frame.rowconfigure(row_num, weight = 1)
            frame.columnconfigure(row_num, weight = 1)
    def updateAxis(self, val):
        pos = val
        self.ax.axis([pos,pos+1,0,1])
        #self.fig.canvas.draw_idle()

    def mejoramiento(self):
        print("Mejoramiento")
        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = "Mejoramiento"

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        Label(frame, bg=c, text="Ingresa la política inicial: ").pack(pady=25)

        politica_grid = Frame(frame, bg=c)
        politica_grid.pack(fill='both')
        politica_grid.grid_rowconfigure(0, weight=1)
        politica_grid.grid_columnconfigure(0, weight=1)
        politica_grid.grid_rowconfigure(2, weight=1)
        politica_grid.grid_columnconfigure(edos+1, weight=1)

        vector = []
        for i in range(edos):

            ent = Entry(politica_grid, bg=c, highlightbackground=c,width=5)
            ent.grid(row=1, column=i+1)
            ent.bind("Entry", "<Up>", self.prev_widget)
            ent.bind("Entry", "<Down>", self.next_widget)
            vector.append(ent)

        sig_btn = Button(
            frame,
            text="Siguiente",
            bg= c,
            relief="flat",
            highlightbackground=c,
            activebackground="IndianRed1",
            command=lambda:self.isPolitica(vector)
        )
        sig_btn.pack()

    def isPolitica(self, vector):
        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos

        politica = np.zeros(edos)
        count=-1
        for i in vector:
            count+=1
            string = i.get()
            if not self.validateInt(string):
                print(string, " no es número")
                return False

            """try:
                a = dicc[string]
            except:
                print(string, " no es un estado")
                return False"""

            politica[count] = int(string)


        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")
        text = Text(frame, bg=c,wrap=WORD, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0)
        side_scroll.config(command = text.yview)
        text.pack(padx=20, pady=5)

        Rn=politica.copy()
        Rn[0]+= 1

        print("Empezamos a iterar")
        comparacion = Rn == politica
        it = 0
        while not comparacion.all():
            print(f"\tITERACION {it}\n")
            text.insert(END, f"\n\t ITERACIÓN {it}\n")
            it += 1
            Rn=politica.copy()
            matriz = np.zeros((edos, edos))
            costos = np.zeros(edos)
            estado = 0
            for pol in politica:
                pol = int(pol)
                matriz[estado] = dicc[str(estado)][str(pol)]
                matriz[estado][-1]= -1
                costos[estado] = - cost[str(estado)][str(pol)]
                estado+=1

            for i in range(edos-1):
                matriz[i][i]-= 1

            print("Matriz a resolver")
            print(matriz)
            print("costos")
            print(costos)
            sol = np.linalg.solve(matriz, costos)
            print("Solución: ")
            print(sol) # vector de Vi, g(r)
            gr=sol[-1]
            sol[-1]=0
            print(f"g(r) = {gr}")
            text.insert(END, f"g(R) = {round(gr, 4)}\n")

            cont=0
            for i in sol:
                print(f"V{cont} = {i}")
                text.insert(END, f"V{cont} = {round(i,4)}\n")
                cont+=1
            """print("Costo esperado")
            esperado = np.dot(sol, costos)
            print(esperado)
            if(signo * esperado > signo * optimo):
                optimo = esperado"""

            print("Mejoramiento de política")
            if self.min:
                signo = 1
            else:
                signo = -1
            for estado in range(edos):
                estado = int(estado)
                optimo = signo * 2**15
                vector = np.zeros(edos)
                index = 0
                print(f"Estado {estado}:")
                for decision in dicc[str(estado)]:
                    print(f"\tDecisión {decision}: ")
                    vector = dicc[str(estado)][decision]
                    Cij = cost[str(estado)][decision]
                    optimizar = np.dot(vector, sol)
                    optimizar += Cij
                    optimizar -= sol[estado]
                    print("\t\t",optimizar)
                    if self.min:
                        comp = optimizar < optimo
                    else:
                        comp = optimizar > optimo
                    if comp:
                        index = decision
                        politica[estado] = int(decision)
                        optimo = optimizar
                print(f"\t\tEl optimo es {optimo} en la decisión {index}\n\n")

            print("\nLa politica nueva es: ")
            print(politica)
            text.insert(END, f"La politica nueva es: {politica}\n")
            comparacion = Rn == politica
        text.insert(END, f"Terminamos con la política {politica}, que tiene un costo asociado de {gr}")
        text.tag_add("colorear", "end-1c linestart",  "end-1c lineend")
        text.tag_config("colorear", background = self.titulo_c)
        text.config(state=DISABLED)


    def descuentos(self):
        print("Descuentos")
        print("Mejoramiento")
        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = "Descuentos"

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        Label(frame, bg=c, text="Ingresa la política inicial: ").pack(pady=25)

        politica_grid = Frame(frame, bg=c)
        politica_grid.pack(fill='both')
        politica_grid.grid_rowconfigure(0, weight=1)
        politica_grid.grid_columnconfigure(0, weight=1)
        politica_grid.grid_rowconfigure(2, weight=1)
        politica_grid.grid_columnconfigure(edos+1, weight=1)

        Label(frame, bg=c, text="Ingresa el factor de descuento: ").pack(pady=25)
        desc = Entry(frame, bg=c, highlightbackground=c,width=5)
        desc.pack(padx=20)
        vector = []
        for i in range(edos):

            ent = Entry(politica_grid, bg=c, highlightbackground=c,width=5)
            ent.grid(row=1, column=i+1)
            ent.bind("Entry", "<Up>", self.prev_widget)
            ent.bind("Entry", "<Down>", self.next_widget)
            vector.append(ent)

        sig_btn = Button(
            frame,
            text="Siguiente",
            bg= c,
            relief="flat",
            highlightbackground=c,
            activebackground="IndianRed1",
            command=lambda:self.metodoDesc(vector, desc.get())
        )
        sig_btn.pack()

    def metodoDesc(self, vector, alpha):
        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos
        politica = np.zeros(edos)
        count=-1
        if not self.validateFloat(alpha):
            return False
        alpha = self.Float(alpha)

        for i in vector:
            count+=1
            string = i.get()
            if not self.validateInt(string):
                print(string, " no es número")
                return False

            """try:
                a = dicc[string]
            except:
                print(string, " no es un estado")
                return False"""

            politica[count] = int(string)

        Rn=politica.copy()
        Rn[0]+= 1

        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')


        side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")
        text = Text(frame, bg=c,wrap=WORD, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0)
        side_scroll.config(command = text.yview)
        text.pack(padx=20, pady=5)


        print("Empezamos a iterar")
        comparacion = Rn == politica
        it = 0
        while not comparacion.all():
            print(f"\n\tITERACION {it}\n")
            text.insert(END, f"\n\tITERACIÓN {it}\n")
            it += 1
            Rn=politica.copy()
            matriz = np.zeros((edos, edos))
            costos = np.zeros(edos)
            estado = 0
            for pol in politica:
                pol = int(pol)
                matriz[estado] = dicc[str(estado)][str(pol)]
                matriz[estado] = alpha * matriz[estado]
                costos[estado] = - cost[str(estado)][str(pol)]
                estado+=1

            for i in range(edos):
                matriz[i][i]-= 1

            print("Matriz a resolver")
            print(matriz)
            print("costos")
            print(costos)
            sol = np.linalg.solve(matriz, costos)
            print("Solución: ")
            print(sol) # vector de Vi, g(r)
            """gr=sol[-1]
            sol[-1]=0
            print(f"g(r) = {gr}")"""
            cont=0
            for i in sol:
                text.insert(END, f"V{cont} = {round(i,4)}\n")
                print(f"V{cont} = {i}")
                cont+=1

            """print("Costo esperado")
            esperado = np.dot(sol, costos)
            print(esperado)
            if(signo * esperado > signo * optimo):
                optimo = esperado"""

            print("\nMejoramiento de política ")
            if self.min:
                signo = 1
            else:
                signo = -1
            for estado in range(edos):
                estado = int(estado)
                optimo = signo * 2**15
                vector2 = np.zeros(edos)
                index = 0
                print(f"Estado {estado}:")
                for decision in dicc[str(estado)]:
                    print(f"\tDecisión {decision}: ")
                    vector2 = dicc[str(estado)][decision]
                    Cij = cost[str(estado)][decision]
                    optimizar = np.dot(vector2, sol)
                    optimizar = alpha * optimizar
                    optimizar += Cij
                    print("\t\t",optimizar)
                    if self.min:
                        comp = optimizar < optimo
                    else:
                        comp = optimizar > optimo
                    if comp:
                        index = decision
                        politica[estado] = int(decision)
                        optimo = optimizar
                print(f"\t\tEl optimo es {optimo} en la decisión {index}\n\n")

            text.insert(END, f"La nueva política es: {politica}\n")

            print("\nLa politica nueva es: ")
            print(politica)
            comparacion = Rn == politica
        text.insert(END, f"Terminamos con la política {politica}")
        text.tag_add("colorear", "end-1c linestart",  "end-1c lineend")
        text.tag_config("colorear", background = self.titulo_c)
        text.config(state=DISABLED)

    def aproximaciones(self):
        print("Aprox")
        print("Mejoramiento")
        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()
        label = self.titulo_txt
        label['text'] = "Aproximaciones"

        btn_ant = Button(frame, bg=c, text="Regresar", height=1,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        #Label(frame, bg=c, text="Ingresa la política inicial: ").pack(pady=25)

        politica_grid = Frame(frame, bg=c)
        politica_grid.pack(fill='both')
        politica_grid.grid_rowconfigure(0, weight=1)
        politica_grid.grid_columnconfigure(0, weight=1)
        politica_grid.grid_rowconfigure(2, weight=1)
        politica_grid.grid_columnconfigure(edos+1, weight=1)

        Label(frame, bg=c, text="Ingresa el factor de descuento: ").pack(pady=15)
        desc = Entry(frame, bg=c, highlightbackground=c,width=5)
        desc.pack(padx=20)

        Label(frame, bg=c, text="Ingresa el número de iteraciones: ").pack(pady=15)
        iter = Entry(frame, bg=c, highlightbackground=c,width=5)
        iter.pack(padx=20)

        Label(frame, bg=c, text="Ingresa la tolerancia: ").pack(pady=15)
        tol = Entry(frame, bg=c, highlightbackground=c,width=5)
        tol.pack(padx=20)
        """
        for i in range(edos):

            ent = Entry(politica_grid, bg=c, highlightbackground=c,width=5)
            ent.grid(row=1, column=i+1)
            ent.bind("Entry", "<Up>", self.prev_widget)
            ent.bind("Entry", "<Down>", self.next_widget)
            vector.append(ent)
        """

        sig_btn = Button(
            frame,
            text="Siguiente",
            bg= c,
            relief="flat",
            highlightbackground=c,
            activebackground="IndianRed1",
            command=lambda:self.metodoAprox(desc.get(), iter.get(), tol.get())
        )
        sig_btn.pack(side="bottom", fill="x")

    def metodoAprox(self, alpha, N, epsilon):
        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos


        root=self.root
        frame=self.frame
        c=self.main_color
        root.bind_class("Entry", "<Up>", self.prev_widget)
        root.bind_class("Entry", "<Down>", self.next_widget)
        edos=self.edos

        for widget in frame.winfo_children():
            widget.destroy()

        btn_ant = Button(frame, bg=c, text="Regresar", height=2,
            activebackground=self.titulo_c, relief='flat', highlightbackground=c,
            command = lambda:self.menuDecisiones())
        btn_ant.pack(side="bottom",fill='x')

        side_scroll = Scrollbar(frame, orient="vertical")
        side_scroll.pack(side="right", fill="y")
        text = Text(frame, wrap=WORD, bg=c, yscrollcommand = side_scroll.set, highlightbackground=c, borderwidth=0)
        side_scroll.config(command = text.yview)
        text.pack(padx=5, pady=5)

        politica = np.zeros(edos)
        if not (self.validateFloat(alpha) and self.validateInt(N)  and self.validateFloat(epsilon)) :
            return False
        alpha = self.Float(alpha)
        N = int(N)
        epsilon = self.Float(epsilon)

        Rn=politica.copy()
        Rn[0]+= 1
        print("Iniciamos encontrando los mínimos de los costos")

        if self.min:
            signo = 1
        else:
            signo = -1

        V = np.zeros(edos)

        for estado in cost:
            optimo = signo * 2**15
            for decision in cost[estado]:
                if self.min:
                    comp = cost[estado][decision] < optimo
                else:
                    comp = cost[estado][decision] > optimo
                if comp:
                    optimo = cost[estado][decision]
                    pi = decision
            V[int(estado)] = optimo
            politica[int(estado)]= pi
        print(V)
        text.insert(END, "\t ITERACIÓN 0\n")
        cont=0
        for i in V:
            text.insert(END, f"V{cont} = {round(i,4)}\n")
            print(f"V{cont} = {i}")
            cont+=1
        text.insert(END, f"Comenzamos con la política {politica}\n")
        print("Empezamos a iterar")

        comparacion = Rn == politica

        it = 0 #Número de iteraciones
        tolerancia=False
        while not (comparacion.all() or tolerancia or N<=it):
            it += 1
            print(f"\n\t ITERACION {it}\n")
            text.insert(END, f"\n\t ITERACION {it}\n")
            Vn=V.copy()
            Rn= politica.copy()

            #matriz = np.zeros((edos, edos))
            #costos = np.zeros(edos)
            estado = 0


            print("Mejoramiento de política")

            for estado in range(edos):
                estado = int(estado)
                optimo = signo * 2**15
                vector = np.zeros(edos)
                index = 0

                difmax=0

                print(f"Estado {estado}:")

                for decision in dicc[str(estado)]:
                    print(f"\tDecisión {decision}: ")
                    vector = dicc[str(estado)][decision]
                    Cij = cost[str(estado)][decision]
                    optimizar = np.dot(vector, V)
                    optimizar = alpha * optimizar
                    optimizar += Cij
                    print("\t\t",optimizar)
                    if self.min:
                        comp = optimizar < optimo
                    else:
                        comp = optimizar > optimo
                    if comp:
                        index = decision
                        politica[estado] = int(decision)
                        optimo = optimizar
                    #ACTUALIZAR V[ESTADO]=OPTIMIZAR
                print(f"\t\tEl optimo es {optimo} en la decisión {index}\n\n")
                V[int(int(estado))]=optimo
                if (V[int(int(estado))]-Vn[int(estado)])**2 > difmax**2:
                    difmax = V[int(estado)]-Vn[int(estado)]
            cont=0
            for i in V:
                text.insert(END, f"V{cont} = {round(i,4)}\n")
                print(f"V{cont} = {i}")
                cont+=1
            print("\nLa politica nueva es: ")
            print(politica)
            text.insert(END, f"Nuestra nueva política es: R{it}={politica} \n")

            tolerancia = (difmax)**2 <= epsilon**2
            comparacion = Rn == politica
            if tolerancia:
                text.insert(END, "Nos detenemos por haber logrado la tolerancia\n")
                print("Nos detenemos por haber logrado la tolerancia")
            if N<=it +1:
                text.insert(END, "Nos detenemos por haber llegado a las iteraciones\n")
                print("Nos detenemos por haber llegado a las iteraciones")
            if comparacion.all():
                text.insert(END, "Nos detenemos porque Vn-1 = Vn\n")
                print("Nos detenemos porque Vn-1 = Vn")

        text.insert(END, f"Terminamos con la política {politica}")
        text.tag_add("colorear", "end-3c linestart",  "end-1c lineend")
        text.tag_config("colorear", background = self.titulo_c)
        text.config(state=DISABLED)
    """def metodoDesc(self, vector, alpha):
        edos = self.edos
        dicc = self.dict_decisiones
        cost = self.dict_costos

        politica = np.zeros(edos)
        count=-1
        if not self.validateFloat(alpha):
            return False
        alpha = self.Float(alpha)

        for i in vector:
            count+=1
            string = i.get()
            if not self.validateInt(string):
                print(string, " no es número")
                return False

            try:
                a = dicc[string]
            except:
                print(string, " no es un estado")
                return False

            politica[count] = int(string)

        Rn=politica.copy()
        Rn[0]+= 1

        print("Empezamos a iterar")
        comparacion = Rn == politica
        it = 0
        while not comparacion.all():
            print(f"\tITERACION {it}\n")
            it += 1
            Rn=politica.copy()
            matriz = np.zeros((edos, edos))
            costos = np.zeros(edos)
            estado = 0
            for pol in politica:
                pol = int(pol)
                matriz[estado] = dicc[str(estado)][str(pol)]
                matriz[estado] = alpha * matriz[estado]
                costos[estado] = - cost[str(estado)][str(pol)]
                estado+=1

            for i in range(edos):
                matriz[i][i]-= 1

            print("Matriz a resolver")
            print(matriz)
            print("costos")
            print(costos)
            sol = np.linalg.solve(matriz, costos)
            print("Solución: ")
            print(sol) # vector de Vi, g(r)
            #gr=sol[-1]
            #sol[-1]=0
            #print(f"g(r) = {gr}")
            #cont=0
            #for i in sol:
            #    print(f"V{cont} = {i}")
            #    cont+=1
            #print("Costo esperado")
            #esperado = np.dot(sol, costos)
            #print(esperado)
            #if(signo * esperado > signo * optimo):
            #    optimo = esperado

            print("Mejoramiento de política")
            if self.min:
                signo = 1
            else:
                signo = -1
            for estado in range(edos):
                estado = int(estado)
                optimo = signo * 2**15
                vector = np.zeros(edos)
                index = 0
                print(f"Estado {estado}:")
                for decision in dicc[str(estado)]:
                    print(f"\tDecisión {decision}: ")
                    vector = dicc[str(estado)][decision]
                    Cij = cost[str(estado)][decision]
                    optimizar = np.dot(vector, sol)
                    optimizar += Cij
                    print("\t\t",optimizar)
                    if self.min:
                        comp = optimizar < optimo
                    else:
                        comp = optimizar > optimo
                    if comp:
                        index = decision
                        politica[estado] = int(decision)
                        optimo = optimizar
                print(f"\t\tEl optimo es {optimo} en la decisión {index}\n\n")

            print("\nLa politica nueva es: ")
            print(politica)
            comparacion = Rn == politica
"""

    def validateFloat(self, string):
        if "/" in string:
            aux = string.split('/')
            num = 1
            for s in aux:
                if not self.validateFloat(s):
                    return False
            return True
        ##REGRESAR DIVISION
        try:
            float(string)
        except:
            return False
        else:
            return True

    def Float(self, string):
        if "/" in string:
            aux = string.split('/')
            num = float(aux[0])
            for s in aux:
                    num= num/float(s)
            num = num * float(aux[0])
            return num
        ##REGRESAR DIVISION
        else:
            return float(string)

    def validateInt(self, string):
        try:
          int(string)
        except:
          return False
        else:
          return True
def only_numbers(char):
    if not char.isdigit():
        char=""
        return False
    return True


def main():
    app = AppProcesos()
    print("hola")

main()
