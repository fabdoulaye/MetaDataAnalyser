# getFileMetaData
# Pour extraire et afficher toutes les métadonnées d'un fichier PDF
from PyPDF2 import PdfReader
# Importez le module pillow
from PIL import Image, ExifTags
import docx2txt
import os


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




# requirement : pip install doc2txt
def extractDOCmetadata(file_path):
    # Créez une liste pour stocker les métadonnées de tous les fichiers DOCX
    all_metadata = []

    try:
        # """ # Parcourez le répertoire spécifié
        # for root, dirs, files in os.walk(folder_path):
        #     for file in files:
        #         if file.lower().endswith(".docx"):  # Vérifiez si le fichier est un DOCX
        #             file_path = os.path.join(root, file) """

        # Utilisez la bibliothèque docx2txt pour extraire les métadonnées
        doc_data = docx2txt.process(file_path)

        # Extrait les métadonnées du document Word
        metadata = {}
        if "title" in doc_data:
            metadata["Titre"] = doc_data["title"]
        else:
            metadata["Titre"] = "N/A"
        if "created" in doc_data:
            metadata["Date de Création"] = doc_data["created"]
        else:
            metadata["Date de Création"] = "N/A"
        if "modified" in doc_data:
            metadata["Date de Modification"] = doc_data["modified"]
        else:
            metadata["Date de Modification"] = "N/A"
        if "author" in doc_data:
            metadata["Propriétaire"] = doc_data["author"]
        else:
            metadata["Propriétaire"] = "N/A"
            metadata["Nom du Document"] = os.path.basename(file_path)
            metadata["Type de Document"] = "Microsoft Word (.docx)"
            metadata["Taille du Document"] = os.path.getsize(file_path)
            metadata["Nom de l'Ordinateur"] = platform.node()

        # entrer le code pour les autres fichiers ici

        all_metadata.append(metadata)

        # Affichez les métadonnées extraites pour chaque fichier
        for metadata in all_metadata:
            print("Métadonnées du fichier :")
            for key, value in metadata.items():
                print(f"{key}: {value}")
            print("\n")

        return all_metadata

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées : {str(e)}")
        return []

# # Spécifiez le chemin du répertoire à parcourir
folder_to_scan = "C:/Users/afadi/Documents/MS EFC/_1009_UE3_/TP2.docx"

# # Appelez la fonction pour extraire les métadonnées des fichiers DOCX dans le répertoire
metadata_list = extractDOCmetadata(folder_to_scan)


    # # Affichez les métadonnées extraites pour chaque fichier
    # for metadata in metadata_list:
    #     print("Métadonnées du fichier :")
    #     for key, value in metadata.items():
    #         print(f"{key}: {value}")
    #     print("\n")

#monPdF = "C:/Users/afadi/Documents/MS EFC/intro_formation.pdf"
#extractPDFMeta(monPdF)

#monIMG = "C:/Windows/SystemApps/MicrosoftWindows.Client.CBS_cw5n1h2txyewy/DesktopSpotlight/Assets/Images/image_3.jpg"
#extractImgMeta(monIMG)
