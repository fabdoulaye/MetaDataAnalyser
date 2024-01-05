# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:32:27 2023

@author: hp
"""

import subprocess

# Chemin vers votre fichier
file_path = 'C:/Users/hp/Documents/MSEFC/Pentest/20231030_201315.jpg'

# Exécuter la commande icacls pour obtenir les permissions du fichier
result = subprocess.run(['icacls', file_path], capture_output=True, text=True)

# Afficher le résultat
print(result.stdout)

# Commande PowerShell pour obtenir les informations sur les privilèges du fichier
powershell_command = f"Get-Acl -Path '{file_path}' | Format-List"

# Exécution de la commande PowerShell
result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)

# Affichage des informations sur les privilèges
print(result.stdout)