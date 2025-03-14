import os
import sys
import glob
from bs4 import BeautifulSoup
import codecs

def extraction_medical(directory):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    substances = {}
    counteur = 0

 
    file_paths = [os.path.join(directory, f'vidal-Sommaires-Substances-{i}.htm') for i in alphabet]
    
    for file_path in file_paths:
        try:
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                continue

            print(f"Processing file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html5lib')

               
                for element in soup.select(f'#letter{os.path.basename(file_path)[-5].lower()} > li'):
                    substance = element.find("a").string.strip().lower()
                    initial_letter = substance[0].upper()
                    
                    if initial_letter not in substances:
                        substances[initial_letter] = []
                    
                    substances[initial_letter].append(substance)
                    counteur += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return substances, counteur

def write_delaf_dictionary(substances, output_file):
    with codecs.open(output_file, 'w', encoding='utf-16-le') as file:
        file.write('\ufeff')  
        for initial_letter in sorted(substances.keys()):
            for substance in sorted(substances[initial_letter]):
                file.write(f"{substance},.N+subst\n")

def write_info_file(substances, counteur, info_file):
    with open(info_file, 'w', encoding='utf-8') as file:
        for initial_letter in sorted(substances.keys()):
            file.write(f"{initial_letter}: {len(substances[initial_letter])}\n")
        file.write(f"Total: {counteur}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extraire.py <VIDAL_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    substances, counteur = extraction_medical(directory)
    write_delaf_dictionary(substances, 'subst.dic')
    write_info_file(substances, counteur, 'infos1.txt')

    for initial_letter in sorted(substances.keys()):
        print(f"{initial_letter}: {len(substances[initial_letter])}")
    print(f"Total: {counteur}")

if __name__ == "__main__":
    main()