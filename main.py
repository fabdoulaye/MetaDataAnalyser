import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import os
from datetime import datetime
import platform
import pandas as pd
import magic
import csv
import getFileMetaData
import win32security
import subprocess
import matplotlib
matplotlib.use('TkAgg')  # Set the backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


root = tk.Tk()
# Ajout d'un titre à la fenêtre principale :
root.title("Folder's Metadata Analyser")
# Définir un icone :
root.iconbitmap("logo.ico")
# Personnaliser la couleur de l'arrière-plan de la fenêtre principale :
#root.config(bg = "#87CEEB")


style = ttk.Style()

# Configuration du style pour le premier treeview
style.configure("Treeview1.Treeview", background="#FFC0CB")  # Couleur de fond  "Pink" pour le premier treeview

# Configuration du style pour le second treeview
style.configure("Treeview2.Treeview", background="lightblue")  # Couleur de fond pour le deuxième treeview


# style.configure("TFrame", background=	"#FFC0CB")

# style2 = ttk.Style()
# style2.configure("Treeview2", background="lightgreen")  # Couleur de fond pour le premier treeview

upper_container = ttk.Frame(root, style="Treeview1.Treeview")
upper_container.pack()

# Creation de la première fenêtre treeview
tree = ttk.Treeview(upper_container, show="headings")
status_label = tk.Label(upper_container ,font=("bold"), text="", padx=20, background="blue", foreground="white")
#tree.pack()

# Creation de la deuxième fenêtre treeview
bottom_tree = ttk.Treeview(root, style="Treeview2.Treeview")
# Constructing vertical scrollbar with treeview
verscrlbar = ttk.Scrollbar(root , 
						orient ="vertical", 
						command = bottom_tree.yview)

# Calling pack method w.r.to vertical scrollbar
verscrlbar.pack(side ='right', fill ='x')

# Configuring treeview
bottom_tree.configure(xscrollcommand = verscrlbar.set)

bottom_tree.column("#0", width=900)  # Largeur de la première colonne
bottom_tree.pack()


label = tk.Label(root, text="Répartition des fichiers du dossier selon leur type")
label.pack()

# Nom de l'ordinateur sur lequel le script tourne
nom_ordinateur = platform.node()

# Pour extraction de métadonnées spécifiques
# Mapping des valeurs de la variable aux fonctions correspondantes 
fonctions = {
    ".pdf"  : getFileMetaData.extractPDFMeta,
    ".jpg"  : getFileMetaData.extractImgMeta,
    ".jpeg" : getFileMetaData.extractImgMeta,
    ".png"  : getFileMetaData.extractImgMeta,
    ".gif"  : getFileMetaData.extractImgMeta,
    ".svg"  : getFileMetaData.extractImgMeta,
    ".tif"  : getFileMetaData.extractImgMeta,
    # ".webp" : getFileMetaData.extractImgMeta,
    ".docx" : getFileMetaData.extractDOCXMeta,
    ".exe" : getFileMetaData.extractEXEMeta ,
    ".elf" : getFileMetaData.extractELFMeta ,
    # ".mp4" : getFileMetaData.extractVIDEOMeta , #mime type
}

# Liste pour stocker les métadonnées des fichiers
metadonnees = []
# Liste pour stocker les métadonnées des fichiers PDF
metadataPDF = []
metadataDOC = []
metadataIMG = []
metadataEXE = []
metadataELF = []
metadataVIDEO = []
list_metadata_Specific_name = set() # Les éléments du set sont entre les symboles {} et un set ne contient pas de doublons.

# Création d'un dictionnaire pour mapper les extensions aux noms de listes
dict_listes = {
    ('.pdf'): 'metadataPDF',
    ('.docx'): 'metadataDOC',
    ('.jpeg', '.jpg', '.png', '.gif', '.svg', '.tif', '.webp'): 'metadataIMG',
    ('.exe'): 'metadataEXE',
    ('.elf'): 'metadataELF',
    ('.mp4'): 'metadataVIDEO',
    #'.csv': metadataCSV,
    #'.txt': metadataTXT,
    # Ajoutez d'autres correspondances selon vos besoins
}

def browse():
    # Ouvre une boîte de dialogue pour sélectionner un dossier
    chemin_dossier = filedialog.askdirectory()
    runMeta(chemin_dossier)


