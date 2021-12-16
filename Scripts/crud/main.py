from typing import Text
from flask import render_template, request, redirect, url_for
from flask.helpers import total_seconds
from flask_login import login_user, logout_user
from datetime import date
import datetime
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.operators import ilike_op
from app import app, db
from app.models import User , Servicos, Clientes, ServicosAgendados, StatusAgendamento
from random import randint
from sqlalchemy.sql import functions
import os

if __name__== 'main':
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        usuario= request.form.get("usuario")
        senha = request.form.get("senha")

        if nome and telefone and usuario and senha:
            user = User(nome,telefone,usuario,senha)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        pwd = request.form['senha']

        user = User.query.filter_by(usuario=usuario).first()

        if not user or not user.verify_password(pwd):
            return redirect(url_for('login'))        

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/", methods=['GET', 'POST'])
def home():
    ultimaAtualizacao=datetime.datetime.now().strftime('%d-%m-%Y as %H:%M:%S')
    queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == date.today()).filter(ServicosAgendados.status == 1).first()
    
    '''Quantidade de serviços por mês'''
    JanSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-01-01','2021-01-31')).count()
    FevSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-02-01','2021-02-29')).count()
    MarSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-03-01','2021-03-31')).count()
    AbrSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-04-01','2021-04-30')).count()
    MaiSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-05-01','2021-05-31')).count()
    JunSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-06-01','2021-06-30')).count()
    JulSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-07-01','2021-07-31')).count()
    AgoSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-08-01','2021-08-31')).count()
    SetSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-09-01','2021-09-30')).count()
    OutSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-10-01','2021-10-31')).count()
    NovSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-11-01','2021-11-30')).count()
    DezSEARCH= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between('2021-12-01','2021-12-31')).count()
    
    '''Numero de vezes que um serviço foi requisitado'''
    CabeloSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==1).filter(ServicosAgendados.status==1).count()
    BarbaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==2).filter(ServicosAgendados.status==1).count()
    TinturaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==3).filter(ServicosAgendados.status==1).count()
    LuzesSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==5).filter(ServicosAgendados.status==1).count()
    SombrancelhaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==8).filter(ServicosAgendados.status==1).count()
    PenteadoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==10).filter(ServicosAgendados.status==1).count()

    '''Numero de vezes que cada servico foi cancelado'''
    CabeloCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==1).filter(ServicosAgendados.status==2).count()
    BarbaCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==2).filter(ServicosAgendados.status==2).count()
    TinturaCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==3).filter(ServicosAgendados.status==1).count()
    LuzesCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==5).filter(ServicosAgendados.status==1).count()
    SombrancelhaCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==8).filter(ServicosAgendados.status==1).count()
    PenteadoCANCELADOSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==10).filter(ServicosAgendados.status==1).count()

    total = queryTotal[2]
    if total == None:
        total = 0
    
    servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=date.today())
    return render_template('home.html', servicosagendados=servicosagendados,ultimaAtualizacao=ultimaAtualizacao, total=total,
                                                                                                                            JanSEARCH =JanSEARCH,
                                                                                                                            FevSEARCH =FevSEARCH,
                                                                                                                            MarSEARCH =MarSEARCH,
                                                                                                                            AbrSEARCH =AbrSEARCH,
                                                                                                                            MaiSEARCH =MaiSEARCH,
                                                                                                                            JunSEARCH =JunSEARCH,
                                                                                                                            JulSEARCH =JulSEARCH,
                                                                                                                            AgoSEARCH =AgoSEARCH,
                                                                                                                            SetSEARCH =SetSEARCH,
                                                                                                                            OutSEARCH =OutSEARCH,
                                                                                                                            NovSEARCH =NovSEARCH,
                                                                                                                            DezSEARCH =DezSEARCH,

                                                                                                                            CabeloSearch =CabeloSearch,
                                                                                                                            BarbaSearch = BarbaSearch,
                                                                                                                            TinturaSearch =TinturaSearch,
                                                                                                                            LuzesSearch =LuzesSearch,
                                                                                                                            SombrancelhaSearch =SombrancelhaSearch,
                                                                                                                            PenteadoSearch =PenteadoSearch,

                                                                                                                            CabeloCANCELADOSearch =CabeloCANCELADOSearch,
                                                                                                                            BarbaCANCELADOSearch =BarbaCANCELADOSearch,
                                                                                                                            TinturaCANCELADOSearch =TinturaCANCELADOSearch,
                                                                                                                            LuzesCANCELADOSearch =LuzesCANCELADOSearch,
                                                                                                                            SombrancelhaCANCELADOSearch =SombrancelhaCANCELADOSearch,
                                                                                                                            PenteadoCANCELADOSearch =PenteadoCANCELADOSearch
                                                                                                                            )


