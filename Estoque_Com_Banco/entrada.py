from logging import root
from tkinter import *
from tkinter import ttk
import sqlite3


class Entrada():
    def limpa_tela_entrada(self):
        self.entry_id_entrada.delete(0, END)
        self.entry_material_entrada.delete(0, END)
        self.entry_quantidade_entrada.delete(0, END)
        self.entry_tipo_entrada.delete(0, END)
        self.entry_data_entrada.delete(0, END)

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
                            CREATE TABLE IF NOT EXISTS "entrada" (
                                "id_entrada"	INTEGER,
                                "quantidade_entrada"	INTEGER NOT NULL,
                                "data_entrada"	DATA NOT NULL,
                                "numero_os"	INTEGER,
                                PRIMARY KEY("id_entrada" AUTOINCREMENT)
                            )
                            """)

        self.conn.commit();
        print('Tabelas cadastro,estoque,entrada e saida Criados')
        self.desconecta_bd()

    def variaveis_entrada(self):
        self.id_entrada = self.entry_id_entrada.get()
        self.material_entrada = self.entry_material_entrada.get()
        self.quantidade_entrada = self.entry_quantidade_entrada.get()
        self.tipo_entrada = self.entry_tipo_entrada.get()
        self.data_entrada = self.entry_data_entrada.get()

    def add_material_entrada(self):
        self.variaveis_entrada()
        self.conecta_bd()

        self.cursor.execute("""
                            INSERT INTO entrada(quantidade_entrada) 
                            VALUES (?)""", (self.quantidade_entrada))

        self.conn.commit()

        id_entrada = self.cursor.execute("""
                                    SELECT id_entrada
                                    FROM entrada 
                                    WHERE numero_os = 21254""")

        id_material = self.cursor.execute("""
                                    SELECT id_cadastro
                                    FROM cadastro 
                                    WHERE numero_os = ?""" , self.material_entrada)

        self.cursor.execute("""
                            INSERT INTO tbr_material_entrada(id_cadastro,id_entrada)
                            VALUES (?,?)""", (id_material[0] , id_entrada[0]))

        self.cursor.execute("""
                            update estoque e 
                            set e.quantidade_estoque = e.quantidade_estoque + ?  
                            where e.id_cadastro = ? """, ( self.quantidade_entrada, id_material[0]))    


        self.conn.commit()                            

        self.desconecta_bd()
        self.select_lista_entrada()
        self.limpa_tela_entrada()

    def select_lista_entrada(self):
        self.lista_material_entrada.delete(*self.lista_material_entrada.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
                                 SELECT e.id_entrada,
                                        c.material_cadastro material_entrada,
                                        e.quantidade_entrada,
                                        c.tipo_cadastro tipo_entrada,
                                        e.data_entrada	
                                    FROM entrada e
                                    inner join tbr_material_entrada em on e.id_entrada = em.id_entrada
                                    inner join cadastro c on em.id_cadastro = c.id_cadastro  
                                    ORDER BY c.material_cadastro ASC""")
        for i in lista:
            self.lista_material_entrada.insert('', 'end', values=i)

        self.lista_total_entrada.delete(*self.lista_total_entrada.get_children())
        lista = self.cursor.execute("""
                                         SELECT e.id_entrada,
                                                c.material_cadastro material_entrada,
                                                e.quantidade_entrada
                                            FROM entrada e
                                            inner join tbr_material_entrada em on e.id_entrada = em.id_entrada
                                            inner join cadastro c on em.id_cadastro = c.id_cadastro  
                                            ORDER BY c.material_cadastro ASC""")
        for i in lista:
            self.lista_total_entrada.insert('', 'end', values=i)

        self.desconecta_bd()

    def OnDoubleClick_entrada(self, event):
        self.limpa_tela_entrada()

        self.lista_material_entrada.selection()
        for n in self.lista_material_entrada.selection():
            col1, col2, col3, col4, col5 = self.lista_material_entrada.item(n, 'values')

            self.entry_id_entrada.insert(END, col1)
            self.entry_material_entrada.insert(END, col2)
            self.entry_quantidade_entrada.insert(END, col3)
            self.entry_tipo_entrada.insert(END, col4)
            self.entry_data_entrada.insert(END, col5)

        self.lista_total_entrada.selection()
        for n in self.lista_total_entrada.selection():
            col1, col2, col3 = self.lista_total_entrada.item(n, 'values')

            self.entry_id_entrada.insert(END, col1)
            self.entry_material_entrada.insert(END, col2)
            self.entry_quantidade_entrada.insert(END, col3)

    def deleta_material_entrada(self):
        self.variaveis_entrada()
        self.conecta_bd()
        self.cursor.execute("""
                                DELETE FROM entrada WHERE id_entrada = ? """, (self.id_entrada,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela_entrada()
        self.select_lista_entrada()

    def alterar_entrada(self):
        self.variaveis_entrada()
        self.conecta_bd()

        self.cursor.execute("""
                            UPDATE entrada SET material_entrada=?, quantidade_entrada=?, tipo_entrada=?, data_entrada=? 
                            WHERE id_entrada = ? """, (
        self.material_entrada, self.quantidade_entrada, self.tipo_entrada, self.data_entrada, self.id_entrada))

        self.conn.commit()

        self.desconecta_bd()
        self.select_lista_entrada()
        self.limpa_tela_entrada()

    def entrada_entrada(self):
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

    def frames_entrada(self):
        self.frame_1_entrada = Frame(self.aba2, bd=4, highlightbackground='black', highlightthickness=2, bg='red')
        self.frame_1_entrada.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.15)

        self.frame_2_entrada = Frame(self.aba2, bd=4, highlightbackground='black', highlightthickness=2, bg='blue')
        self.frame_2_entrada.place(relx=0.01, rely=0.17, relwidth=0.98, relheight=0.42)

        self.frame_3_entrada = Frame(self.aba2, bd=4, highlightbackground='black', highlightthickness=2, bg='green')
        self.frame_3_entrada.place(relx=0.01, rely=0.60, relwidth=0.98, relheight=0.39)

    def widgts_entrada(self):
        # Titulo
        self.label_titulo_entrada = Label(self.frame_1_entrada, text='estoque - cordeirinho'.upper(), font='verdana 40 bold')
        self.label_titulo_entrada.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        # ID
        self.label_id_entrada = Label(self.frame_2_entrada, text='id'.upper(), font='verdana 10 bold')
        self.label_id_entrada.place(relx=0.07, rely=0.05, relwidth=0.04, relheight=0.08)

        self.entry_id_entrada = Entry(self.frame_2_entrada, font='verdana 10 bold')
        self.entry_id_entrada.place(relx=0.12, rely=0.05, relwidth=0.10, relheight=0.08)
        # Data
        self.label_data_entrada = Label(self.frame_2_entrada, text='data'.upper(), font='verdana 10 bold')
        self.label_data_entrada.place(relx=0.30, rely=0.05, relwidth=0.05, relheight=0.08)

        self.entry_data_entrada = Entry(self.frame_2_entrada, font='verdana 10 bold')
        self.entry_data_entrada.place(relx=0.36, rely=0.05, relwidth=0.12, relheight=0.08)
        # Material
        self.label_material_entrada = Label(self.frame_2_entrada, text='material'.upper(), font='verdana 10 bold')
        self.label_material_entrada.place(relx=0.01, rely=0.17, relwidth=0.10, relheight=0.08)

        self.entry_material_entrada = Entry(self.frame_2_entrada, font='verdana 10 bold')
        self.entry_material_entrada.place(relx=0.12, rely=0.17, relwidth=0.36, relheight=0.08)
        # Quantidade
        self.label_quantidade_entrada = Label(self.frame_2_entrada, text='quantidade'.upper(), font='verdana 8 bold')
        self.label_quantidade_entrada.place(relx=0.01, rely=0.29, relwidth=0.10, relheight=0.08)

        self.entry_quantidade_entrada = Entry(self.frame_2_entrada, font='verdana 10 bold')
        self.entry_quantidade_entrada.place(relx=0.12, rely=0.29, relwidth=0.10, relheight=0.08)

        # Tipo
        self.label_tipo_entrada = Label(self.frame_2_entrada, text='tipo'.upper(), font='verdana 10 bold')
        self.label_tipo_entrada.place(relx=0.30, rely=0.29, relwidth=0.05, relheight=0.08)

        self.entry_tipo_entrada = Entry(self.frame_2_entrada, font='verdana 10 bold')
        self.entry_tipo_entrada.place(relx=0.36, rely=0.29, relwidth=0.12, relheight=0.08)

        # Botao Cadastrar Material

        self.bt_Material_entrada = Button(self.frame_2_entrada, text='entrada de material'.upper(), command=self.add_material_entrada)
        self.bt_Material_entrada.place(relx=0.01, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Entrada_entrada = Button(self.frame_2_entrada, text='entrada no estoque'.upper(), command=self.entrada_entrada)
        self.bt_Entrada_entrada.place(relx=0.18, rely=0.70, relwidth=0.16, relheight=0.20)

        """self.bt_Saida_entrada = Button(self.frame_2, text='saida do estoque'.upper(), command=self.saida_estoque)
        self.bt_Saida_entrada.place(relx=0.35, rely=0.70, relwidth=0.16, relheight=0.20)"""

        self.bt_Inserir_Data_entrada = Button(self.frame_2_entrada, text='inserir data'.upper())
        self.bt_Inserir_Data_entrada.place(relx=0.49, rely=0.05, relwidth=0.10, relheight=0.12)

        self.bt_limpar_entrada = Button(self.frame_2_entrada, text='limpar tela'.upper(), command=self.limpa_tela_entrada)
        self.bt_limpar_entrada.place(relx=0.49, rely=0.20, relwidth=0.10, relheight=0.12)

        # Alterar
        self.bt_alterar_entrada = Button(self.frame_2_entrada, text='alterar'.upper(), command=self.alterar_entrada)
        self.bt_alterar_entrada.place(relx=0.01, rely=0.50, relwidth=0.16, relheight=0.10)

        self.bt_excluir_entrada = Button(self.frame_2_entrada, text='excluir'.upper(), command=self.deleta_material_entrada)
        self.bt_excluir_entrada.place(relx=0.01, rely=0.60, relwidth=0.16, relheight=0.10)

    def lista_frame3_entrada(self):
        self.lista_material_entrada = ttk.Treeview(self.frame_3_entrada, height=3,
                                                   columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.lista_material_entrada.heading('#0', text='')
        self.lista_material_entrada.heading('#1', text='id')
        self.lista_material_entrada.heading('#2', text='material')
        self.lista_material_entrada.heading('#3', text='quantidade')
        self.lista_material_entrada.heading('#4', text='tipo')
        self.lista_material_entrada.heading('#5', text='data')

        self.lista_material_entrada.column('#0', width=1)
        self.lista_material_entrada.column('#1', width=40)
        self.lista_material_entrada.column('#2', width=200)
        self.lista_material_entrada.column('#3', width=100)
        self.lista_material_entrada.column('#4', width=50)
        self.lista_material_entrada.column('#5', width=50)

        self.lista_material_entrada.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.95)

        # Barra de Rolagem
        self.scroollista_entrada = Scrollbar(self.frame_3_entrada, orient='vertical')
        self.lista_material_entrada.configure(yscroll=self.scroollista_entrada.set)
        self.scroollista_entrada.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_material_entrada.bind('<Double-1>', self.OnDoubleClick_entrada)

    def lista_frame2_entrada(self):
        self.lista_total_entrada = ttk.Treeview(self.frame_2_entrada, height=3, columns=('col1', 'col2', 'col3'))
        self.lista_total_entrada.heading('#0', text='')
        self.lista_total_entrada.heading('#1', text='Id/TOTAL')
        self.lista_total_entrada.heading('#2', text='Material')
        self.lista_total_entrada.heading('#3', text='Quantidade')

        self.lista_total_entrada.column('#0', width=0)
        self.lista_total_entrada.column('#1', width=50)
        self.lista_total_entrada.column('#2', width=100)
        self.lista_total_entrada.column('#3', width=40)

        self.lista_total_entrada.place(relx=0.60, rely=0.01, relwidth=0.40, relheight=0.95)

        # Barra de Rolagem
        self.scrool_total_entrada = Scrollbar(self.frame_2_entrada, orient='vertical')
        self.lista_total_entrada.configure(yscroll=self.scrool_total_entrada.set)
        self.scrool_total_entrada.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_total_entrada.bind('<Double-1>', self.OnDoubleClick_entrada)
