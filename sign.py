# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 17:25:02 2023

@author: hp
"""

import pefile
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def verifier_signature_pe(fichier_pe):
    pe = pefile.PE(fichier_pe)

    if hasattr(pe, 'DIRECTORY_ENTRY_SECURITY'):
        print("Le fichier est signé numériquement.")
        cert_raw = pe.get_data(pe.DIRECTORY_ENTRY_SECURITY.struct.OffsetToData, pe.DIRECTORY_ENTRY_SECURITY.struct.Size)
        cert = x509.load_der_x509_certificate(cert_raw, default_backend())

        print("Informations sur le certificat :")
        print("Émetteur :", cert.issuer)
        print("Sujet :", cert.subject)
        print("Valide du", cert.not_valid_before, "au", cert.not_valid_after)
    else:
        print("Le fichier n'est pas signé numériquement.")

# Spécifiez le chemin du fichier exécutable PE
chemin_fichier_exe = 'C:/Users/hp/Documents/MSEFC/ue7_Forensic1/RAM/strings.exe'

# Vérifiez et obtenez des informations sur la signature et le certificat associé
verifier_signature_pe(chemin_fichier_exe)
