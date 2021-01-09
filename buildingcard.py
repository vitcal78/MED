from probGraphicalModels import Belief_network
from probVariables import Variable
from probFactors import Prob
from probMCMC import Gibbs_sampling
import json

def rt(patologia,q,regole):

    distribuzione = q[1]

    elenco = set()

    for terapia in regole:
        for reg in regole[terapia]:            
            if ((reg[0]==patologia) & (distribuzione[reg[1]]>=reg[2])):
                elenco.add(terapia)
    
    return elenco


fi = json.load(open("cardiologia.json"))

var = fi['variables']

elenco_terapie = fi['therapies']

patients = json.load(open("osservazioni.json"))

var_dict = dict()                  ### dizionario variabili con distrubuzioni e descrizione
var_list = list()                  ### lista delle variabili da dare in pasto alla BN 

for v in var:
    var_dict[v] = Variable(v,var[v][1])              ### costruisce una variabile da inserire nella BN dal dizionario variabili 
    var_list.append(var_dict[v])

prob_dict = dict()                                   ### dizionario probability table 
prob_list = list()                                   ### lista probability table da inseriore nella BN 

for v in var:
    nod = var_dict[v]   

    gen = list()

    lis = var[v][3]                                   ### lista genitori della singola variabile 

    for l in lis:
        gen.append(var_dict[l])        
    
    prob_dict[v] = Prob(nod,gen,var[v][4])           ### costruzione probability table: variabile, genitore, distribuzioni di probabilità 

    prob_list.append(prob_dict[v])                   ### append in lista probability table da inseriore in BN 

    print(prob_dict[v])
    
bn = Belief_network(var_list,prob_list)

sampling = Gibbs_sampling(bn)                        ### sampling di Gibbs 

##### costruita base ^^^^^^


lista_patologie = list()                             ### lista patologia da estrarre nella BN 

for pat in var:
    if (var[pat][2]=="patologia"):
         lista_patologie.append(pat)                ### completato append liste patologie da BN 

for paz in patients:

    print("\n\nNome paziente:"+patients[paz][0]+"\n")

    listaOsservazioni = patients[paz][1]

    ##print(listaOsservazioni)

    diz_oss = dict()

    terapie = set()

    for oss in listaOsservazioni:
                
        print("    "+var[oss][2]+" "+var[oss][0]+" "+patients[paz][1][oss])

        diz_oss[var_dict[oss]] = patients[paz][1][oss]               ### viene creato un dizionario osservazioni da inserire nel sampling 

        ##print(var_dict[oss])
        ##print(patients[paz][1][oss])   

    for pat in lista_patologie:        

        print("\n    Probabilità "+var[pat][0]+" ") 

        query = sampling.query(var_dict[pat],diz_oss)               ### la BN risponde con un grado di credenza su tutte le patologie, 
        
        print("    "+str(query))                                                            ### tenendo conto delle osservazioni date (sintomi ed esami eseguiti)
       
        ins = rt(pat,query,elenco_terapie)      

        terapie = terapie|ins

    print("\n    Terapie suggerite:\n")

    print("    "+str(terapie))
 
    
    
   




