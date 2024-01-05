# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 23:08:51 2023

@author: hp
"""

import pefile

# Chemin vers le fichier exécutable
exe_path = 'C:/Users/hp/Documents/MSEFC/ue7_Forensic1/RAM/strings.exe'

# Chargement du fichier PE
pe = pefile.PE(exe_path)
#print(pe.dump_info())

# Récupérer le point d'entrée (adresse) du programme
entry_point = pe.OPTIONAL_HEADER. AddressOfEntryPoint
print(f"Point d'entrée du programme : {hex(entry_point)}")

# Affichage des informations de l'en-tête
print("Adresse d'entrée du programme: 0x%x" % pe.OPTIONAL_HEADER.AddressOfEntryPoint)
#print("Liste des sections:")
# for section in pe.sections:
#     print(section.Name.decode().strip('\x00').decode(), hex(section.VirtualAddress), hex(section.Misc_VirtualSize))
# Parcourir et afficher les sections
print("Liste des sections :")
for section in pe.sections:
    print(section.Name.decode().strip('\x00'))
    print(hex(section.VirtualAddress), hex(section.Misc_VirtualSize))


# Accéder à d'autres parties des métadonnées si nécessaire, par exemple :
print("Liste des imports:")
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(entry.dll)
    for imp in entry.imports:
        print('\t', hex(imp.address), imp.name.decode())
        
        
# Récupérer les symboles exportés
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    export_symbols = pe.DIRECTORY_ENTRY_EXPORT.symbols
    print("Symboles exportés :")
    for symbol in export_symbols:
        print(symbol.name.decode('utf-8', 'ignore'))  # Décoder le nom du symbole en UTF-8
else:
    print("Aucun symbole exporté trouvé.")

# Fermer le fichier PE
pe.close()