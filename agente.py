"""
Sistema MED - Sistema esperto basato su Belieft Network, 
              a supporto diagnostico e suggerimento terapeutico
Autore: Vittorio Calabrese 
Matr: 555662

Modulo Agente inferenziale : Elencazione osservazioni, 
                             inferenze e suggerimento terapeutico

"""


from base import Base
from probMCMC import Gibbs_sampling
from os import system

class Agente:

    def __init__(self,filename,fileosservazioni):

        self.base = Base(filename,fileosservazioni)        

        self.sampling = Gibbs_sampling(self.base.bn)
    
    """def rt(self,patologia,q,regole):

        distribuzione = q[1]

        elenco = set()

        for terapia in regole:
            for reg in regole[terapia]:            
                if ((reg[0]==patologia) & (distribuzione[reg[1]]>=reg[2])):
                    elenco.add(terapia)
    
        return elenco """

    """def infer(self):

        lista_patologie = list()                             ### lista patologia da estrarre nella BN 

        for pat in self.base.var:
            if (self.base.var[pat][2]=="patologia"):
                lista_patologie.append(pat)                ### completato append liste patologie da BN 
        
        for paz in self.base.patients:
            
            print("\n\nNome paziente:"+self.base.patients[paz][0]+"\n")

            listaOsservazioni = self.base.patients[paz][1]

            diz_oss = dict()
            terapie = set()

            for oss in listaOsservazioni:
                
                print("     osservato "+self.base.var[oss][2]+" "+self.base.var[oss][0]+" "+self.base.patients[paz][1][oss])

                diz_oss[self.base.var_dict[oss]] = self.base.patients[paz][1][oss]
            
            for pat in lista_patologie:        

                print("\n    Probabilità "+self.base.var[pat][0]+" ") 

                query = self.sampling.query(self.base.var_dict[pat],diz_oss)               ### la BN risponde con un grado di credenza su tutte le patologie, 
                                                                                           ### tenendo conto delle osservazioni date (sintomi ed esami eseguiti)   
                print("    "+str(query))  

                ins = self.rt(pat,query,self.base.elenco_terapie)      

                terapie = terapie|ins

            print("\n    Terapie suggerite:"+str(terapie))"""
    
    def infer(self):

        for paz in self.base.patients:           

            print("\n\nNome paziente:"+self.base.patients[paz][0]+"\n")

            listaOsservazioni = self.base.patients[paz][1]

            diz_oss = dict()
            terapie_appl = set()

            query_dict = dict()         

            for oss in listaOsservazioni:
                
                print("     osservato "+self.base.var[oss][2]+" "+self.base.var[oss][0]+" "+self.base.patients[paz][1][oss])

                diz_oss[self.base.var_dict[oss]] = self.base.patients[paz][1][oss]
        
            for terapia in self.base.elenco_terapie:                    ### iterazione terapie
                for reg in self.base.elenco_terapie[terapia]:           ### iterazione singole regole

                    chiave = self.base.var_dict[reg[0]]

                    if (chiave in query_dict):
                        query=query_dict[chiave]                        
                    else:                        
                        query = self.sampling.query(chiave,diz_oss)
                        query_dict.update({chiave:query})
                        print("    Studio probabilità "+str(self.base.var[reg[0]][2])+" "+str(self.base.var[reg[0]][0]))
                        print("    "+str(query[1]))
                                             

                                                          
                    if (query[1][reg[1]]>=reg[2]):
                        terapie_appl=terapie_appl|{terapia}
            
            for collisione in self.base.collisioni:
                for ter in self.base.collisioni[collisione]:
                    if (ter in terapie_appl):
                        terapie_appl=terapie_appl-{collisione}

            print("    \nTerapie suggerite:"+str(terapie_appl))

            system('pause')