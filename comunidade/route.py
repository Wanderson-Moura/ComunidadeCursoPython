from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from flask import render_template, flash, redirect, request, url_for, abort
from comunidade import app, database, bcrypt
from comunidade.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


# lista_usuarios = ['Wanderson R', 'Adriana', 'Esdras', 'Rebeka', 'Wanderson T',]


@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login Bem sucedido no email: {form_login.email.data}', 'alert-success')
            # redireciona o cliente depois de logado para a página pesquisada
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for("home"))
            # até aqui a função de redirecionameto
        else:
            flash('falha no login, verifique o email ou a senha e tente novamente','alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # criar usuario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        # adicionar sessão
        database.session.add(usuario)
        # commit na sessão?
        database.session.commit()
        # mensagem para o cliente
        flash(f'Conta Criada com Sucesso no email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for("home"))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout bem sucedido', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='FotoPerfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['POST', 'GET'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(('Post Criado com Sucesso'))
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/FotoPerfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['POST', 'GET'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Edição bem sucedida', 'alert-success')
        return  redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='FotoPerfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)



@app.route('/post/<post_id>', methods=['POST', 'GET'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Editado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['POST', 'GET'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)



