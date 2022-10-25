from logging import root
from tkinter import *
from tkinter import ttk
import sqlite3


class Estoque():
    def limpa_tela_estoque(self):
        self.entry_id_estoque.delete(0, END)
        self.entry_material_estoque.delete(0, END)
        self.entry_quantidade_estoque.delete(0, END)
        self.entry_tipo_estoque.delete(0, END)
        self.entry_data_estoque.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('cordeirinho2.bd')
        self.cursor = self.conn.cursor()

        print('Conectado ao Banco Cordeirinho')

    def desconecta_bd(self):
        self.conn.close()

    def monta_tabelas_estoque(self):
        self.conecta_bd()
        print('Banco Desconectado')

        # Criar Tabelas
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS estoque (
                                id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
                                material_estoque VARCHAR(100) NOT NULL,
                                quantidade_estoque INTEGER NOT NULL,
                                tipo_estoque VARCHAR(30) NOT NULL,
                                data_estoque DATA NOT NULL,
                                id_cadastro INTEGER,
                                id_entrada INTEGER,
                                id_saida INTEGER,
                                FOREIGN KEY (id_cadastro) REFERENCES cadastro (id_cadastro),
                                FOREIGN KEY (id_entrada) REFERENCES cadastro (id_entrada),
                                FOREIGN KEY (id_saida) REFERENCES cadastro (id_saida)
                                )
                            """)

        self.conn.commit();
        print('Tabelas cadastro,estoque,entrada e saida Criados')
        self.desconecta_bd()

    def variaveis_estoque(self):
        self.id_estoque = self.entry_id_estoque.get()
        self.material_estoque = self.entry_material_estoque.get()
        self.quantidade_estoque = self.entry_quantidade_estoque.get()
        self.tipo_estoque = self.entry_tipo_estoque.get()
        self.data_estoque = self.entry_data_estoque.get()

    def exibir_material_estoque(self):
        self.variaveis_estoque()
        self.conecta_bd()
        self.cursor.execute("""
                            INSERT INTO estoque(material_estoque,quantidade_estoque,tipo_estoque,data_estoque)
                            VALUES (?,?,?,?)""", (
                            self.material_estoque, self.quantidade_estoque, self.tipo_estoque, self.data_estoque))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista_estoque()
        self.limpa_tela_estoque()

    def select_lista_estoque(self):
        self.lista_material_estoque.delete(*self.lista_material_estoque.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
                                SELECT id_estoque, material_estoque,quantidade_estoque,tipo_estoque,data_estoque
                                FROM estoque
                                ORDER BY material_estoque ASC""")
        for i in lista:
            self.lista_material_estoque.insert('', 'end', values=i)

        self.lista_total_estoque.delete(*self.lista_total_estoque.get_children())
        lista = self.cursor.execute("""
                                        SELECT id_estoque,material_estoque,quantidade_estoque 
                                        FROM estoque
                                        ORDER BY material_estoque ASC""")
        for i in lista:
            self.lista_total_estoque.insert('', 'end', values=i)

        self.desconecta_bd()

    def OnDoubleClick_estoque(self, event):
        self.limpa_tela_estoque()

        self.lista_material_estoque.selection()
        for n in self.lista_material_estoque.selection():
            col1, col2, col3, col4, col5 = self.lista_material_estoque.item(n, 'values')

            self.entry_id_estoque.insert(END, col1)
            self.entry_material_estoque.insert(END, col2)
            self.entry_quantidade_estoque.insert(END, col3)
            self.entry_tipo_estoque.insert(END, col4)
            self.entry_data_estoque.insert(END, col5)

        self.lista_total_estoque.selection()
        for n in self.lista_total_estoque.selection():
            col1, col2, col3 = self.lista_total_estoque.item(n, 'values')

            self.entry_id_estoque.insert(END, col1)
            self.entry_material_estoque.insert(END, col2)
            self.entry_quantidade_estoque.insert(END, col3)

    def deleta_material_estoque(self):
        self.variaveis_estoque()
        self.conecta_bd()
        self.cursor.execute("""
                                DELETE FROM estoque WHERE id_estoque = ? """, (self.id_estoque,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela_estoque()
        self.select_lista_estoque()

    def alterar_estoque(self):
        self.variaveis_estoque()
        self.conecta_bd()

        self.cursor.execute("""
                            UPDATE estoque SET material_estoque=?, quantidade_estoque=?, tipo_estoque=?, data_estoque=? 
                            WHERE id_estoque = ? """, (
                            self.material_estoque, self.quantidade_estoque, self.tipo_estoque, self.data_estoque, self.id_estoque))

        self.conn.commit()

        self.desconecta_bd()
        self.select_lista_estoque()
        self.limpa_tela_estoque()

    def entrada_estoque_teste(self):
        self.variaveis_estoque()
        self.conecta_bd()
        self.lista_total_estoque.delete(*self.lista_total_estoque.get_children())

        self.entry_material_estoque.insert('end', '%')
        nome = self.entry_material_estoque.get()

        self.cursor.execute("""
                                SELECT quantidade_estoque,material_estoque
                                FROM estoque
                                WHERE material_estoque
                                LIKE '%s' ORDER BY material_estoque ASC""" % nome)
        busca = self.cursor.fetchall();
        print(busca)

        for i in busca:
            self.lista_total_estoque.insert('', END, values=i)
        self.limpa_tela_estoque()

        self.desconecta_bd()

    def saida_estoque(self):
        self.variaveis_estoque()
        self.conecta_bd()
        self.lista_total_estoque.delete(*self.lista_total_estoque.get_children())

        self.entry_material_estoque.insert('end', '%')
        nome = self.entry_material_estoque.get()
        self.cursor.execute("""
                                        SELECT SUM(quantidade_estoque),material_estoque
                                        FROM estoque
                                        WHERE material_estoque
                                        LIKE '%s' ORDER BY material_estoque ASC""" % nome)
        busca = self.cursor.fetchall();
        print(busca)  # completo

        total = busca[0];
        print(total)  # tupla

        lista_atual = list(total);
        print(lista_atual)  # lista

        lista2 = lista_atual[0];
        print(lista2)  # primeiro valor da lista

        lista3 = int(lista2) - int(self.entry_quantidade_estoque);
        print(lista3)  # redução do valor

        lista_atual.insert(1, lista3);
        print(lista_atual)

        for i in busca:
            self.lista_total_estoque.insert('', END, values=i)
        self.limpa_tela_estoque()

        self.desconecta_bd()

    def frames_estoque(self):
        self.frame_1_estoque = Frame(self.aba4, bd=4, highlightbackground='black', highlightthickness=2, bg='red')
        self.frame_1_estoque.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.15)

        self.frame_2_estoque = Frame(self.aba4, bd=4, highlightbackground='black', highlightthickness=2, bg='blue')
        self.frame_2_estoque.place(relx=0.01, rely=0.17, relwidth=0.98, relheight=0.42)

        self.frame_3_estoque = Frame(self.aba4, bd=4, highlightbackground='black', highlightthickness=2, bg='green')
        self.frame_3_estoque.place(relx=0.01, rely=0.60, relwidth=0.98, relheight=0.39)

    def widgts_estoque(self):
        # Titulo
        self.label_titulo_estoque = Label(self.frame_1_estoque, text='estoque - cordeirinho'.upper(), font='verdana 40 bold')
        self.label_titulo_estoque.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        # ID
        self.label_id_estoque = Label(self.frame_2_estoque, text='id'.upper(), font='verdana 10 bold')
        self.label_id_estoque.place(relx=0.07, rely=0.05, relwidth=0.04, relheight=0.08)

        self.entry_id_estoque = Entry(self.frame_2_estoque, font='verdana 10 bold')
        self.entry_id_estoque.place(relx=0.12, rely=0.05, relwidth=0.10, relheight=0.08)
        # Data
        self.label_data_estoque = Label(self.frame_2_estoque, text='data'.upper(), font='verdana 10 bold')
        self.label_data_estoque.place(relx=0.30, rely=0.05, relwidth=0.05, relheight=0.08)

        self.entry_data_estoque = Entry(self.frame_2_estoque, font='verdana 10 bold')
        self.entry_data_estoque.place(relx=0.36, rely=0.05, relwidth=0.12, relheight=0.08)
        # Material
        self.label_material_estoque = Label(self.frame_2_estoque, text='material'.upper(), font='verdana 10 bold')
        self.label_material_estoque.place(relx=0.01, rely=0.17, relwidth=0.10, relheight=0.08)

        self.entry_material_estoque = Entry(self.frame_2_estoque, font='verdana 10 bold')
        self.entry_material_estoque.place(relx=0.12, rely=0.17, relwidth=0.36, relheight=0.08)
        # Quantidade
        self.label_quantidade_estoque = Label(self.frame_2_estoque, text='quantidade'.upper(), font='verdana 8 bold')
        self.label_quantidade_estoque.place(relx=0.01, rely=0.29, relwidth=0.10, relheight=0.08)

        self.entry_quantidade_estoque = Entry(self.frame_2_estoque, font='verdana 10 bold')
        self.entry_quantidade_estoque.place(relx=0.12, rely=0.29, relwidth=0.10, relheight=0.08)

        # Tipo
        self.label_tipo_estoque = Label(self.frame_2_estoque, text='tipo'.upper(), font='verdana 10 bold')
        self.label_tipo_estoque.place(relx=0.30, rely=0.29, relwidth=0.05, relheight=0.08)

        self.entry_tipo_estoque = Entry(self.frame_2_estoque, font='verdana 10 bold')
        self.entry_tipo_estoque.place(relx=0.36, rely=0.29, relwidth=0.12, relheight=0.08)

        # Botao Cadastrar Material

        self.bt_Material_estoque = Button(self.frame_2_estoque, text='exibir  material'.upper(), command=self.exibir_material_estoque)
        self.bt_Material_estoque.place(relx=0.01, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Entrada_entrada = Button(self.frame_2_estoque, text='entrada no estoque teste'.upper(), command=self.entrada_estoque_teste)
        self.bt_Entrada_entrada.place(relx=0.18, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Saida_estoque = Button(self.frame_2_estoque, text='saida do estoque'.upper(), command=self.saida_estoque)
        self.bt_Saida_estoque.place(relx=0.35, rely=0.70, relwidth=0.16, relheight=0.20)

        self.bt_Inserir_Data_estoque = Button(self.frame_2_estoque, text='inserir data'.upper())
        self.bt_Inserir_Data_estoque.place(relx=0.49, rely=0.05, relwidth=0.10, relheight=0.12)

        self.bt_limpar_estoque = Button(self.frame_2_estoque, text='limpar tela'.upper(), command=self.limpa_tela_estoque)
        self.bt_limpar_estoque.place(relx=0.49, rely=0.20, relwidth=0.10, relheight=0.12)

        # Alterar
        self.bt_alterar_estoque = Button(self.frame_2_estoque, text='alterar'.upper(), command=self.alterar_estoque)
        self.bt_alterar_estoque.place(relx=0.01, rely=0.50, relwidth=0.16, relheight=0.10)

        self.bt_excluir_estoque = Button(self.frame_2_estoque, text='excluir'.upper(), command=self.deleta_material_estoque)
        self.bt_excluir_estoque.place(relx=0.01, rely=0.60, relwidth=0.16, relheight=0.10)

    def lista_frame3_estoque(self):
        self.lista_material_estoque = ttk.Treeview(self.frame_3_estoque, height=3,
                                                   columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.lista_material_estoque.heading('#0', text='')
        self.lista_material_estoque.heading('#1', text='id')
        self.lista_material_estoque.heading('#2', text='material')
        self.lista_material_estoque.heading('#3', text='quantidade')
        self.lista_material_estoque.heading('#4', text='tipo')
        self.lista_material_estoque.heading('#5', text='data')

        self.lista_material_estoque.column('#0', width=1)
        self.lista_material_estoque.column('#1', width=40)
        self.lista_material_estoque.column('#2', width=200)
        self.lista_material_estoque.column('#3', width=100)
        self.lista_material_estoque.column('#4', width=50)
        self.lista_material_estoque.column('#5', width=50)

        self.lista_material_estoque.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.95)

        # Barra de Rolagem
        self.scroollista_estoque = Scrollbar(self.frame_3_estoque, orient='vertical')
        self.lista_material_estoque.configure(yscroll=self.scroollista_estoque.set)
        self.scroollista_estoque.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_material_estoque.bind('<Double-1>', self.OnDoubleClick_estoque)

    def lista_frame2_estoque(self):
        self.lista_total_estoque = ttk.Treeview(self.frame_2_estoque, height=3, columns=('col1', 'col2', 'col3'))
        self.lista_total_estoque.heading('#0', text='')
        self.lista_total_estoque.heading('#1', text='Id/TOTAL')
        self.lista_total_estoque.heading('#2', text='Material')
        self.lista_total_estoque.heading('#3', text='Quantidade')

        self.lista_total_estoque.column('#0', width=0)
        self.lista_total_estoque.column('#1', width=50)
        self.lista_total_estoque.column('#2', width=100)
        self.lista_total_estoque.column('#3', width=40)

        self.lista_total_estoque.place(relx=0.60, rely=0.01, relwidth=0.40, relheight=0.95)

        # Barra de Rolagem
        self.scrool_total_estoque = Scrollbar(self.frame_2_estoque, orient='vertical')
        self.lista_total_estoque.configure(yscroll=self.scrool_total_estoque.set)
        self.scrool_total_estoque.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.95)

        self.lista_total_estoque.bind('<Double-1>', self.OnDoubleClick_estoque)
