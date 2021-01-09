
from display import Displayable

class Clause(object):
    """A definite clause"""

    def __init__(self,head,body=[]):
        """clause with atom head and lot of atoms body"""
        self.head = head
        self.body = body

    def __str__(self):
        """returns the string representation of a clause.21"""
        if self.body:
            return self.head + " <- " + " & ".join(self.body) + "."
        else:
            return self.head + "."

class Askable(object):
    """An askable atom"""

    def __init__(self,atom):
        """clause with atom head and lost of atoms body"""
        self.atom=atom

    def __str__(self):
        """returns the string representation of a clause."""
        return "askable " + self.atom + "."

class Assumable(object):
    """An askable atom"""

    def __init__(self,atom):
        """clause with atom head and lost of atoms body"""
        self.atom = atom

    def __str__(self):
        """returns the string representation of a clause.
        """
        return "assumable " + self.atom + "."

class KB(Displayable):
    """A knowledge base consists of a set of clauses.
    This also creates a dictionary to give fast access to the clauses with an atom in head.
    """
    def __init__(self, statements=[]):
        self.statements = statements
        self.clauses = [c for c in statements if isinstance(c, Clause)]
        self.askables = [c.atom for c in statements if isinstance(c, Askable)]
        self.atom_to_clauses = {}  # dictionary giving clauses with atom as head
        for c in self.clauses:
            if c.head in self.atom_to_clauses:
                self.atom_to_clauses[c.head].add(c)
            else:
                self.atom_to_clauses[c.head] = {c}

    def clauses_for_atom(self,a):
        """returns set of clauses with atom a as the head"""
        if a in self.atom_to_clauses:
            return  self.atom_to_clauses[a]
        else:
            return set()

    def __str__(self):
        """returns a string representation of this knowledge base.
        """
        return '\n'.join([str(c) for c in self.statements])

class KBA(KB):
    """A knowledge base that can include assumables"""

    def __init__(self,statements):
        self.assumables = [c.atom for c in statements if isinstance(c, Assumable)]
        KB.__init__(self,statements)
        
    def prove_all_ass(self, ans_body, assumed=set()):
        """returns a list of sets of assumables that extends assumed 
        to imply ans_body from self.
        ans_body is a list of atoms (it is the body of the answer clause).
        assumed is a set of assumables already assumed
        """
        if ans_body:
            selected = ans_body[0]   # select first atom from ans_body
            if selected in self.askables:
                if yes(input("Is "+selected+" true? ")):
                    return  self.prove_all_ass(ans_body[1:],assumed)
                else:
                    return []   # no answers
            elif selected in self.assumables:
                return self.prove_all_ass(ans_body[1:],assumed|{selected})
            else:
                return [ass
                        for cl in self.clauses_for_atom(selected)
                        for ass in self.prove_all_ass(cl.body+ans_body[1:],assumed)
                           ]  # union of answers for each clause with head=selected
        else:                 # empty body
            return [assumed]    # one answer 

    def conflicts(self):
        """returns a list of minimal conflicts"""
        return minsets(self.prove_all_ass(['false']))


b = [Clause("bypass",["infarto"]),Clause("ossigeno",["angina"]),Clause("False",['angina','infarto']),Assumable('infarto'),Assumable("angina")]

base = KBA(b)

print("Stampa della base\n")
print(base)

conflitti = base.prove_all_ass(['False'])   ### provo tutte le contraddizioni

print('Clausole inconsistenti ')
print(conflitti)

if ('infarto' in conflitti[0]):
    print('Infarto sarebbe una contraddizione')

ass_provato = base.prove_all_ass(['infarto'])  ### provo l'assumibile infarto
print('Terapia infarto ')
print(ass_provato)


prova_bypass = base.clauses_for_atom("bypass")   ### estrapolo tutte le clausole aventi come testa bypass (implicato)

print('Perchè effettuo un bypass ')

for c in prova_bypass:
    print(c) 
