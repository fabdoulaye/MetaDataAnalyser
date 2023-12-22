import os
from datetime import datetime
import getFileMetaData
import platform
import pandas as pd
import magic
import stat
import win32security
# importing pwd module  
#import pwd 


# Spécifiez le chemin du répertoire que vous souhaitez lister
repertoire = "C:/Users/hp/Documents/MSEFC/Stage" #"C:/Users/hp/Documents/MSEFC/Pentest" #"C:\Program Files (x86)" #"C:/Users/hp/Documents/MSEFC" #"Pentest"

# Nom de l'ordinateur sur lequel le script tourne
nom_ordinateur = platform.node()

# Mapping des valeurs de la variable aux fonctions correspondantes
fonctions = {
    ".pdf" : getFileMetaData.extractPDFMeta,
    2: getFileMetaData.extractImgMeta ,
    3: getFileMetaData.extractDOCXMeta ,
}

# Liste pour stocker les métadonnées des fichiers
metadonnees = []
# Liste pour stocker les métadonnées des fichiers PDF
metadataPDF = []


for racine, sous_repertoires, fichiers in os.walk(repertoire):
    for fichier in fichiers:
        chemin_complet = os.path.join(racine, fichier)
        nom_fichier, extension = os.path.splitext(chemin_complet)
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
        
# =============================================================================
#             # Récupérer les informations du propriétaire (sous Unix)
#             infos_fichier = os.stat(chemin_complet)
#             proprietaire = pwd.getpwuid(infos_fichier.st_uid).pw_name
#             file_owner = infos_fichier.st_uid
# =============================================================================
        
        # Récupérer les informations du propriétaire (sous Unix)
        infos_fichier = os.stat(chemin_complet)

        # Obtenez les autorisations du fichier (permissions)
        autorisations = stat.S_IMODE(infos_fichier.st_mode)
        # Obtenez les autorisations du propriétaire du fichier (permissions)
        autorisations_proprietaire = infos_fichier.st_mode & 0o700  # Masque pour les autorisations du propriétaire

        # Affichage des autorisations séparément pour le propriétaire du fichier
        lecture_proprietaire = autorisations_proprietaire & stat.S_IRUSR != 0
        ecriture_proprietaire = autorisations_proprietaire & stat.S_IWUSR != 0
        execution_proprietaire = autorisations_proprietaire & stat.S_IXUSR != 0
        # Affichage des autorisations séparément pour le groupe du fichier
        lecture_groupe = autorisations & stat.S_IRGRP != 0
        ecriture_groupe = autorisations & stat.S_IWGRP != 0
        execution_groupe = autorisations & stat.S_IXGRP != 0
        # Affichage des autorisations séparément pour les autres utilisateurs du fichier
        lecture_autres = autorisations & stat.S_IROTH != 0
        ecriture_autres = autorisations & stat.S_IWOTH != 0
        execution_autres = autorisations & stat.S_IXOTH != 0
        
        
        
        # Récupérer les informations du propriétaire (sous Windows)
        infos_fichier = win32security.GetFileSecurity(chemin_complet, win32security.OWNER_SECURITY_INFORMATION)
        proprietaire_sid = infos_fichier.GetSecurityDescriptorOwner()
        proprietaire_nom, _, _ = win32security.LookupAccountSid(None, proprietaire_sid)
        
        
        # Créez un objet Magic pour accéder aux fonctionnalités de détection de type de fichier
        mime = magic.Magic()
        # Utilisez la méthode `from_file` pour déterminer le type de fichier
        file_type = mime.from_file(chemin_complet)
        
        # Système de fichiers
        #infos_fs = os.statvfs(chemin_complet)
        #type_fs = infos_fs.f_basetype
        
        empreinte_md5 = getFileMetaData.calculer_md5(chemin_complet)
        
        # Specific Meta data
        SpecificMetaData = True
        # Vérifier si la valeur existe dans le dictionnaire et exécuter la fonction correspondante
        if extension in fonctions:
            metadataPDF.append(fonctions[extension](chemin_complet))
        else:
            SpecificMetaData = False
            #print("Aucune fonction associée à cette valeur")


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
            "Propriétaire du fichier": proprietaire_nom, #file_owner,
            "Type MIME": file_type,
            "Extension": extension,
            "Permissions de fichier": autorisations,
            "Propriétaire Lecture" : lecture_proprietaire,
            "Propriétaire Ecriture" : ecriture_proprietaire ,
            "Propriétaire Exécution" : execution_proprietaire ,
            "Groupe Lecture" : lecture_groupe ,
            "Groupe Ecriture" : ecriture_groupe ,
            "Groupe Exécution" : execution_groupe ,
            "Autres Lecture" : lecture_autres ,
            "Autres Ecriture" : ecriture_autres ,
            "Autres Exécution" : execution_autres,
            "Hash MD5" : empreinte_md5,
            #"Système de fichiers" : type_fs
       })
                
# Créez un DataFrame à partir de la liste de métadonnées
df_metadonnees = pd.DataFrame(metadonnees)

# Créez un DataFrame à partir de la liste de métadonnées
df_metadataPDF = pd.DataFrame(metadataPDF)

# Affichez le DataFrame
 #print(df_metadonnees[["Date de création"]])
print("Nombre de fichiers", df_metadonnees.shape[0])
print(df_metadonnees)
print(25*'-')
print(df_metadataPDF )

# Enregistrement du DataFrame dans un fichier Excel
nom_fichier = "Metadonnees.csv"  # Nom du fichier Excel
df_metadonnees.to_csv(nom_fichier)  # index=False pour ne pas inclure les index dans le fichier Excel


print(25*'-')
# Utilisation de la fonction pour trouver une ligne par valeur dans une colonne
resultat = getFileMetaData.trouver_ligne_par_valeur(df_metadataPDF, 'Chemin', 'C:/Users/hp/Documents/MSEFC/Stage\offre_stage_pentest_2023-2024_v2.pdf')
if resultat is not None:
    print("Ligne correspondante :", resultat)
else:
    print("Aucune correspondance trouvée.")