@app.route("/lista")
def lista():
    pessoas = User.query.all()
    return render_template("lista.html",pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = User.query.filter_by(id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = User.query.all()
    return render_template("lista.html",pessoas=pessoas)


@app.route("/clientes", methods=['GET', 'POST'])
def clientes():
    erro= ""
    if request.method == "POST":
        nome = request.form.get("nome_cliente")
        cpf = request.form.get("cpf_cliente")
        telefone = request.form.get("telefone_cliente")

        if nome and cpf and telefone:
            valido = cpf_validate(cpf)
            if valido == True:
                user = Clientes(nome,cpf,telefone)
                db.session.add(user)
                db.session.commit()
            else:
                erro = "CPF Inválido"
            
    clientes = Clientes.query.all()
    return render_template("clientes.html",clientes=clientes, erro=erro)

@app.route("/pesquisaCliente", methods=['GET', 'POST'])
def pesquisaCliente():
    clientes = ""
    if request.method == "POST":
        nomePesquisa = request.form.get("nomeClientePesquisa")
        tipoPesquida = request.form.get("comboboxCliente")
        if nomePesquisa:
            if tipoPesquida == "2":
                clientes= db.session.query(Clientes).filter(Clientes.nome.like("%"+nomePesquisa+"%")).all()
            elif tipoPesquida == "1":
                clientes= Clientes.query.filter_by(nome=nomePesquisa).all()
            else:
                clientes = Clientes.query.all()
        else:
            clientes = Clientes.query.all()
        
    return render_template("clientes.html",clientes=clientes)


@app.route("/excluircliente/<int:id>")
def excluircliente(id):
    cliente = Clientes.query.filter_by(id_cliente=id).first()

    db.session.delete(cliente)
    db.session.commit()

    clientes = Clientes.query.all()
    return render_template("clientes.html",clientes=clientes)


@app.route("/servicos", methods=['GET', 'POST'])
def servicos():
    if request.method == "POST":
        nome = request.form.get("servico")
        preco = request.form.get("preco")

        if nome and preco:
            user = Servicos(nome,preco)
            db.session.add(user)
            db.session.commit()
            
    servicos = Servicos.query.all()
    return render_template("servicos.html",servicos=servicos)


@app.route("/excluirservico/<int:id>")
def excluirservico(id):
    servico = Servicos.query.filter_by(id_servicos=id).first()

    db.session.delete(servico)
    db.session.commit()

    servicos = Servicos.query.all()
    return render_template("servicos.html",servicos=servicos)


@app.route("/financeiro", methods=['GET', 'POST'])
def financeiro():
    total=0
    pesquisasDatas=""
    if request.method == 'POST':
        data = request.form.get("dataPesquisa")
        data2 = request.form.get("dataPesquisa2")
        tipoPesquida = request.form.get("comboboxTipoPesquisaFinanceiro")
        if data and tipoPesquida == "1":
            pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == data).filter(ServicosAgendados.status == 1).all()
            queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == data).filter(ServicosAgendados.status == 1).first()
            total = queryTotal[2]
            return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)
        elif tipoPesquida == "2":
            if data and data2 :
                pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento.between(data,data2)).filter(ServicosAgendados.status == 1).all()
                queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento.between(data,data2)).filter(ServicosAgendados.status == 1).first()
                total = queryTotal[2]
                return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)
        else:
            pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.status == 1).all()
            queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.status == 1).first()
            total = queryTotal[2]
            return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)

    return render_template('financeiro.html',pesquisasDatas=pesquisasDatas, total=total)


