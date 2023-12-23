# getFileMetaData
# Pour extraire et afficher toutes les métadonnées d'un fichier PDF
from PyPDF2 import PdfReader
# Importez le module pillow
from PIL import Image, ExifTags
#import docx2txt
from docx import Document
# Pour utiliser PowerShell pour exécuter une commande
import subprocess 
import pandas as pd


monPdF = "C:/Users/afadi/Documents/MS EFC/intro_formation.pdf"

# Création d'un dictionnaire pour associer les types MIME à leurs extensions
types_mime_extensions = {
    'PDF document, version 1.7' :'.pdf',
    'PDF document, version 1.6' :'.pdf',
    'block special' :'.e01',
    'data' :'.xmet',
    'Composite Document File V2 Document, Little Endian, Os: Windows, Version 6.2, MSI Installer, Title: Installation Database, Subject: Python 2.7.18 (64-bit), Author: Python Software Foundation, Template: x64;1033, Revision Number: {1514A29B-ECBA-42BF-9A36-476BC87C7EC6}, Number of Words: 2, Number of Pages: 200, Name of Creating Application: Python MSI Library' :'.msi',
    'PE32 executable (console) Intel 80386, for MS Windows' :'.exe',
    'ASCII text, with very long lines, with CRLF line terminators' :'.txt',
    'PE32+ executable (console) x86-64, for MS Windows' :'.exe',
    'Composite Document File V2 Document, Little Endian, Os: Windows, Version 6.3, MSI Installer, Code page: 1252, Title: Installation Database, Subject: Microsoft Visual C++ Compiler Package for Python 2.7, Author: Microsoft Corporation, Keywords: Installer, Comments: This installer database contains the logic and data required to install Microsoft Visual C++ Compiler Package for Python 2.7., Template: Intel;1033, Revision Number: {7602330B-3527-4E2F-A4D7-A1E7BCA878F8}, Create Time/Date: Mon Sep 29 16:48:02 2014, Last Saved Time/Date: Mon Sep 29 16:48:02 2014, Number of Pages: 300, Number of Words: 10, Name of Creating Application: Windows Installer XML Toolset (3.8.1128.0), Security: 2' :'.msi',
    'PE32 executable (GUI) Intel 80386 (stripped to external PDB), for MS Windows, Nullsoft Installer self-extracting archive' :'.exe',
    'POSIX tar archive (GNU)' :'.tar',
    'POSIX tar archive':'.ova',
    'ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=b0d7a6bd600fe406c5699892feb171baeb93de79, not stripped' :'',
    'ASCII text, with very long lines' :'.md',
    'UTF-8 Unicode (with BOM) text, with CRLF line terminators' :'.psm1',
    'ASCII text, with CRLF line terminators' :'.ps1',
    'ASCII text' :'.txt',
    'PE32+ executable (console), for MS Windows' :'.exe',
    '7-zip archive data, version 0.4' :'.7z',
    'ISO-8859 text, with CRLF line terminators' :'.txt',
    'PE32 executable (DLL) (GUI) Intel 80386, for MS Windows' :'.dll',
    'troff or preprocessor input, ASCII text, with CRLF line terminators' :'.css',
    'Little-endian UTF-16 Unicode text' :'.txt',
    'VAX-order 68k Blit mpx/mux executable' :'.cfg',
    'PE32 executable (DLL) (console) Intel 80386 (stripped to external PDB), for MS Windows' :'.dll',
    'PE32 executable (DLL) (console) Intel 80386, for MS Windows' :'.dll',
    'PE32 executable (GUI) Intel 80386, for MS Windows' :'.dat',
    'PE32 executable (GUI) Intel 80386, for MS Windows, Nullsoft Installer self-extracting archive' :'.exe',
    'ISO-8859 text, with very long lines, with CRLF line terminators' :'.log',
    'diff output, ASCII text, with CRLF line terminators' :'.txt',
    'UTF-8 Unicode text, with CRLF line terminators' :'.txt',
    'Little-endian UTF-16 Unicode text, with no line terminators' :'.txt',
    'Little-endian UTF-16 Unicode text, with very long lines, with CRLF line terminators' :'.txt',
    'Little-endian UTF-16 Unicode text, with CRLF line terminators' :'.txt',
    'UTF-8 Unicode (with BOM) text, with very long lines, with CRLF line terminators' :'.txt',
    'Little-endian UTF-16 Unicode text, with CRLF, CR line terminators' :'.txt',
    'ASCII text, with no line terminators' :'.txt',
    'Little-endian UTF-16 Unicode text, with very long lines' :'.txt',
    'Non-ISO extended-ASCII text, with CRLF line terminators' :'.txt',
    'MS Windows HtmlHelp Data' :'.chm',
    'PE32+ executable (GUI) x86-64, for MS Windows' :'.exe',
    #"cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\cases\Derni\303\250re session hp.prj' (No such file or directory)" :'.prj',
    'HTML document, ISO-8859 text, with CRLF line terminators' :'.html',
    'SQLite 3.x database, last written using SQLite version 3008007' :'',
    'SQLite 3.x database, user version 25, last written using SQLite version 3008007' :'.sqlite',
    'HTML document, UTF-8 Unicode text, with very long lines, with CRLF line terminators' :'.html',
    'MS Windows registry file, NT/2000 or above' :'.DAT',
     #'cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\cases\Exo1\skel-exercice-ms, P2\Thunderbird\TR\342\210\266 IF03 \342\210\266 erratum emploi du temps.eml' (No such file or directory)' :'.eml',
    'PDP-11 old overlay' :'',
    'empty' :'',
    'HTML document, Non-ISO extended-ASCII text, with very long lines, with CRLF, CR, NEL line terminators' :'.html',
    'SQLite 3.x database, last written using SQLite version 3030001' :'',
    'DOS executable (block device driver\377)' :'',
    '68k Blit mpx/mux executable' :'',
    'PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows' :'.exe',
    'HTML document, UTF-8 Unicode text, with very long lines' :'.html',
    'HTML document, ASCII text' :'.html',
    'XML 1.0 document, ASCII text' :'.conf',
    'XML 1.0 document, UTF-8 Unicode text' :'.conf',
    'TrueType Font data, 19 tables, 1st "FFTM", 26 names, Macintosh' :'.ttf',
    #'cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\MSEFC23\CASES\Derni\303\250re session hp.prj' (No such file or directory)' :'.prj',
    'SysEx File - Lexicon' :'',
    'PE32+ executable (DLL) (GUI) x86-64, for MS Windows' :'.dll',
    'SQLite 3.x database, last written using SQLite version 3008005' :'',
    'SQLite 3.x database, last written using SQLite version 0' :'.db',
    'PE32 executable (DLL) (console) Intel 80386 Mono/.Net assembly, for MS Windows' :'.dll',
    'PE32+ executable (DLL) (console) x86-64, for MS Windows' :'.dll',
    'vCalendar calendar file' :'.ics',
    'Zip archive data, at least v2.0 to extract' :'.zip',
    'Microsoft PowerPoint 2007+' :'.pptx',

    # Ajoutez d'autres correspondances selon les besoins
}

def return_listData_name(dictionnaire, extension_recherchee):
    # extension_recherchee = Extension que vous cherchez à trouver dans les tuples de clé
    
    nom_liste_trouvee = None
    
    # Parcours du dictionnaire pour trouver la liste associée à l'extension spécifique
    for extensions, nom_liste in dictionnaire.items():
        if extension_recherchee in extensions:
            nom_liste_trouvee = nom_liste
            break  # Arrêter la recherche dès qu'on trouve la correspondance
    
    # if nom_liste_trouvee is not None:
    #     print(f"Le nom de la liste pour l'extension '{extension_recherchee}' est : {nom_liste_trouvee}")
    # else:
    
    #     print(f"Aucune liste trouvée pour l'extension '{extension_recherchee}'")
    
    return nom_liste_trouvee


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


def trouver_ligne_par_valeur(df, valeur):
    
   
    ligne = df[df['Chemin'] == valeur]
    if not ligne.empty:
        return ligne.iloc[0]  # Renvoie la première ligne correspondante
    else:
        return None
