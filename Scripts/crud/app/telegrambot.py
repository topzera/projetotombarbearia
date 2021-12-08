import requests
import time
import json
import os
import sqlite3
from datetime import datetime

banco = sqlite3.connect('tombarbearia.db')

cursor = banco.cursor()

#cursor.execute("CREATE TABLE servicos (id integer, nome text, preco integer, fk_usuario text)")

#cursor.execute("INSERT INTO servicos values (1, 'Cabelo',20 ,'')")

banco.commit()

class TelegramBot:
    def __init__(self):
        token = '2099403924:AAG-NaeCtUwNls6QMA-1XtIBN6WwpW6b4WU'
        self.url_base = f'https://api.telegram.org/bot{token}/'
    def Iniciar(self):
        stage = 0
        id_cliente = None
        cliente = None
        update_id = None
        id_servicos_disponiveis = self.servicos_disponiveis()
        horarios_atendimento= []
        servico_adquirido = []
        id_servico = None
        horario_agendado = None
        data_atual = str(datetime.today().strftime('%d-%m-%Y'))
        horario_atual = datetime.today().strftime('%H:%M')

        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado['message']['text'])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(dado["message"]["message_id"]) == 1

                    if stage == 0 and cliente == None:
                        resposta = "Olá bem-vindo ao Tom Barbearia digite o seu CPF ?"
                        self.responder(resposta, chat_id)
                        stage = 1
                        break
                    if stage == 1 and cliente == None:
                        consulta_cliente = self.e_cliente(mensagem)
                        id_cliente = consulta_cliente[0]
                        cliente = consulta_cliente[1]
                        if cliente == None:
                            stage = 1
                            resposta= "Se você ainda não for cliente, se cadastre em nosso salão... \nSe ja for cliente digite um CPF valido!!!"
                            self.responder(resposta, chat_id)
                            break
                    if stage == 1 and cliente != None:
                        resposta = self.criar_resposta(mensagem, eh_primeira_mensagem,cliente)
                        stage = 2
                        self.responder(resposta[1], chat_id)
                        break
                    if stage == 2:
                        if mensagem.lower() in ('menu'):
                            resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, cliente)
                            stage = 3
                            self.responder(resposta[1], chat_id)
                            break
                        else:
                            resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, cliente)
                            self.responder(resposta[1], chat_id)
                            break
                    if stage == 3:
                        validate = False
                        for i in range(len(id_servicos_disponiveis)):
                            if mensagem.lower() in str(id_servicos_disponiveis[i][0]):
                                resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, cliente)
                                self.responder(resposta[1], chat_id)
                                servico_adquirido.append(resposta[0])
                                id_servico = resposta[2]
                                stage = 4
                                validate = True
                                break
                        if validate == False:
                            resposta = "Desculpe não entendi, pode repetir? "
                            self.responder(resposta, chat_id)
                        break
                    if stage == 4:
                        if mensagem.lower() in ('s','sim','n','não','nao'):
                            horarios = self.horarios_disponiveis(2)
                            resposta = self.criar_resposta2(None, horarios, cliente,servico_adquirido)
                            self.responder(resposta[1], chat_id)
                            stage = 5
                            break
                        else:
                            resposta = "Desculpe não entendi, pode repetir? \nDigite 'S/N' "
                            self.responder(resposta, chat_id)
                            stage = 4
                            break
                        break
                    if stage == 5:
                        validate = False
                        horarios_disponiveis = self.horarios_disponiveis(1)
                        for i in range(len(horarios_disponiveis)):
                            if mensagem.lower() in str(horarios_disponiveis[i]):
                                resposta = self.criar_resposta2(mensagem, None, cliente,servico_adquirido)
                                self.responder(resposta[1], chat_id)
                                horario_agendado = resposta[0]
                                validate = True
                                stage = 6
                                break
                        if validate == False:
                            resposta = "Desculpe não entendi, pode repetir?\nDigite o número correspondente ao horários disponível !!!"
                            self.responder(resposta, chat_id)
                        break

                    if stage == 6:
                        if mensagem.lower() in ('n', 'não', 'nao'):
                            servico_adquirido = []
                            stage = 2
                            resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, cliente)
                            self.responder(resposta[1], chat_id)
                            break
                        elif mensagem.lower() in ('s', 'sim'):
                            resposta = self.criar_resposta(mensagem, eh_primeira_mensagem, cliente)
                            self.responder(resposta[1], chat_id)
                            self.agendamento(id_servico, servico_adquirido, id_cliente, cliente, horario_agendado,data_atual)
                            stage = 2
                            break
                        else:
                            resposta = ''' Desculpe não entendi !!! \nDigite 'S/N '''
                            self.responder(resposta, chat_id)
                            break
                        break

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Obter cliente
    def e_cliente(self,mensagem):
        mensagem = mensagem.replace(".","")
        mensagem = mensagem.replace("-", "")
        mensagem = mensagem.replace("/", "")
        try:
            cursor.execute("SELECT id_cliente, nome FROM clientes where cpf ="+mensagem)
            nm_cliente = cursor.fetchall()
            return nm_cliente[0]
        except:
            return [None,None]

    #Se o agendamento e concluido inseri na tabela
    def agendamento(self,fk_id_servico,desc_servico, fk_id_cliente,nm_cliente,horario_agendado,data_agendamento):
        id_servico = desc_servico[0][0]
        nm_servico = desc_servico[0][1]
        preco_servico = desc_servico[0][2]
        desc = f'''NOME: {nm_servico}, PREÇO: R${preco_servico},00'''
        cursor.execute(f'''INSERT INTO servicos_agendados(fk_id_servico,desc_servico,fk_id_cliente,nm_cliente,horario_agendado,data_agendamento) 
                            values ({fk_id_servico}, '{desc}',{fk_id_cliente} ,'{nm_cliente}', '{horario_agendado}','{data_agendamento}')''')
        banco.commit()

    #Pegar horarios disponiveis
    def horarios_disponiveis(self,status):
        data_atual = str(datetime.today().strftime('%d-%m-%Y'))
        horario_atual = str(datetime.today().strftime('%H:%M'))
        horarios_disponiveis = ""
        id_horarios_disponiveis=[]
        try:
            cursor.execute(f'''SELECT id_horario_funcionamento,horarios 
                                FROM horarios_funcionamento 
                                    WHERE horarios NOT IN 
                                    (SELECT horario_agendado 
                                        FROM servicos_agendados 
                                            WHERE data_agendamento = '{data_atual}')''')
            horarios = cursor.fetchall()
            for i in range(len(horarios)):
                for j in range(len(horarios[i])):
                    x = str(horarios[i][j])
                    x= x.replace(":","")
                    horario_atual = horario_atual.replace(":","")
                    if int(x) > int(horario_atual):
                        horarios_disponiveis += str(horarios[i][0])
                        horarios_disponiveis += " - "
                        horarios_disponiveis += str(horarios[i][j])
                        horarios_disponiveis +="\n"
                        id_horarios_disponiveis.append(horarios[i][0])
            if status == 1:
                return id_horarios_disponiveis
            return horarios_disponiveis
        except:
            return None

    # Criar resposta 2
    def criar_resposta2(self,mensagem,horarios,cliente,servicos):
        if mensagem == None:
            resp = [None, f'''{cliente} Escolha um horário que gostaria de agendar: \n{horarios}''']
            return resp
        else:
            if mensagem == '1':
                resp = ['9:00',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 9:00 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '2':
                resp = ['9:40',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 9:40 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '3':
                resp = ['10:20',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 10:20 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '4':
                resp = ['11:00',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 11:00 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '5':
                resp = ['11:40',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 11:40 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '6':
                resp = ['13:40',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 13:40 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '7':
                resp = ['14:20',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 14:20 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '8':
                resp = ['15:00',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 15:00 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '9':
                resp = ['15:40',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 15:40 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '10':
                resp = ['16:20',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 16:20 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '11':
                resp = ['17:00',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 17:00 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '12':
                resp = ['17:40',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 17:40 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '13':
                resp = ['18:20',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 18:20 horas? \nDigite "S/N" ''']
                return resp
            elif mensagem == '14':
                resp = ['19:00',
                        f'''{cliente} você tem certeza que deseja agendar {servicos[0][1]} R$ {servicos[0][2]} as 19:00 horas? \nDigite "S/N" ''']
                return resp

    def servicos_disponiveis(self):
        cursor.execute("SELECT id_servicos FROM servicos")
        servicos = cursor.fetchall()
        return servicos

    # Criar uma resposta 1
    def criar_resposta(self, mensagem, eh_primeira_mensagem,cliente):
        cursor.execute("SELECT id_servicos, nome, preco FROM servicos")
        servicos = cursor.fetchall()
        if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu'):
            msg = ""
            for i in range(len(servicos)):
                msg += "\n"
                for j in range(len(servicos[i])):
                    msg += " "
                    if type(servicos[i][j]) == int:
                        if servicos[i][j] > 10:
                            msg += "R$ "
                    msg += str(servicos[i][j])
            resp = [None, f'''Olá {cliente} bem-vindo ao Tom Barbearia digite o número do serviço que gostaria de agendar:{msg}''']
            return resp
        for i in range(len(servicos)):
            for j in range(len(servicos[i])):
                if str(servicos[i][0]) == mensagem:
                    resp = [servicos[i], f'''{cliente} você escolheu {servicos[i][1]} R$ {servicos[i][2]}, Deseja confirmar? digite "S/N" ''',servicos[i][0]]
                    return resp

        if mensagem.lower() in ('agendar', 'agendar'):
            msg = ""
            for i in range(len(servicos)):
                msg += "\n"
                for j in range(len(servicos[i])):
                    msg += " "
                    if type(servicos[i][j]) == int:
                        if servicos[i][j] > 10:
                            msg += "R$ "
                    msg += str(servicos[i][j])

            return f'''{cliente} digite o número do serviço que gostaria de agendar:{msg}'''
        
        elif mensagem.lower() in ('s', 'sim'):
            resp = [None,''' Agendamento Confirmado!!!  ''' ]
            return resp
        elif mensagem.lower() in ('n', 'não'):
            resp = [None, ''' Agendamento Cancelado!!! \nDigite "menu" para voltar ''']
            return resp
        else:
            resp = [None, f'''Olá {cliente} Bem-Vindo ao Tom Barbearia. Gostaria de acessar o menu? Digite "menu"''']
            return resp

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = TelegramBot()


bot.Iniciar()


