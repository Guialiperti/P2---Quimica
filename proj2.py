import math
import json
import sys

class BuildBattery():
    def __init__(self, metal1, metal2, mass1, mass2, concen1, concen2, temp):
        self.metal1 = metal1
        self.metal2 = metal2
        self.mass1 = mass1
        self.mass2 = mass2
        self.concen1 = concen1
        self.concen2 = concen2
        self.temp = temp
        self.ddp = self.ddpCalc()
        self.c_capacity = self.charge_capacity()
        self.potency = self.potencyCalc()

    def ddpCalc_primary(self):
        e1 = self.metal1["E"]

        if self.metal2["E"] > e1:
            e0 = self.metal2["E"] - e1
            cathode = self.metal2
            anode = self.metal1
            cathode_sol = self.concen2
            anode_sol = self.concen1
        else:
            e0 = e1 - self.metal2["E"]
            cathode = self.metal1
            anode = self.metal2
            cathode_sol = self.concen1
            anode_sol = self.concen2
        
        return e0, cathode, anode, cathode_sol, anode_sol

    def charge_capacity(self):
        electron = 1.6021 * (10**(-19))
        avogrado = 6.0225 * (10 ** (23))
        faraday = electron * avogrado

        limit = self.mass1
        metal = self.metal1
        other = self.metal2
        if self.mass2 < limit:
            limit = self.mass2
            metal = self.metal2
            other = self.metal1
        
        e_mol = (metal["eletrons"] * limit * other["eletrons"]) / metal["M"]

        charge = faraday * e_mol / 3600 #CONFIRMAR SE É ISSO MESMO!!!!!!!!!!!!
        return charge
    
    def ddpCalc(self):
        self.temp += 273
        r = 8.314
        f = 96485
        e0, cat, ano, sol_cat, sol_ano = self.ddpCalc_primary()
        n = self.metal1["eletrons"] * self.metal2["eletrons"]
        k = sol_ano ** ano["eletrons"] / sol_cat ** cat["eletrons"]
        ddp = e0 - ((r*self.temp)/(n*f)) * math.log1p(k)
        return ddp

    def potencyCalc(self):
        pot = self.ddp * self.c_capacity
        return pot / 1000

class ChooseBattery():
    def __init__(self, ddp, pot, time, c_capacity):
        self.ddp = ddp
        self.pot = pot
        self.time = time
        self.c_capacity = c_capacity

    def sort(self, battery_list):
        price_list = []
        model_list = []
        serie_list = []
        paralel_list = []
        max_current_list = []

        for battery in battery_list:
            q_serie = 1
            q_paralel = 1
            q_tempo = 1

            ddp_atual = q_serie * battery_list[battery]["ddp"]
            while ddp_atual < self.ddp:
                q_serie += 1
                ddp_atual = q_serie * battery_list[battery]["ddp"]
            
            corrente = self.pot / (battery_list[battery]["ddp"] * q_serie)
            current_time = battery_list[battery]["cap_carga"] / corrente 
            while current_time < self.time:
                q_paralel += 1
                current_time = (battery_list[battery]["cap_carga"] * q_paralel) / corrente

            price = (q_serie + q_paralel) * battery_list[battery]["preco"]

            price_list.append(price)
            model_list.append(battery_list[battery]["nome"])
            serie_list.append(q_serie)
            paralel_list.append(q_paralel)
            max_current_list.append(2 * battery_list[battery]["cap_carga"] * q_paralel)

        min_price = min(price_list)
        index = price_list.index(min_price)

        return model_list[index], max_current_list[index], serie_list[index], paralel_list[index], price_list[index]

        

def choose_option():
    print("--------------------------------------------------")
    print("Bem-vindo ao construtor de pilhas\n")
    print("Feito por: Daniel Ruhman, Gabriel Moura, Guilherme Aliperti\n")
    print("5 Semestre - Engenharia da Computação")
    print("--------------------------------------------------\n")
    print("Primeiro escolha uma opção:")
    print("Digite 0 para montar uma pilha com suas configurações")
    print("Digite 1 para encontrarmos uma pilha com as melhores configurações para sua aplicação")
    user_choice = int(input("Opção escolhida:"))
    return user_choice


def battery_assemble(material_list):
    print("--------------------------------------------------")
    print("Escolha 2 metais a partir da lista abaixo\n")
    print("ID | Metal")
    for material in material_list:
        print("{0} : {1}".format(material_list[material]["id"], material_list[material]["nome"]))
    print("--------------------------------------------------")
    print("Digite o ID dos metais escolhidos")
    metal_1_id = int(input("\nMetal 1: "))
    metal_2_id = int(input("\nMetal 2: "))
    print("Agora digite a massa de cada um dos materias")
    metal_1_mass = int(input("Massa do primeiro metal em gramas: "))
    metal_2_mass = int(input("Massa do segundo metal em gramas: "))
    print("Digite a concentração da solução de cada metal ")
    metal_1_concen = int(input("Concentração do primeiro metal em mol/L: "))
    metal_2_concen = int(input("Concentração do segundo metal em mol/L: "))
    print("Para finalizar, digite a temperatura da pilha")
    temp = int(input("Temperatura em Celsius: "))
    for i in range(30):
        print("Computando....")
    print("--------------------------------------------------")
    metal1 = material_list[str(metal_1_id)]
    metal2 = material_list[str(metal_2_id)]
    battery = BuildBattery(metal1, metal2, metal_1_mass, metal_2_mass, metal_1_concen, metal_2_concen, temp)
    
    print("De acordo com as configurações escolhidas essa seria sua bateria:")
    print("DDP: {0}".format(battery.ddp))
    print("Corrente: {0} mA".format(2 * battery.c_capacity))
    print("Capacidade de carga: {0} mAh".format(battery.c_capacity))
    print("Potência: {0} W/h".format(battery.potency))
    print("--------------------------------------------------")


def sort_battery(comercial_list):
    print("------------------------------")
    print("Inpute as configurações desejadas\n")
    ddp = int(input("DDP em Volts: "))
    pot = int(input("Potência em W/h: "))
    time = int(input("Tempo de utilização em horas: "))
    c_capacity = int(input("Capacidade de carga em Ah: "))
    for i in range(30):
       print("Computando....")
    print("-----------------------------------------")
    escolha = ChooseBattery(ddp, pot, time, c_capacity)
    model, max_current, serie, paralel, price = escolha.sort(comercial_list)

    print("--------------------------------------")
    print("A bateria mais barata que atende as suas necessidade é: {0}".format(model))
    print("Corrente máxima da bateria: {0} mA".format(max_current))
    print("A configuração de {0} células em série e {1} células em paralelo".format(serie, paralel))
    print("Total de pilhas utilizado: {0}".format(paralel + serie))
    print("Custo total da bateria: R$ {0}".format(price))
    print("---------------------------------------")
    
    


with open("metais.json", "r") as fp:
    material_list = json.load(fp)

with open("pilhas_comerciais.json") as fp:
    comercial_list = json.load(fp)

option = choose_option()
if option == 0:
    battery_assemble(material_list)
else:
    sort_battery(comercial_list)
