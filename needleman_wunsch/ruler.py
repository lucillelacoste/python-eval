import numpy as np
from colorama import Fore, Style


## Fonctions préliminaires
def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def dist(a, b):
    if a == b:
        return 0
    else:
        return 1


## Classe Ruler

class Ruler:
    def __init__(self, chaine1, chaine2, distance = None):
        self.chaine1 = chaine1
        self.chaine2 = chaine2
        self.distance = distance
    
    def F(self):
        n = len(self.chaine1)
        m = len(self.chaine2)
        chaine1 = list(self.chaine1)
        chaine2 = list(self.chaine2)
        F = np.zeros((n, m))
        d = 1
        for j in range(m):
            F[0,j] = d*j
        for i in range(n):
            F[i,0] = d*i
        for i in range(n):
            for j in range(m):
                choice_1 = F[i-1, j-1] + dist(chaine1[i-1], chaine2[j-1])
                choice_2 = F[i, j-1] + d
                choice_3 = F[i-1, j] + d
                F[i, j] = min(choice_1, choice_2, choice_3)
        return F

    def compute(self):
        n = len(self.chaine1)
        m = len(self.chaine2)
        self.distance = self.F()[n-1, m-1]
    
    def report(self):
        ''' On remonte la matrice F à partir de F(n,m). 
        d est la distance engendrée lorsqu'une lettre de chaine1 correspond 
        à un trou de chaine2 et vice-versa. 
        '''
        d = 1
        n = len(self.chaine1)
        m = len(self.chaine2)
        chaine1 = list(self.chaine1)
        chaine2 = list(self.chaine2)
        F = self.F()
        alignement1 = ""  # on définit ce qui sera la séquence finale 1 après comparaison
        alignement2 = ""  # on définit ce qui sera la séquence finale 2 après comparaison
        i = n - 1
        j = m - 1
        while i > 0 and j > 0:
            if F[i, j] == F[i-1, j-1] + dist(chaine1[i-1], chaine2[j-1]):
                if chaine1[i-1] != chaine2[j-1]:
                    alignement1 = red_text(chaine1[i-1]) + alignement1
                    alignement2 = red_text(chaine2[j-1]) + alignement2
                else:
                    alignement1 = chaine1[i-1] + alignement1
                    alignement2 = chaine2[j-1] + alignement2
                i = i - 1
                j = j - 1
            elif F[i, j] == F[i, j-1] + d:
                alignement1 = red_text("=") + alignement1
                alignement2 = chaine2[j-1] + alignement2
                j = j-1
            else:
                alignement1 = chaine1[i-1] + alignement1
                alignement2 = red_text("=") + alignement2
                i = i-1
        while i > 0:
            alignement1 = chaine1[i-1] + alignement1
            alignement2 = red_text("=") + alignement2
            i = i - 1
        while j > 0:
            alignement1 = red_text("=") + alignement1
            alignement2 = chaine2[j-1] + alignement2
            j = j - 1
        return f"{alignement1}", f"{alignement2}"
    