@app.route("/agendamento", methods=['GET', 'POST'])
def agendamento():
    if request.method == "POST":
        fk_id_servico = request.form.get("servicoagendado")
        desc = Servicos.query.filter_by(id_servicos=fk_id_servico).first()
        desc_servico = "NOME: "+desc.nome +", PREÇO: R$ "+str(desc.preco)+",00"
        fk_id_cliente = request.form.get("nome-cliente")
        cliente_selecionado = Clientes.query.filter_by(id_cliente=fk_id_cliente).first()
        nm_cliente = cliente_selecionado.nome
        data_agendamento = request.form.get("data")
        horario_agendado = request.form.get("horario")
        
        
        
        if fk_id_servico and desc_servico and fk_id_cliente and nm_cliente and horario_agendado and data_agendamento:
            status = None
            desc_status = None
            user = ServicosAgendados(fk_id_servico, desc_servico, fk_id_cliente, nm_cliente, horario_agendado, data_agendamento,status,desc_status)
            db.session.add(user)
            db.session.commit()

    clientes = Clientes.query.all()
    servicos = Servicos.query.all()
    return render_template('agendamento.html', servicos=servicos, clientes=clientes)


@app.route("/agenda", methods=['GET', 'POST'])
def agenda():
    servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=date.today())
    servicosconcluidos = ServicosAgendados.query.filter_by(status=1,data_agendamento=date.today())
    servicoscancelados = ServicosAgendados.query.filter_by(status=2,data_agendamento=date.today())
    if request.method == "POST":
        data = request.form.get("dataPesquisa")
        if data:
            servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=data)
            servicosconcluidos = ServicosAgendados.query.filter_by(status=1,data_agendamento=data)
            servicoscancelados = ServicosAgendados.query.filter_by(status=2,data_agendamento=data)
        else:
            servicosagendados = ServicosAgendados.query.all()
            servicosconcluidos = ServicosAgendados.query.filter_by(status=1)
            servicoscancelados = ServicosAgendados.query.filter_by(status=2)
    return render_template('agenda.html', servicosagendados = servicosagendados, servicosconcluidos=servicosconcluidos, servicoscancelados=servicoscancelados)


@app.route("/excluirservicoagendado/<int:id>")
def excluirservicoagendado(id):
    servico_agendado = ServicosAgendados.query.filter_by(id_servico_agendado=id).first()

    db.session.delete(servico_agendado)
    db.session.commit()

    servicosagendados = ServicosAgendados.query.all()
    return render_template('agenda.html', servicosagendados = servicosagendados)


@app.route("/atualizarServicos/<int:id>", methods=['GET', 'POST'])
def atualizarServicos(id):
    servico = Servicos.query.filter_by(id_servicos=id).first()
    
    if request.method == "POST":
        nome = request.form.get("servico")
        preco = request.form.get("preco")
       
        if nome and preco:
            servico.nome = nome
            servico.preco = preco

            db.session.commit()

            return redirect(url_for("servicos"))
    
    return render_template("atualizarServicos.html", servico=servico)


@app.route("/statusAgendamento/<int:id>", methods=['GET', 'POST'])
def statusAgendamento(id):
    servicosagendados = ServicosAgendados.query.filter_by(id_servico_agendado=id).first()

    if request.method == "POST":
        status = request.form.get("status")
       
        if status :
            servicosagendados.status = status
            desc_status = StatusAgendamento.query.filter_by(id_status=status).first()
            servicosagendados.desc_status = desc_status.desc_status
            db.session.commit()

            return redirect(url_for("agenda"))

    return render_template('statusAgendamento.html', servicosagendados = servicosagendados)

@app.route("/atualizarCliente/<int:id>", methods=['GET', 'POST'])
def atualizarCliente(id):
    cliente = cliente = Clientes.query.filter_by(id_cliente=id).first()
    erro = ""
    if request.method == "POST":
        nome = request.form.get("nome_cliente")
        cpf = request.form.get("cpf_cliente")
        telefone = request.form.get("telefone_cliente")
        

        if nome and cpf and telefone:
            valido = cpf_validate(cpf)
            if valido == True:
                cliente.nome = nome
                cliente.cpf = cpf
                cliente.telefone = telefone

                db.session.commit()

                return redirect(url_for("clientes"))
            else:
                erro = "CPF Inválido"

    
    return render_template("atualizarCliente.html", cliente = cliente, erro=erro)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

def cpf_validate(numbers):

    cpf = [int(char) for char in numbers if char.isdigit()]


    if len(cpf) != 11:
        return False

    if cpf == cpf[::-1]:
        return False

    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

    

app.run(debug=True)