import tkinter as tk
from tkinter import Frame, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import os
from datetime import datetime
import platform
import pandas as pd
import magic
import stat
import csv
import getFileMetaData
import win32security


root = tk.Tk()
tree = ttk.Treeview(root, show="headings")
status_label = tk.Label(root,font=("bold"), text="", padx=20, background="blue", foreground="white")

# Nom de l'ordinateur sur lequel le script tourne
nom_ordinateur = platform.node()



# Pour extraction de métadonnées spécifiques
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
metadataDOC = []
metadataIMG = []
list_metadata_Specific_name = []

# Création d'un dictionnaire pour mapper les extensions aux noms de listes
dict_listes = {
    ('.pdf'): 'metadataPDF',
    ('.docx'): metadataDOC,
    ('.jpeg', '.jpg', '.png', '.gif', '.svg', '.tif'): metadataIMG,
    #'.csv': metadataCSV,
    #'.txt': metadataTXT,
    # Ajoutez d'autres correspondances selon vos besoins
}

def browse():
    chemin_dossier = tk.filedialog.askdirectory()
    runMeta(chemin_dossier)

def main():
    root.title("Scan Folder")
    root.geometry("{}x{}".format(int(root.winfo_screenwidth()*0.8), int(root.winfo_screenheight()*0.7)))
    root.config(background="white")
    file_explorer = tk.Label(root, text="WELCOME TO METADATA ANALYSER FOR FOLDER FILES", font=("Verdana", 14, "bold"), width=root.winfo_screenwidth(), height=2, fg="white", bg="gray")
    

    button=tk.Button(root, text="Select Folder", font =("Roboto", 12, "bold"), width=12, height=2, command=browse)
    file_explorer.pack()
    button.pack(pady=10)
    status_label.pack()
    tree.pack(padx=20, pady=10, fill="both", expand=True)
    root.mainloop()

def runMeta(repertoire):
    
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
            
            # Récupérer l'extension pour le type MIME spécifique
            extension_mime = getFileMetaData.types_mime_extensions.get(file_type)
            #print(extension_mime)
            
            if extension_mime is not None :
                metadata_Specific_name = getFileMetaData.return_listData_name(dict_listes, extension_mime)
                # Specific Meta data
                SpecificMetaData = True
                # Vérifier si la valeur existe dans le dictionnaire et exécuter la fonction correspondante
                if extension_mime in fonctions:
                    # Accès à la variable à partir de son nom en utilisant globals()
                    globals()[metadata_Specific_name].append(fonctions[extension_mime](chemin_complet))
                    list_metadata_Specific_name.append(metadata_Specific_name)
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
                "Extension": extension,
                "Type MIME": file_type,
                "Extension MIME": extension_mime,
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


    # Affichez le DataFrame
     #print(df_metadonnees[["Date de création"]])
    print("Nombre de fichiers", df_metadonnees.shape[0])
    print(df_metadonnees)
    print(25*'-')

    # Enregistrement du DataFrame dans un fichier Excel
    nom_fichier = "Metadonnees.csv"  # Nom du fichier Excel
    df_metadonnees.to_csv(nom_fichier)  # index=False pour ne pas inclure les index dans le fichier Excel


    print(25*'-')
    # Création de DataFrames vide
    df_metadataPDF = pd.DataFrame()
    df_metadataDOC = pd.DataFrame()
    df_metadataIMG = pd.DataFrame()
    # Stockage des DataFrames dans un dictionnaire
    dataframes = {
        'metadataPDF': df_metadataPDF,
        'metadataDOC': df_metadataDOC,
        'metadataIMG': df_metadataIMG,
    }
    for df_specific_name in list_metadata_Specific_name:
        # Créez un DataFrame à partir de la liste de métadonnées
        dataframes[df_specific_name] = pd.DataFrame(globals()[df_specific_name])
        #print(dataframes[df_specific_name].head() )

    # Accès à tous les DataFrames du dictionnaire en les parcourant
    for nom_dataframe, dataframe in dataframes.items():
        if len(dataframe) != 0:
            print(f"Nom du DataFrame : {nom_dataframe}")
            print(dataframe.head())
            print("---------")

    print(25*'-')
                    
    # Créez un DataFrame à partir de la liste de métadonnées
    df_metadonnees = pd.DataFrame(metadonnees)
    df_metadonnees.to_csv("results.csv")
    display_csv_data("results.csv", repertoire)



def on_click(row):
    print(row)

def display_csv_data(file_path, repertoire):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            tree.delete(*tree.get_children())  # Clear the current data

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                tree.insert("", "end", values=row)
                tree.bind("<Button-1>", lambda e, row=row:on_click(row))

            status_label.config(text=f"Les résultats sont enregistrés à l'emplacement : {Path().resolve()}\\results.csv")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    main()
    

# # Utilisation de la fonction pour trouver une ligne par valeur dans une colonne
def return_specific_metadata(dictionnaire, extension, valeur):
    df_name = getFileMetaData.return_listData_name(dictionnaire, extension)
    df = pd.DataFrame(globals()[df_name])
    resultat = getFileMetaData.trouver_ligne_par_valeur(df, 'C:/Users/hp/Documents/MSEFC/Pentest/guide.pdf')
    if resultat is not None:
        print("Ligne correspondante :", resultat)
    else:
        print("Aucune correspondance trouvée.")
return_specific_metadata(dict_listes, '.pdf', 'C:/Users/hp/Documents/MSEFC/Pentest/guide.pdf')        