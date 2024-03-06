from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmção de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_criar_conta = SubmitField('Criar Conta')

    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Insira outro e-mail ou faça login')

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados')
    botao_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto do Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power Bi Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadora')
    curso_sql = BooleanField('SQL Impressionador')
    curso_html = BooleanField('HTML Impressionador')
    curso_css = BooleanField('CSS Impressionador')
    curso_javascript = BooleanField('JavaScript Impressionador')

    botao_editarperfil = SubmitField('Editar')


    def validate_email(self,email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado. Insira outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')






