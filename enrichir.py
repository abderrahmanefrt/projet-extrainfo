import re
from sys import argv

extra_file = open('subst_corpus.dic', 'w', encoding="UTF-16 LE")
extra_file.write(u'\ufeff')  

with open('subst.dic', 'r', encoding="UTF-16 LE") as file:
    subst_step1 = file.read().replace(u'\ufeff', '').split("\n")
subst_step1 = [line for line in subst_step1 if line.strip() != '']

existing_dict = {line.split(',')[0].lower() for line in subst_step1}

with open(argv[1], 'r', encoding="UTF-8") as file:
    corpus_text = file.read().replace(u'\u00A0', ' ')

substance_pattern = r'^[ 0-9\tØ-]*([A-Za-zéèê]{3,})( LP)?[ :]*?(\d+(\.\d+|,\d+)?|(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)[ ])[ :]*?(mg|U[ ]|UI|g|µg|ml|[,: ]?[ ]?\d*?(/j|sachet(s)?))'
substances = re.findall(substance_pattern, corpus_text, re.I | re.M)

corpus_set = set()
for sub in substances:
    substance_name = sub[0].lower()
    extra_file.write(f'{substance_name},.N+subst\n')
    corpus_set.add(substance_name)
extra_file.close()

final_result = sorted(existing_dict.union(corpus_set))
enrichissement = sorted(corpus_set.difference(existing_dict))

with open('subst.dic', 'w', encoding="UTF-16 LE") as finaldict:
    finaldict.write(u'\ufeff')
    for entry in final_result:
        finaldict.write(f'{entry},.N+subst\n')

letter_marker = 'a'
letter_counter = 0
total_counter = 0
with open('infos2.txt', 'w', encoding="UTF-8") as f2:
    for substance in sorted(corpus_set):
        while letter_marker < substance[0]:
            f2.write("=========================================================================" + "\n")
            f2.write(f'{letter_marker.upper()}: {letter_counter}\n')
            f2.write("=========================================================================" + "\n")
            total_counter += letter_counter
            letter_counter = 0
            letter_marker = chr(ord(letter_marker) + 1)
        letter_counter += 1
        f2.write(f'{substance}\n')

    f2.write("=========================================================================" + "\n")
    f2.write(f'{letter_marker.upper()}: {letter_counter}\n')
    f2.write("=========================================================================" + "\n")
    total_counter += letter_counter
    f2.write(f'Nombre total de substances actives issues du corpus: {total_counter}\n')

letter_marker = 'a'
letter_counter = 0
total_counter = 0
with open('infos3.txt', 'w', encoding="UTF-8") as f3:
    for substance in enrichissement:
        while letter_marker < substance[0]:
            f3.write("=========================================================================" + "\n")
            f3.write(f'{letter_marker.upper()}: {letter_counter}\n')
            f3.write("=========================================================================" + "\n")
            total_counter += letter_counter
            letter_counter = 0
            letter_marker = chr(ord(letter_marker) + 1)
        letter_counter += 1
        f3.write(f'{substance}\n')

    f3.write("=========================================================================" + "\n")
    f3.write(f'{letter_marker.upper()}: {letter_counter}\n')
    f3.write("=========================================================================" + "\n")
    total_counter += letter_counter
    f3.write(f'Nombre total de substances actives pour l’enrichissement: {total_counter}\n')
