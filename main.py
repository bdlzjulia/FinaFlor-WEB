from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)
BANCO = 'produtos.bd'


def criar_banco():
    bd = sqlite3.connect(BANCO)
    bd.execute(
        '''CREATE TABLE IF NOT EXISTS floricultura(
            codigo INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            preco TEXT NOT NULL,
            categoria TEXT NOT NULL)'''
    )
    bd.close()

def bd():
    if 'bd' not in g:
        g.bd = sqlite3.connect(BANCO)
    return g.bd

@app.teardown_appcontext
def fechar_conexao(exeption):
    if 'bd' in g:
        g.bd.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/lista')
def lista():
    produtos = bd().execute('''SELECT * FROM floricultura''').fetchall()
    return render_template("lista2.html", lista_produtos=produtos)

@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        codigo = request.form['codigo']
        titulo = request.form['titulo']
        preco = request.form['preco']
        categoria = request.form['categoria']
        bd().execute('''INSERT INTO floricultura(
                    codigo, titulo, preco, categoria)
                    values(?,?,?,?)''', [codigo, titulo, preco, categoria])
        bd().commit()
        return redirect(url_for('lista'))

    return render_template('cadastro2.html')


if __name__ == "__main__":
    criar_banco()
    app.run(port=80, debug=True)