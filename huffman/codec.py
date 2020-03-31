class TreeBuilder:
    def __init__(self, text):
        self.text = text
    
    def occ_lettre(self):
        ''' Retourne la liste des lettres associées à leurs occurences, 
        triées par ordre croissant des occurences
        '''
        dict = {}
        for e in self.text:
            if e in dict:
                dict[e] += 1
            else:
                dict[e] = 1
        list = sorted(dict.items(), key = lambda t : t[1])
        return list
    
    def tree(self):
        dict = {}
        list = self.occ_lettre()
        ''' on ajoute en feuille de l'arbre les lettres de base, 
        qui n'ont pas de descendant
        '''
        for e in list:
            dict[e] = [None]
        while len(list) > 1:
            ''' on trie les liste des occurences par nombre d'occurences croissant '''
            list = sorted(list, key = lambda t : t[1])
            ''' on actualise l'arbre avec le parent des deux feuilles de plus faible poids '''
            parent = (list[0][0] + list[1][0], list[0][1] + list[1][1])
            dict[parent] = [list[0], list[1]]
            ''' on actualise la liste des occurences avec les regroupements effectués '''
            list.remove(list[0])
            list.remove(list[0])
            list.append(parent)
        return dict


class Codec:
    def __init__(self, binary_tree):
        self.binary_tree = binary_tree
    
    def encode(self, text):
        tree = self.binary_tree
        racine = list(tree)[-1]
        
        ''' on crée un dico qui contiendra à terme les clés de l'arbre, avec leur codage '''
        dict = {tree[racine][0]: '0', tree[racine][1]: '1'}
        
        ''' on crée la liste des clés de l'arbre non encore codées '''
        L = list(tree)
        L.remove(racine)
        L.remove(tree[racine][0])
        L.remove(tree[racine][1])
        
        ''' on parcourt cette liste, et dès qu'on arrive à coder un de ses éléments 
        à l'aide de son parent, on l'enlève de L
        '''
        while len(L) > 0:
            ''' L2 est une liste tampon dont on enlève les cle_fils qui viennent 
            d'être codées en cours d'itération de cle_fils sur L, 
            pour ne pas que l'itération se fasse sur une L qui change. 
            On actualise L après l'itération
            '''
            L2 = L 
            for cle_fils in L:
                for cle in tree.keys():
                    ''' si cle est le parent de cle_fils '''
                    if cle_fils in tree[cle]:
                        ''' si cle est déjà codée, on code cle_fils avec un 0 
                        ou un 1 en plus selon s'il est à droite ou à gauche. 
                        Sinon, on passe à une autre cle
                        '''
                        if cle in dict.keys(): 
                            if cle_fils == tree[cle][0]:
                                dict[cle_fils] = dict[cle] + '0'
                                L2.remove(cle_fils)
                            else:
                                dict[cle_fils] = dict[cle] + '1'
                                L2.remove(cle_fils)
                        else:
                            break
            L = L2
        
        ''' on ne garde que les éléments du dico qui sont des lettres simples avec leur codage,
        et on crée avec cela un dictionnaire dont cle = lettre et valeur = codage associé. 
        Ce dictionnaire est global car on en a besoin dans la fonction de décodage
        '''
        global codage_lettre
        codage_lettre = {}
        for cle, valeur in dict.items():
            if len(cle[0]) == 1:
                codage_lettre[cle[0]] = valeur
        
        ''' on code le texte grâce à ce nouveau dictionnaire '''
        encoded_text = ''
        for lettre in text:
            encoded_text += codage_lettre[lettre]
        
        return encoded_text
                
    def decode(self, encoded):
        decoded = ''
        n = len(encoded)
        i = 0
        while i < n:
            j = i + 1
            while encoded[i:j] not in codage_lettre.values() and j <= n:
                j += 1
            for cle, item in codage_lettre.items():
                if item == encoded[i:j]:
                    decoded += cle
            i = j
        return decoded