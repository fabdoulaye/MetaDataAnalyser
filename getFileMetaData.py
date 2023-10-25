# getFileMetaData
# Pour extraire et afficher toutes les métadonnées d'un fichier PDF
from PyPDF2 import PdfReader

monPdF = "C:/Users/afadi/Documents/MS EFC/intro_formation.pdf"

def extractPDFMeta(chemin_du_pdf):
    # Ouvrez le fichier PDF en mode lecture
    reader = PdfReader(chemin_du_pdf)

    # Récupérez et affichez les métadonnées du fichier PDF
    meta = reader.metadata

    # Affichez les métadonnées du fichier PDF
    print("Auteur:", meta.author)
    print("Créateur:", meta.creator)
    print("Sujet:", meta.subject)
    print("Titre:", meta.title)
    print("Producteur:", meta.producer)
    print("Nombre de pages:", len(reader.pages))
    
    # Vérifiez si le fichier PDF est chiffré (protégé par un mot de passe)
    #if pdf.is_encrypted:
    #    print("Le fichier PDF est chiffré et nécessite un mot de passe pour accéder aux métadonnées.")
    #else:

extractPDFMeta(monPdF)
