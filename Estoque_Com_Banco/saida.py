from logging import root
from tkinter import *
from tkinter import ttk
import sqlite3


class Saida():
    def limpa_tela_saida(self):
        self.entry_id_saida.delete(0, END)
        self.entry_material_saida.delete(0, END)
        self.entry_quantidade_saida.delete(0, END)
        self.entry_tipo_saida.delete(0, END)
        self.entry_data_saida.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('cordeirinho2.bd')
        self.cursor = self.conn.cursor()

        print('Conectado ao Banco Cordeirinho')

    def desconecta_bd(self):
        self.conn.close()

    def monta_tabelas(self):
        self.conecta_bd()
        print('Banco Desconectado')

        # Criar Tabelas
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS saida (
                                id_saida INTEGER PRIMARY KEY,
                                material_saida VARCHAR(100) NOT NULL,
                                quantidade_saida INTEGER NOT NULL,
                                tipo_saida VARCHAR(30) NOT NULL,
                                data_saida DATA NOT NULL,
                                )
                            """)

        self.conn.commit();
        print('Tabelas cadastro,estoque,entrada e saida Criados')
        self.desconecta_bd()

    def variaveis_saida(self):
        self.id_saida = self.entry_id_saida.get()
        self.material_saida = self.entry_material_saida.get()
        self.quantidade_saida = self.entry_quantidade_saida.get()
        self.tipo_saida = self.entry_tipo_saida.get()
        self.data_saida = self.entry_data_saida.get()

    def off_material_saida(self):
        self.variaveis_saida()
        self.conecta_bd()
        self.cursor.execute("""
                            INSERT INTO saida(material_saida,quantidade_saida,tipo_saida,data_saida)
                            VALUES (?,?,?,?)""", (
                            self.material_saida, self.quantidade_saida, self.tipo_saida, self.data_saida))

        self.conn.commit()
        self.desconecta_bd()
        self.select_lista_saida()
        self.limpa_tela_saida()

    def select_lista_saida(self):
        self.lista_material_saida.delete(*self.lista_material_saida.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
                                SELECT id_saida, material_saida,quantidade_saida,tipo_saida,data_saida
                                FROM saida
                                ORDER BY material_saida ASC""")
        for i in lista:
            self.lista_material_saida.insert('', 'end', values=i)

        self.lista_total_saida.delete(*self.lista_total_saida.get_children())
        lista = self.cursor.execute("""
                                        SELECT id_saida,material_saida,quantidade_saida 
                                        FROM saida
                                        ORDER BY material_saida ASC""")
        for i in lista:
            self.lista_total_saida.insert('', 'end', values=i)

        self.desconecta_bd()

    def OnDoubleClick_saida(self, event):
        self.limpa_tela_saida()

        self.lista_material_saida.selection()
        for n in self.lista_material_saida.selection():
            col1, col2, col3, col4, col5 = self.lista_material_saida.item(n, 'values')

            self.entry_id_saida.insert(END, col1)
            self.entry_material_saida.insert(END, col2)
            self.entry_quantidade_saida.insert(END, col3)
            self.entry_tipo_saida.insert(END, col4)
            self.entry_data_saida.insert(END, col5)

        self.lista_total_saida.selection()
        for n in self.lista_total_saida.selection():
            col1, col2, col3 = self.lista_total_saida.item(n, 'values')

            self.entry_id_saida.insert(END, col1)
            self.entry_material_saida.insert(END, col2)
            self.entry_quantidade_saida.insert(END, col3)

    def deleta_material_saida(self):
        self.variaveis_saida()
        self.conecta_bd()
        self.cursor.execute("""
                                DELETE FROM saida WHERE id_saida = ? """, (self.id_saida,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela_saida()
        self.select_lista_saida()

    def alterar_saida(self):
        self.variaveis_saida()
        self.conecta_bd()

        self.cursor.execute("""
                            UPDATE saida SET material_saida=?, quantidade_saida=?, tipo_saida=?, data_saida=? 
                            WHERE id_saida = ? """, (
                            self.material_saida, self.quantidade_saida, self.tipo_saida, self.data_saida, self.id_saida))

        self.conn.commit()

        self.desconecta_bd()
        self.select_lista_saida()
        self.limpa_tela_saida()

    def entrada_estoque(self):
        self.variaveis_entrada()
        self.conecta_bd()
        self.lista_total_entrada.delete(*self.lista_total_entrada.get_children())

        self.entry_material_entrada.insert('end', '%')
        nome = self.entry_material_entrada.get()

        self.cursor.execute("""
                                SELECT SUM(quantidade_entrada),material_entrada
                                FROM entrada
                                WHERE material_entrada
                                LIKE '%s' ORDER BY material_entrada ASC""" % nome)
        busca = self.cursor.fetchall();
        print(busca)

        for i in busca:
            self.lista_total_entrada.insert('', END, values=i)
        self.limpa_tela_entrada()

        self.desconecta_bd()


    def frames_saida(self):
        self.frame_1_saida = Frame(self.aba3, bd=4, highlightbackground='black', highlightthickness=2, bg='red')
        self.frame_1_saida.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.15)

        self.frame_2_saida = Frame(self.aba3, bd=4, highlightbackground='black', highlightthickness=2, bg='blue')
        self.frame_2_saida.place(relx=0.01, rely=0.17, relwidth=0.98, relheight=0.42)

        self.frame_3_saida = Frame(self.aba3, bd=4, highlightbackground='black', highlightthickness=2, bg='green')
        self.frame_3_saida.place(relx=0.01, rely=0.60, relwidth=0.98, relheight=0.39)

    def widgts_saida(self):
        # Titulo
        self.label_titulo_saida = Label(self.frame_1_saida, text='estoque - cordeirinho'.upper(), font='verdana 40 bold')
        self.label_titulo_saida.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        # ID
        self.label_id_saida = Label(self.frame_2_saida, text='id'.upper(), font='verdana 10 bold')
        self.label_id_saida.place(relx=0.07, rely=0.05, relwidth=0.04, relheight=0.08)

        self.entry_id_saida = Entry(self.frame_2_saida, font='verdana 10 bold')
        self.entry_id_saida.place(relx=0.12, rely=0.05, relwidth=0.10, relheight=0.08)
        # Data
        self.label_data_saida = Label(self.frame_2_saida, text='data'.upper(), font='verdana 10 bold')
        self.label_data_saida.place(relx=0.30, rely=0.05, relwidth=0.05, relheight=0.08)

        self.entry_data_saida = Entry(self.frame_2_saida, font='verdana 10 bold')
        self.entry_data_saida.place(relx=0.36, rely=0.05, relwidth=0.12, relheight=0.08)
        # Material
        self.label_material_saida = Label(self.frame_2_saida, text='material'.upper(), font='verdana 10 bold')
        self.label_material_saida.place(relx=0.01, rely=0.17, relwidth=0.10, relheight=0.08)

        self.entry_material_saida = Entry(self.frame_2_saida, font='verdana 10 bold')
        self.entry_material_saida.place(relx=0.12, rely=0.17, relwidth=0.36, relheight=0.08)
        # Quantidade
        self.label_quantidade_saida = Label(self.frame_2_saida, text='quantidade'.upper(), font='verdana 8 bold')
        self.label_quantidade_saida.place(relx=0.01, rely=0.29, relwidth=0.10, relheight=0.08)

        self.entry_quantidade_saida = Entry(self.frame_2_saida, font='verdana 10 bold')
        self.entry_quantidade_saida.place(relx=0.12, rely=0.29, relwidth=0.10, relheight=0.08)

        # Tipo
        self.label_tipo_saida = Label(self.frame_2_saida, text='tipo'.upper(), font='verdana 10 bold')
        self.label_tipo_saida.place(relx=0.30, rely=0.29, relwidth=0.05, relheight=0.08)

        self.entry_tipo_saida = Entry(self.frame_2_saida, font='verdana 10 bold')
        self.entry_tipo_saida.place(relx=0.36, rely=0.29, relwidth=0.12, relheight=0.08)

        # Botao Cadastrar Material

        self.bt_Material_saida = Button(self.frame_2_saida, text='saida de material'.upper(), command=self.off_material_saida)
        self.bt_Material_saida.place(relx=0.01, rely=0.70, relwidth=0.16, relheight=0.20)

        """self.bt_Entrada_entrada = Button(self.frame_2_entrada, text='entrada no estoque'.upper(), command=self.entrada_estoque)
        self.bt_Entrada_entrada.place(relx=0.18, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Saida_entrada = Button(self.frame_2, text='saida do estoque'.upper(), command=self.saida_estoque)
        self.bt_Saida_entrada.place(relx=0.35, rely=0.70, relwidth=0.16, relheight=0.20)"""

        self.bt_Inserir_Data_saida = Button(self.frame_2_saida, text='inserir data'.upper())
        self.bt_Inserir_Data_saida.place(relx=0.49, rely=0.05, relwidth=0.10, relheight=0.12)

        self.bt_limpar_saida = Button(self.frame_2_saida, text='limpar tela'.upper(), command=self.limpa_tela_saida)
        self.bt_limpar_saida.place(relx=0.49, rely=0.20, relwidth=0.10, relheight=0.12)

        # Alterar
        self.bt_alterar_saida = Button(self.frame_2_saida, text='alterar'.upper(), command=self.alterar_saida)
        self.bt_alterar_saida.place(relx=0.01, rely=0.50, relwidth=0.16, relheight=0.10)

        self.bt_excluir_entrada = Button(self.frame_2_saida, text='excluir'.upper(), command=self.deleta_material_saida)
        self.bt_excluir_entrada.place(relx=0.01, rely=0.60, relwidth=0.16, relheight=0.10)

    def lista_frame3_saida(self):
        self.lista_material_saida = ttk.Treeview(self.frame_3_saida, height=3,
                                                   columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.lista_material_saida.heading('#0', text='')
        self.lista_material_saida.heading('#1', text='id')
        self.lista_material_saida.heading('#2', text='material')
        self.lista_material_saida.heading('#3', text='quantidade')
        self.lista_material_saida.heading('#4', text='tipo')
        self.lista_material_saida.heading('#5', text='data')

        self.lista_material_saida.column('#0', width=1)
        self.lista_material_saida.column('#1', width=40)
        self.lista_material_saida.column('#2', width=200)
        self.lista_material_saida.column('#3', width=100)
        self.lista_material_saida.column('#4', width=50)
        self.lista_material_saida.column('#5', width=50)

        self.lista_material_saida.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.95)

        # Barra de Rolagem
        self.scroollista_saida = Scrollbar(self.frame_3_saida, orient='vertical')
        self.lista_material_saida.configure(yscroll=self.scroollista_saida.set)
        self.scroollista_saida.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_material_saida.bind('<Double-1>', self.OnDoubleClick_saida)

    def lista_frame2_saida(self):
        self.lista_total_saida = ttk.Treeview(self.frame_2_saida, height=3, columns=('col1', 'col2', 'col3'))
        self.lista_total_saida.heading('#0', text='')
        self.lista_total_saida.heading('#1', text='Id/TOTAL')
        self.lista_total_saida.heading('#2', text='Material')
        self.lista_total_saida.heading('#3', text='Quantidade')

        self.lista_total_saida.column('#0', width=0)
        self.lista_total_saida.column('#1', width=50)
        self.lista_total_saida.column('#2', width=100)
        self.lista_total_saida.column('#3', width=40)

        self.lista_total_saida.place(relx=0.60, rely=0.01, relwidth=0.40, relheight=0.95)

        # Barra de Rolagem
        self.scrool_total_saida = Scrollbar(self.frame_2_saida, orient='vertical')
        self.lista_total_saida.configure(yscroll=self.scrool_total_saida.set)
        self.scrool_total_saida.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_total_saida.bind('<Double-1>', self.OnDoubleClick_saida)
