import os
from datetime import datetime
import getFileMetaData
import platform

# Spécifiez le chemin du répertoire que vous souhaitez lister
repertoire = "C:/Users/afadi/Documents/MS EFC"

nom_ordinateur = platform.node()

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

        # Extensions d'images courantes
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.ico', 'svg', '.ai', '.eps', '.psd', '.heic']  

    
        print(f"{chemin_du_fichier} est un fichier.")
        
         # Obtenez les informations sur le fichier
        infos_fichier = os.stat(chemin_du_fichier)
    
        # Récupération des metadonnées
        file_name = os.path.basename(chemin_du_fichier)
        file_size = infos_fichier.st_size
        created_datetime = datetime.utcfromtimestamp(infos_fichier.st_ctime)
        modified_datetime = datetime.utcfromtimestamp(infos_fichier.st_mtime)
        accessed_datetime = datetime.utcfromtimestamp(infos_fichier.st_atime)
        file_owner = infos_fichier.st_uid
        file_permissions = oct(infos_fichier.st_mode & 0o777)
        file_path = os.path.abspath(chemin_du_fichier) # Chemin d'accès


        # Affichez les métadonnées de base
        print("Nom du fichier:", file_name)
        print("Taille du fichier en octets:", file_size)
        print("Date de création:", created_datetime)
        print("Date de modification:", modified_datetime)
        print("Date d'accès:", accessed_datetime)
        print("Propriétaire du fichier:", file_owner)
        print("Permissions de fichier:",file_permissions)
        print("Chemin d'accès", file_path)
        print("Nom de l'Ordinateur", nom_ordinateur)
        
        #print("Date de création formatée:", created_timestamp.isoformat())
    
        # Utilisez os.path.splitext() pour obtenir l'extension
        nom_base, extension = os.path.splitext(chemin_du_fichier)
        print("Extension du fichier:", extension)

        print(25*'*')
        if extension == '.docx':
            getFileMetaData.extractDOCXMeta(chemin_du_fichier)
        elif extension == '.pdf':
            getFileMetaData.extractPDFMeta(chemin_du_fichier)
        elif extension in image_extensions:
            getFileMetaData.extractImgMeta(chemin_du_fichier)
            
        print(25*'-')

    else:
        print(f"{chemin_du_fichier} n'est pas un fichier.")
        
    #else:
    #    print("Le fichier n'existe pas.")
