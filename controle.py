from PyQt6 import uic,QtWidgets # É necessário importa a biblioteca "uic" para conseguirmos fazer a comunicação com o layout
from tkinter import messagebox
import mysql.connector
from reportlab.pdfgen import canvas


banco = mysql.connector.connect(
   host ='localhost',
   user ='root',
   password = 'carvalho13',
   database = 'cadastro_produtos',
   auth_plugin = "mysql_native_password"
)


def excluir_dados():    
    linha_tabela = segunda_t.tableWidget.currentRow() # Seleciona a linha que deseja excluir

    #verificar se é uma linha valida
    if linha_tabela == -1:
        return # Caso não tenha uma linha selecionada, não faz nada

    segunda_t.tableWidget.removeRow(linha_tabela) # exclui a linha selecionada na variavel acima

    cursor = banco.cursor()
    comando_SQL = 'SELECT id FROM produtos'
    cursor.execute(comando_SQL) # pega todos os ID da tabela "produtos"
    dados_lidos = cursor.fetchall()

    if linha_tabela< len(dados_lidos):
        valor_des = dados_lidos[linha_tabela][0]
        print(valor_des)
    

    

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() # Salvar dados recuperados do banco
    y = 0
    pdf = canvas.Canvas('cadastro_produtos.pdf')
    pdf.setFont('Times-Bold', 25)
    pdf.drawString(200,800, 'Produtos Cadastrados:')
    pdf.setFont('Times-Bold',12)

    pdf.drawString(10,750, 'ID')
    pdf.drawString(110,750, 'CÓDIGO')
    pdf.drawString(210,750, 'PRODUTO')
    pdf.drawString(310,750, 'PREÇO')
    pdf.drawString(410,750, 'CATEGORIA')

    for i in range(0, len(dados_lidos)):
        y = y + 50 # A variavel Y serve pra ir escrevendo os dados e ir pulando uma linha
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    messagebox.showinfo('Sucesso', 'PDF gerado com sucesso!')



def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria =''
  

    if formulario.radioButton.isChecked():
        print('Categoria Informática selecionada')
        categoria = 'Informatica'
    elif formulario.radioButton_2.isChecked():
        print('Categoria Alimentos selecionado')
        categoria = 'Alimentos'
    elif formulario.radioButton_3.isChecked():
        print('Categoria Eletrônicos selecionado')
        categoria = 'Eletrônicos'
    else:
        messagebox.showerror('Erro', 'Selecione uma categoria')


    print('Código:', linha1)
    print('Descrição:', linha2)
    print('Preço:', linha3)


    # Enviar informações ao banco de dados
    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s,%s,%s,%s)'
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText('') # Limpar o campo após gravar as informações no banco
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')

    
def chamar_segunda_tela():
   segunda_t.show()


   


# Mostrar tabelas com os dados cadastrados
   cursor = banco.cursor()
   comando_SQL = 'SELECT * FROM produtos' # Comando para visualizar todos os dados criados no banco
   cursor.execute(comando_SQL)
   dados_lidos = cursor.fetchall() # Pega todos os dados da variavel 'comando_SQL' e salva nessa variavel
   segunda_t.tableWidget.setRowCount(len(dados_lidos)) #setRowCount determina quantas linhas terá a tabela
   segunda_t.tableWidget.setColumnCount(5) #setColumnCount determinar o número de colunas (nesse caso o numerod e colunas é fixo)


   for i in range(0, len(dados_lidos)): # Criamos um for que percorrer 0 até o tamanho total de linhas
    for j in range(0, 5):
        segunda_t.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
formulario=uic.loadUi('formulario.ui') # Faz a comunicação com o layout do formulário
segunda_t=uic.loadUi('listar_dados.ui')
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chamar_segunda_tela)
segunda_t.pushButton_2.clicked.connect(gerar_pdf)
segunda_t.pushButton_3.clicked.connect(excluir_dados)



formulario.show()
app.exec()



