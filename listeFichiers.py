import os
from datetime import datetime
import getFileMetaData
import platform
import pandas as pd
# importing pwd module  
#import pwd 

# Spécifiez le chemin du répertoire que vous souhaitez lister
repertoire = "C:/Users/hp/Documents/MSEFC/Pentest"

# Nom de l'ordinateur sur lequel le script tourne
nom_ordinateur = platform.node()

# Liste pour stocker les métadonnées des fichiers
metadonnees = []

for racine, sous_repertoires, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            chemin_complet = os.path.join(racine, fichier)
            # Les fichiers cachés
            fichier_cache = True if fichier.startswith('.') else False
            # Return the size, in bytes, of path
            taille = os.path.getsize(chemin_complet)  # Taille en octets
            # Return the time of last modification of path. (timestamp)
            modified_datetime = datetime.utcfromtimestamp(os.path.getmtime(chemin_complet))
            # Return the time of last access of path
            accessed_datetime = datetime.utcfromtimestamp(os.path.getatime(chemin_complet))
            # Return the system's ctime which, on some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time for path
            created_datetime = datetime.utcfromtimestamp(os.path.getctime(chemin_complet))
            # Return True if pathname path is a mount point: a point in a file system where a different file system has been mounted
            mount_point = os.path.ismount(chemin_complet)
            # Renvoie une version absolue et normalisée du chemin d'accès path
            absolute_path = os.path.abspath(chemin_complet)
            
            # Récupérer les informations du propriétaire (sous Unix)
            infos_fichier = os.stat(chemin_complet)
            #proprietaire = pwd.getpwuid(infos_fichier.st_uid).pw_name
            file_owner = infos_fichier.st_uid

            # Ajoutez les métadonnées à la liste
            metadonnees.append({
                "Nom du fichier": fichier,
                "Chemin complet": chemin_complet,
                "Fichier caché": fichier_cache,
                "Taille (octets)": taille,
                "Date de création": created_datetime,
                "Date de modification": modified_datetime,
                "Date du dernier accès": accessed_datetime,
                "Point de montage": mount_point,
                "Chemin absolue": absolute_path,
                "Propriétaire du fichier": file_owner,
                #"Nom Propriétaire du fichier": proprietaire,
                #"Permissions de fichier:",file_permissions)
           })
                
# Créez un DataFrame à partir de la liste de métadonnées
df_metadonnees = pd.DataFrame(metadonnees)

# Affichez le DataFrame
print(df_metadonnees[["Date de création"]])
print("Nombre de fichiers", df_metadonnees.shape[0])
print(df_metadonnees)

# Enregistrement du DataFrame dans un fichier Excel
nom_fichier = "Metadonnees"  # Nom du fichier Excel
df_metadonnees.to_csv(nom_fichier)  # index=False pour ne pas inclure les index dans le fichier Excel

# =============================================================================
# # Utilisez os.listdir() pour obtenir la liste des fichiers dans le répertoire
# fichiers = os.listdir(repertoire)
# 
# # Parcourez la liste de fichiers et affichez-les un par un
# for fichier in fichiers:
#     print(fichier)
#     chemin_du_fichier = repertoire + '/' + fichier
#     # Vérifiez si le fichier existe
#     #if os.path.exists(chemin_du_fichier):
# 
#     # Vérifiez si le chemin correspond à un fichier
#     if os.path.isfile(chemin_du_fichier):
# 
#         # Extensions d'images courantes
#         image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.ico', 'svg', '.ai', '.eps', '.psd', '.heic']  
# 
#     
#         print(f"{chemin_du_fichier} est un fichier.")
#         
#          # Obtenez les informations sur le fichier
#         infos_fichier = os.stat(chemin_du_fichier)
#     
#         # Récupération des metadonnées
#         file_name = os.path.basename(chemin_du_fichier)
#         file_size = infos_fichier.st_size
#         created_datetime = datetime.utcfromtimestamp(infos_fichier.st_ctime)
#         modified_datetime = datetime.utcfromtimestamp(infos_fichier.st_mtime)
#         accessed_datetime = datetime.utcfromtimestamp(infos_fichier.st_atime)
#         file_owner = infos_fichier.st_uid
#         file_permissions = oct(infos_fichier.st_mode & 0o777)
#         file_path = os.path.abspath(chemin_du_fichier) # Chemin d'accès
# 
# 
#         # Affichez les métadonnées de base
#         print("Nom du fichier:", file_name)
#         print("Taille du fichier en octets:", file_size)
#         print("Date de création:", created_datetime)
#         print("Date de modification:", modified_datetime)
#         print("Date d'accès:", accessed_datetime)
#         print("Propriétaire du fichier:", file_owner)
#         print("Permissions de fichier:",file_permissions)
#         print("Chemin d'accès", file_path)
#         print("Nom de l'Ordinateur", nom_ordinateur)
#         
#         #print("Date de création formatée:", created_timestamp.isoformat())
#     
#         # Utilisez os.path.splitext() pour obtenir l'extension
#         nom_base, extension = os.path.splitext(chemin_du_fichier)
#         print("Extension du fichier:", extension)
# 
#         print(25*'*')
#         if extension == '.docx':
#             getFileMetaData.extractDOCXMeta(chemin_du_fichier)
#         elif extension == '.pdf':
#             getFileMetaData.extractPDFMeta(chemin_du_fichier)
#         elif extension in image_extensions:
#             getFileMetaData.extractImgMeta(chemin_du_fichier)
#             
#         print(25*'-')
# 
#     else:
#         print(f"{chemin_du_fichier} n'est pas un fichier.")
# =============================================================================
        
    #else:
    #    print("Le fichier n'existe pas.")
