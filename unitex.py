import os
from os import path

unitex_path = r"C:\Users\abdou\AppData\Local\Unitex-GramLab\App"

directory = "corpus-medical_snt"
if not path.exists(directory):
    os.mkdir(directory)
else:
    print(f"Directory '{directory}' already exists.")

os.system(f"{unitex_path}/UnitexToolLogger Normalize corpus-medical.txt -r Norm.txt")
os.system(f"{unitex_path}/UnitexToolLogger Tokenize corpus-medical.snt -a Alphabet.txt")
os.system(f"{unitex_path}/UnitexToolLogger Compress subst.dic")
os.system(f"{unitex_path}/UnitexToolLogger Dico -t corpus-medical.snt -a Alphabet.txt subst.bin Dela_fr.bin")
os.system(f"{unitex_path}/UnitexToolLogger Grf2Fst2 posologie.grf")
os.system(f"{unitex_path}/UnitexToolLogger Locate -t corpus-medical.snt posologie.fst2 -a Alphabet.txt -L -I --all")
os.system(f"{unitex_path}/UnitexToolLogger Concord corpus-medical_snt/concord.ind -f \"Courier New\" -s 12 -l 40 -r 55")

"""
Explication du fichier "Alphabet.txt" :
---------------------------------------
1. son role :
   - Définit les caractères acceptés (lettres, chiffres, accents, etc.) et leurs correspondances.
   - Sert à normaliser, tokeniser et appliquer les dictionnaires sur le texte.
    - Sans ce fichier, les étapes de traitement échouent ou donnent des résultats erronés.
2. Utilisation dans le script :
   - **Normalize** : Transforme les caractères spéciaux (ex. "é" → "e").
   - **Tokenize** : Segmente correctement le texte (ex. "100 mg" comme une unité).
   - **Dico** : Vérifie les correspondances entre le texte et le dictionnaire.
des Exemples  :
   - `é=e` : Normalise la lettre accentuée "é" en "e" pour garantir une cohérence linguistique.
   - `mg=m.g` : Définit "mg" comme une unité reconnue pour éviter les erreurs de segmentation.
   - `0=0` et `1=1` : Gère les chiffres en tant que caractères acceptés dans les unités lexicales.
   
"""
