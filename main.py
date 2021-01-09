"""
Sistema MED - Sistema esperto basato su Belieft Network, 
              a supporto diagnostico e suggerimento terapeutico
Autore: Vittorio Calabrese 
Matr: 555662

Modulo principale : scelta della base di conoscenza

"""

from agente import Agente
from os import system

sel = 1


while (sel!='0'):
    system('cls')

    print("\n--------------------------------------------------------------")
    print("Sistema MED - supporto diagnostico e suggerimento terapeutico")
    print("--------------------------------------------------------------")

    casistica = {"1":("Casistica di Cardiologia","cardiologia.json","osservazioni_card.json"),
                 "2":("Casistica Covid","covid.json","osservazioni_covid.json")}

    print("\n"+str(casistica))

    sel=input("\nSelezionare la casistica (0 per uscire) -> ")

    if (sel!='0'):
        file_base = casistica[sel][1]
        file_osservazioni = casistica[sel][2]
        ag = Agente(file_base,file_osservazioni)
        ag.infer()
    



