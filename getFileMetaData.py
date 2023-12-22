# getFileMetaData
# Pour extraire et afficher toutes les métadonnées d'un fichier PDF
from PyPDF2 import PdfReader
# Importez le module pillow
from PIL import Image, ExifTags
#import docx2txt
from docx import Document
# Pour utiliser PowerShell pour exécuter une commande
import subprocess 


monPdF = "C:/Users/afadi/Documents/MS EFC/intro_formation.pdf"

def extractPDFMeta(chemin_du_pdf):
    
    # Ouvrez le fichier PDF en mode lecture
    reader = PdfReader(chemin_du_pdf)

    # Récupérez et affichez les métadonnées du fichier PDF
    meta = reader.metadata
    
# =============================================================================
#     # Affichez les métadonnées du fichier PDF
#     print("Auteur:", meta.author)
#     print("Créateur:", meta.creator)
#     print("Sujet:", meta.subject)
#     print("Titre:", meta.title)
#     print("Producteur:", meta.producer)
#     print("Nombre de pages:", len(reader.pages))
# =============================================================================
    
    return {"Chemin": chemin_du_pdf ,
            "Auteur":meta.author,
            "Créateur":meta.creator,
            "Sujet": meta.subject ,
            "Titre": meta.title ,
            "Producteur": meta.producer ,
            "Nombre de pages": len(reader.pages)
            }    
    #print("Contenu de la liste :", metadataPDF)    
    
    # Vérifiez si le fichier PDF est chiffré (protégé par un mot de passe)
    #if pdf.is_encrypted:
    #    print("Le fichier PDF est chiffré et nécessite un mot de passe pour accéder aux métadonnées.")
    #else:

def extractImgMeta(chemin_de_img):

    # Chargez l'image
    img = Image.open(chemin_de_img)

    # Obtenez les métadonnées
    exif = img.getexif()

    # Convertissez les métadonnées en une forme lisible par l'homme
    for tag_id in exif:
        # Obtenez le nom du tag
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        # Obtenez la valeur du tag
        value = exif.get(tag_id)
        # Si la valeur est une séquence d'octets, décodez-la
        if isinstance(value, bytes):
            value = value.decode()
        # Imprimez le nom et la valeur du tag
        print(f"{tag:25}: {value}")
        
    # Créez un DataFrame à partir de la liste de métadonnées
    #df_metadonnees = pd.DataFrame(metadonnees)


def extractDOCXMeta(chemin_du_doc):
    try:
        doc = Document(chemin_du_doc)

        metadata = {}
        
        # Propriétés du document
        core_properties = doc.core_properties
        metadata["Titre"] = core_properties.title
        metadata["Auteur"] = core_properties.author
        metadata["Sujet"] = core_properties.subject
        metadata["Mots-clés"] = core_properties.keywords
        metadata["Dernier modifié par"] = core_properties.last_modified_by
        metadata["Créé le"] = core_properties.created
        metadata["Modifié le"] = core_properties.modified
        print("Auteur:", doc.core_properties.author)
        #print("Créateur:", core_properties.creator)
        print("Sujet:", core_properties.subject)
        print("Mots-clés", core_properties.keywords)
        print("Titre:", core_properties.title)
        #print("Producteur:", core_properties.producer)
        #print("Nombre de pages:", len(reader.pages))
        print("Créé le:", core_properties.created)
        print("Modifié le:", core_properties.modified)
        print("Dernière modification par :", core_properties.last_modified_by)
        print("Dernière impression le :", core_properties.last_printed)
        print("Type de document:", core_properties.category)
        print("Langue:", core_properties.language)
        print("Version:", core_properties.version)


        #return metadata

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées : {str(e)}")
        return []


# # Spécifiez le chemin du répertoire à parcourir
#folder_to_scan = r"C:/Users/afadi/Documents/MS EFC/_1009_UE3/TP2.docx"

# # Appelez la fonction pour extraire les métadonnées des fichiers DOCX dans le répertoire
#extractDOCXMeta(folder_to_scan)



#monPdF = "C:/Users/afadi/Documents/MS EFC/intro_formation.pdf"
#extractPDFMeta(monPdF)

#monIMG = "C:/Windows/SystemApps/MicrosoftWindows.Client.CBS_cw5n1h2txyewy/DesktopSpotlight/Assets/Images/image_3.jpg"
#extractImgMeta(monIMG)

def calculer_md5(chemin_fichier):
    
    commande_powershell = f"Get-FileHash -Algorithm MD5 -Path '{chemin_fichier}' | Select-Object -ExpandProperty Hash"
    
    process = subprocess.Popen(["powershell", "-Command", commande_powershell], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    sortie, erreur = process.communicate()
    
    if process.returncode == 0:
        empreinte_md5 = sortie.strip().decode('utf-8')
        #♣print("Empreinte MD5 du fichier :", empreinte_md5)
    else:
        empreinte_md5 = erreur.decode('utf-8')
        #print("Erreur lors du calcul du hash :", erreur.decode('utf-8'))
    return empreinte_md5


def trouver_ligne_par_valeur(df, nom_colonne, valeur):
    ligne = df[df[nom_colonne] == valeur]
    if not ligne.empty:
        return ligne.iloc[0]  # Renvoie la première ligne correspondante
    else:
        return None
