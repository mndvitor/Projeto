# FORMULÁRIO DE LEADS PARA UMA AGENCIA DE MARKETING DIGITAL

# A AGÊNCIA "MARKETING DIGITAL" ESTÁ SEM UM SISTEMA ADEQUADO PARA
# GERENCIAR OS LEADS (POTENCIAIS CLIENTES) QUE RECEBE POR MEIO DE
# CAMPANHAS ONLINE. ATUALMENTE, OS LEADS SÃO ARMAZENADOS
# MANUALMENTE EM PLANILHAS, O QUE DIFICULTA O SEU GERENCIAMENTO E
# A RÁPIDA CONSULTA DOS DADOS. A AGÊNCIA PRECISA DE UM SISTEMA
# EFICIENTE PARA GERENCIAR E ACOMPANHAR OS LEADS.

# Solução proposta: Criar um formulário de cadastro de leads com campos
# como nome, e-mail, número de telefone e interesse no serviço. O sistema
# também permitirá visualizar, editar e excluir os leads, além de atualizar o
# status do lead (por exemplo, “Em andamento”, “Convertido”, “Perdido”).


import sqlite3 # banco de dados
import tkinter as tk # interface basica
from tkinter import messagebox # caixas de mensagens
from tkinter import ttk # interface grafica tb

def conectar():
    return sqlite3.connect('clientes.db')
# criar o banco (connect)

def criar_tabela():
    conn = conectar()
    c= conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes(
            CPF INTEGER NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            CNPJ INTEGER NOT NULL,
            Servico TEXT NOT NULL 
              
        )       
    ''')
    conn.commit()
    conn.close()
  


# CREATE
def inserir_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    cpf =  entry_cpf.get()
    cnpj =  entry_cnpj.get()
    servico =  entry_servico.get()


    if cpf and nome:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO clientes(CPF,nome, email,CNPJ,Servico) VALUES(?,?,?,?,?)', (cpf,nome, email,cnpj,servico))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!') 
        mostrar_cliente()
    else:
        messagebox.showerror('ERRO', 'ALGO DEU ERRADO!') 

# READ
def mostrar_cliente():
    for row in tree.get_children():   
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()    
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert("", "end", values=(cliente[0], cliente[1],cliente[2]))
    conn.close()    


# DELETE
def delete_cliente():
    dado_del = tree.selection()
    if dado_del:
       user_id = tree.item(dado_del)['values'][0]
       conn = conectar()
       c = conn.cursor()    
       c.execute('DELETE FROM clientes WHERE id = ? ',(user_id,))
       conn.commit()
       conn.close()
       messagebox.showinfo('', 'DADO DELETADO')
       mostrar_cliente()

    else:
       messagebox.showerror('', 'OCORREU UM ERRO')  

# UPDATE 
       
def editar():
     selecao = tree.selection()
     if selecao:
         user_id = tree.item(selecao)['values'][0]
         novo_nome = entry_nome.get()
         novo_email = entry_email.get()

         if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()    
            c.execute('UPDATE clientes SET nome = ? , email = ? WHERE id = ? ',(novo_nome,novo_email,user_id))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_cliente()

         else:
             messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')

     else:
            messagebox.showerror('','ALGO DEU ERRADO!')


# VAMOS COMPLETAR A INTERFACE GRÁFICA...
# 1
janela = tk.Tk()
janela.title('CRUD')

label_nome = tk.Label(janela, text='Cliente:')
label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_email = tk.Label(janela, text='E-mail:')
label_email.grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=10, pady=10)


label_cpf = tk.Label(janela, text='CPF:')
label_cpf.grid(row=2, column=0, padx=10, pady=10)
entry_cpf = tk.Entry(janela, text='CPF:')
entry_cpf.grid(row=2, column=1, padx=10, pady=10)

label_cnpj = tk.Label(janela, text='CNPJ:')
label_cnpj.grid(row=3, column=0, padx=10, pady=10)
entry_cnpj = tk.Entry(janela, text='CNPJ:')
entry_cnpj.grid(row=3, column=1, padx=10, pady=10)

label_servico = tk.Label(janela, text='Serviço Contratado:')
label_servico.grid(row=4, column=0, padx=10, pady=10)
entry_servico = tk.Entry(janela, text='Serviço Contratado:')
entry_servico.grid(row=4, column=1, padx=10, pady=10)


# botões

btn_salvar = tk.Button(janela, text='SALVAR',command=inserir_cliente)
btn_salvar.grid(row = 0, column=2, padx=10, pady=10  )

btn_deletar = tk.Button(janela, text='DELETAR',command=delete_cliente)
btn_deletar.grid(row = 1, column=2, padx=10, pady=10  )

btn_atualizar = tk.Button(janela, text='ATUALIZAR',command=editar)
btn_atualizar.grid(row = 2, column=2, padx=10, pady=10  )

# arvore
columns = ('CPF','NOME', 'EMAIL','CNPJ','Serviço Contratado')

tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=6, column=0,columnspan=2, padx=10, pady=10 )

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_cliente()


janela.mainloop()