# # Utilisation de la fonction pour trouver une ligne par valeur dans une colonne
def return_specific_metadata(extension, chemin):
    df_name = getFileMetaData.return_listData_name(dict_listes , extension)
    df = pd.DataFrame(globals()[df_name])
    resultat_spec = getFileMetaData.trouver_ligne_par_valeur(df, chemin)
    if resultat_spec is not None:
        print("Ligne correspondante :", resultat_spec)
    else:
        print("Aucune correspondance trouvée.")
    print(type(resultat_spec))
    bottom_tree.delete(*bottom_tree.get_children())
    i=0
    for index, valeur in resultat_spec.items():
        print("index:", index)
        print("valeur:", valeur)
        if valeur is None: valeur = 'None'
        
        # Inserting items to the treeview 
        if index == 'Chemin':
            # Inserting parent
            bottom_tree.insert('', i, 'item' + str(i+1), text = valeur)
        else:
            # item = 
            # Inserting child
            bottom_tree.insert('', i, 'item' + str(i+1), text =index)
            # Inserting more than one attribute of an item
            bottom_tree.insert('item' + str(i+1), 'end', text =valeur)  
    
        i+=1
        
    #label.config(text=resultat_spec)
        
def main():
    # Définir les dimensions par défaut la fenêtre principale :
    root.geometry("{}x{}".format(int(root.winfo_screenwidth()*0.8), int(root.winfo_screenheight()*0.7)))
    root.config(background="#87CEEB") #○ "Sky Blue" 
    file_explorer = tk.Label(upper_container , text="WELCOME TO METADATA ANALYSER FOR FOLDER'S FILES", font=("Verdana", 14, "bold"), width=root.winfo_screenwidth(), height=2, fg="white", bg="gray")
    

    button=tk.Button(upper_container , text="Select Folder", font =("Roboto", 12, "bold"), width=12, height=1, command=browse)
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
    # # =============================================================================
    # #             # Récupérer les informations du propriétaire (sous Unix)
    # #             infos_fichier = os.stat(chemin_complet)
    # #             proprietaire = pwd.getpwuid(infos_fichier.st_uid).pw_name
    # #             file_owner = infos_fichier.st_uid
    # # =============================================================================
    #         
    #         # Récupérer les informations du propriétaire (sous Unix)
    #         infos_fichier = os.stat(chemin_complet)
    # 
    #         # Obtenez les autorisations du fichier (permissions)
    #         autorisations = stat.S_IMODE(infos_fichier.st_mode)
    #         # Obtenez les autorisations du propriétaire du fichier (permissions)
    #         autorisations_proprietaire = infos_fichier.st_mode & 0o700  # Masque pour les autorisations du propriétaire
    # 
    #         # Affichage des autorisations séparément pour le propriétaire du fichier
    #         lecture_proprietaire = autorisations_proprietaire & stat.S_IRUSR != 0
    #         ecriture_proprietaire = autorisations_proprietaire & stat.S_IWUSR != 0
    #         execution_proprietaire = autorisations_proprietaire & stat.S_IXUSR != 0
    #         # Affichage des autorisations séparément pour le groupe du fichier
    #         lecture_groupe = autorisations & stat.S_IRGRP != 0
    #         ecriture_groupe = autorisations & stat.S_IWGRP != 0
    #         execution_groupe = autorisations & stat.S_IXGRP != 0
    #         # Affichage des autorisations séparément pour les autres utilisateurs du fichier
    #         lecture_autres = autorisations & stat.S_IROTH != 0
    #         ecriture_autres = autorisations & stat.S_IWOTH != 0
    #         execution_autres = autorisations & stat.S_IXOTH != 0
    # =============================================================================
            
            
            
            # Récupérer les informations du propriétaire (sous Windows)
            infos_fichier = win32security.GetFileSecurity(chemin_complet, win32security.OWNER_SECURITY_INFORMATION)
            proprietaire_sid = infos_fichier.GetSecurityDescriptorOwner()
            proprietaire_nom, _, _ = win32security.LookupAccountSid(None, proprietaire_sid)
            
            # La commande icacls pour obtenir les permissions du fichier
            permissions = subprocess.run(['icacls', chemin_complet], capture_output=True, text=True)
            

            # Commande PowerShell pour obtenir les informations sur les privilèges du fichier
            powershell_command = f"Get-Acl -Path '{chemin_complet}' | Format-List"

            # Exécution de la commande PowerShell pour les informations sur les privilèges
            privileges = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
            
            
            
            # Créez un objet Magic pour accéder aux fonctionnalités de détection de type de fichier
            mime = magic.Magic()
            # Utilisez la méthode `from_file` pour déterminer le type de fichier
            file_type = mime.from_file(chemin_complet)
            #<print(file_type)
            # Système de fichiers
            #infos_fs = os.statvfs(chemin_complet)
            #type_fs = infos_fs.f_basetype
            
            empreinte_md5 = getFileMetaData.calculer_md5(chemin_complet)
            
            # Récupérer l'extension pour le type MIME spécifique
            extension_mime = getFileMetaData.types_mime_extensions.get(file_type.split(",")[0])
            #print(extension_mime)
            
            SpecificMetaData = ""
            if extension_mime is not None :
                metadata_Specific_name = getFileMetaData.return_listData_name(dict_listes, extension_mime)
                 # Vérifier si la valeur existe dans le dictionnaire et exécuter la fonction correspondante
                if extension_mime in fonctions:
                    # Specific Meta data
                    SpecificMetaData = "oui"
               
                    # Accès à la variable à partir de son nom en utilisant globals()
                    globals()[metadata_Specific_name].append(fonctions[extension_mime](chemin_complet))
                    list_metadata_Specific_name.add(metadata_Specific_name)


            # Ajoutez les métadonnées à la liste
            metadonnees.append({
                "Details": SpecificMetaData ,
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
                "Permissions": permissions,
                "Privilèges": privileges,
                # "Permissions de fichier": autorisations,
                # "Propriétaire Lecture" : lecture_proprietaire,
                # "Propriétaire Ecriture" : ecriture_proprietaire ,
                # "Propriétaire Exécution" : execution_proprietaire ,
                # "Groupe Lecture" : lecture_groupe ,
                # "Groupe Ecriture" : ecriture_groupe ,
                # "Groupe Exécution" : execution_groupe ,
                # "Autres Lecture" : lecture_autres ,
                # "Autres Ecriture" : ecriture_autres ,
                # "Autres Exécution" : execution_autres,
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
                    
    # Créez un DataFrame à partir de la liste de métadonnées
    df_metadonnees = pd.DataFrame(metadonnees)
    # Enregistrement du DataFrame dans un fichier 
    df_metadonnees.to_csv("results.csv")
    display_csv_data("results.csv", repertoire)
    
    # # Enregistrement du DataFrame dans un fichier Excel
    # nom_fichier = "Metadonnees.csv"  # Nom du fichier Excel
    # df_metadonnees.to_csv(nom_fichier)  # index=False pour ne pas inclure les index dans le fichier Excel


    print(25*'-')
    # Création de DataFrames vide
    df_metadataPDF = pd.DataFrame()
    df_metadataDOC = pd.DataFrame()
    df_metadataIMG = pd.DataFrame()
    df_metadataEXE = pd.DataFrame()
    df_metadataELF = pd.DataFrame()
    df_metadataVIDEO = pd.DataFrame()
    # Stockage des DataFrames dans un dictionnaire
    dataframes = {
        'metadataPDF': df_metadataPDF,
        'metadataDOC': df_metadataDOC,
        'metadataIMG': df_metadataIMG,
        'metadataEXE': df_metadataEXE,
        'metadataELF': df_metadataELF,
        'metadataVIDEO' : df_metadataVIDEO,
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
            # Enregistrement du DataFrame dans un fichier CSV
            dataframe.to_csv(nom_dataframe + '.csv')

    print(25*'-')



def on_click(row):
    print(row)


def on_select(event):
    selected_item = tree.selection()[0]
    item_info = tree.item(selected_item)
    print(f"Selected item: {selected_item}")
    print(f"Item info: {item_info}")
    values = tree.item(selected_item, 'values')
    print(f"Values: {values}")
    print(f"chemin à recuperer : {values[3]}")
    print(f"extension à recuperer : {values[14]}")
    if values[1] == 'oui' :
        print(f"détails : {values[1]}")
        return_specific_metadata(values[14], values[3])

def create_figure():
    # Generate some data (replace with your own data)
    df = pd.read_csv("results.csv")

    # Create a figure and plot the data
    figure = Figure(figsize=(6, 6))
    ax = figure.subplots()
    sns.countplot(data=df, x="Extension MIME", ax=ax)

    return figure

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

            line_count = 0
            for row in csv_reader:
                line_count += 1
                tree.insert("", "end", values=row)
                tree.bind("<Button-1>", lambda e, row=row:on_select(row))

            status_label.config(text=f"Le répertoire contient {line_count} fichiers enregistrés à l'emplacement : {Path().resolve()}\\results.csv")
            
            canvas = FigureCanvasTkAgg(create_figure(), master=root)
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            # root.mainloop()

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")



if __name__ == "__main__":
    main()
    

#:return_specific_metadata('.pdf', 'C:/Users/hp/Documents/MSEFC/Pentest\guide.pdf')   