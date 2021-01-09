from probGraphicalModels import Belief_network
from probVariables import Variable
from probFactors import Prob
from probMCMC import Gibbs_sampling

boolean = [False,True]


nodi = dict()

temp = Variable('infarto',boolean)

nodi['infarto'] = ('infarto del miocardio','patologia',temp,(temp,[],[0.2,0.8]))

temp = Variable('dolore',boolean)

nodi['dolore'] = ('dolore al petto','sintomo',temp,(temp,[nodi['infarto'][2]],[0.2,0.8,0.8,0.2]))

propertytable = dict()

propertytable['infarto'] = Prob(nodi['infarto'][2],[],nodi['infarto'][3][2])
propertytable['dolore'] =  Prob(nodi['dolore'][2],[nodi['infarto'][2]],nodi['dolore'][3][2])   

lista_nodi = list()

for n in nodi:
    lista_nodi.append(nodi[n][2])

lista_prop = list()

for p in propertytable:
    lista_prop.append(propertytable[p])

bn = Belief_network(lista_nodi,lista_prop)

bnq = Gibbs_sampling(bn)

a=bnq.query(nodi['infarto'][2],{nodi['dolore'][2]:True})

print(a)


