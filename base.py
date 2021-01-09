"""
Sistema MED - Sistema esperto basato su Belieft Network, 
              a supporto diagnostico e suggerimento terapeutico
Autore: Vittorio Calabrese 
Matr: 555662

Modulo Base di conoscenza : Costruzione della base di conoscenza e belief network

"""


import json
from probGraphicalModels import Belief_network
from probVariables import Variable
from probFactors import Prob


class Base:

    def __init__(self,filename,fileosservazioni):

        fi = json.load(open(filename))
        self.var = fi['variables']
        self.elenco_terapie = fi['therapies']
        self.collisioni = fi['false']        
        self.patients = json.load(open(fileosservazioni))

        self.var_dict = dict()                  ### dizionario variabili con distrubuzioni e descrizione
        self.prob_dict = dict()                                   ### dizionario probability table 

        var_list = list()                  ### lista delle variabili da dare in pasto alla BN 
        prob_list = list()                                   ### lista probability table da inseriore nella BN 

        for v in self.var:
            self.var_dict[v] = Variable(v,self.var[v][1])              ### costruisce una variabile da inserire nella BN dal dizionario variabili 
            var_list.append(self.var_dict[v])        

        for v in self.var:
            nod = self.var_dict[v]   
            gen = list()

            lis = self.var[v][3]                                   ### lista genitori della singola variabile 

            for l in lis:
                gen.append(self.var_dict[l])        
    
            self.prob_dict[v] = Prob(nod,gen,self.var[v][4])           ### costruzione probability table: variabile, genitore, distribuzioni di probabilità 
            

            prob_list.append(self.prob_dict[v])                   ### append in lista probability table da inseriore in BN 
            print(self.prob_dict[v])
        
        self.bn = Belief_network(var_list,prob_list)

        
