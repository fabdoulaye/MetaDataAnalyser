import os
import getFileMetaData

# Spécifiez le chemin du répertoire que vous souhaitez lister
repertoire = "C:/Users/afadi/Documents/MS EFC"

# Utilisez os.listdir() pour obtenir la liste des fichiers dans le répertoire
fichiers = os.listdir(repertoire)

# Parcourez la liste de fichiers et affichez-les un par un
for fichier in fichiers:
    print(fichier)
    chemin_du_fichier = repertoire + '/' + fichier
    # Vérifiez si le fichier existe
    #if os.path.exists(chemin_du_fichier):

    # Vérifiez si le chemin correspond à un fichier
    if os.path.isfile(chemin_du_fichier):
        print(f"{chemin_du_fichier} est un fichier.")
        
         # Obtenez les informations sur le fichier
        infos_fichier = os.stat(chemin_du_fichier)
    
        # Affichez les métadonnées de base
        print("Nom du fichier:", os.path.basename(chemin_du_fichier))
        print("Taille du fichier en octets:", infos_fichier.st_size)
        print("Date de modification (timestamp):", infos_fichier.st_mtime)
    
        # Utilisez os.path.splitext() pour obtenir l'extension
        nom_base, extension = os.path.splitext(chemin_du_fichier)
        print("Extension du fichier:", extension)

        if extension == '.pdf':
            getFileMetaData.extractPDFMeta(chemin_du_fichier)
            

    else:
        print(f"{chemin_du_fichier} n'est pas un fichier.")
        
    #else:
    #    print("Le fichier n'existe pas.")
