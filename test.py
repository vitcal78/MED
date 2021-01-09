from probGraphicalModels import Belief_network
from probVariables import Variable
from probFactors import Prob
from probMCMC import Gibbs_sampling

boolean = [False,True]

Al = Variable("Alarm", boolean)
Fi = Variable("Fire", boolean)
Le = Variable("Leaving", boolean)
Re = Variable("Report", boolean)
Sm = Variable("Smoke", boolean)
Ta = Variable("Tamper", boolean)

f_ta = Prob(Ta,[],[0.98,0.02])
f_fi = Prob(Fi,[],[0.99,0.01])
f_sm = Prob(Sm,[Fi],[0.99,0.01,0.1,0.9])
f_al = Prob(Al,[Fi,Ta],[0.9999, 0.0001, 0.15, 0.85, 0.01, 0.99, 0.5, 0.5])
f_lv = Prob(Le,[Al],[0.999, 0.001, 0.12, 0.88])
f_re = Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])

bn2 = Belief_network([Ta,Fi,Le,Re,Sm,Al],[f_ta,f_fi,f_sm,f_al,f_lv,f_re])

bn2g = Gibbs_sampling(bn2)

a=bn2g.query(Le,{Al:True,Ta:True})
b=bn2g.query(Le,{Ta:True})
c=bn2g.query(Le,{Al:True})

print(a)
print(b)
print(c)