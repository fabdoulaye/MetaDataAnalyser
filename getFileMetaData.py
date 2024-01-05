# getFileMetaData
# Pour extraire et afficher toutes les métadonnées d'un fichier PDF
from PyPDF2 import PdfReader
# Importez le module pillow
from PIL import Image #, ExifTags
#import docx2txt
from docx import Document
# Pour utiliser PowerShell pour exécuter une commande
import subprocess 
import piexif
from moviepy.editor import VideoFileClip
import pefile
from elftools.elf.elffile import ELFFile
# import getFileMetaData



# Création d'un dictionnaire pour associer les types MIME à leurs extensions
types_mime_extensions = {
    'PDF document' :'.pdf',
    'data' :'.xmet',
    'ASCII text' :'.txt',
    'Composite Document File V2 Document' :'.msi',
    'PE32 executable (console) Intel 80386' :'.exe',
    'PE32+ executable (console)' :'.exe',
    'PE32+ executable (console)' :'.exe',
    'PE32+ executable (GUI) x86-64' :'.exe',
    'PE32+ executable (console) x86-64' :'.exe',
    'PE32 executable (GUI) Intel 80386 (stripped to external PDB)' :'.exe',
    'PE32+ executable (console) x86-64 (stripped to external PDB)' :'.exe',
    'PE32 executable (DLL) (console) Intel 80386 (stripped to external PDB)' :'.dll',
    'PE32 executable (DLL) (console) Intel 80386' :'.dll',
    'PE32 executable (GUI) Intel 80386' :'.dat',
    'PE32+ executable (DLL) (GUI) x86-64' :'.dll',
    'PE32 executable (DLL) (console) Intel 80386 Mono/.Net assembly' :'.dll',
    'PE32+ executable (DLL) (console) x86-64' :'.dll',
    'Composite Document File V2 Document' :'.msi',
    'POSIX tar archive (GNU)' :'.tar',
    'POSIX tar archive':'.ova',
    'ELF 64-bit LSB executable' :'.elf',
    'RIFF (little-endian) data' :'.webp',
    'UTF-8 Unicode (with BOM) text' :'.psm1',
    '7-zip archive data' :'.7z',
    'PE32 executable (DLL) (GUI) Intel 80386' :'.dll',
    'troff or preprocessor input' :'.css',
    'Little-endian UTF-16 Unicode text' :'.txt',
    'VAX-order 68k Blit mpx/mux executable' :'.cfg',
    'ISO-8859 text' :'.log', #'.txt'
    'diff output' :'.txt',
    'UTF-8 Unicode text' :'.txt',
    'Little-endian UTF-16 Unicode text' :'.txt',
    'Non-ISO extended-ASCII text' :'.txt',
    'MS Windows HtmlHelp Data' :'.chm',
    #"cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\cases\Derni\303\250re session hp.prj' (No such file or directory)" :'.prj',
    'HTML document' :'.html',
    'SQLite 3.x database' :'.sqlite',
    'MS Windows registry file' :'.DAT',
     #'cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\cases\Exo1\skel-exercice-ms, P2\Thunderbird\TR\342\210\266 IF03 \342\210\266 erratum emploi du temps.eml' (No such file or directory)' :'.eml',
    #####'PDP-11 old overlay' :'',
    #####'empty' :'',
    'DOS executable (block device driver\377)' :'',
    '68k Blit mpx/mux executable' :'',
    'XML 1.0 document' :'.conf',
    'TrueType Font data' :'.ttf',
    #'cannot open `C:/Users/hp/Documents/MSEFC/ue7_Forensic1\X-ways\xwf210\MSEFC23\CASES\Derni\303\250re session hp.prj' (No such file or directory)' :'.prj',
    #####'SysEx File - Lexicon' :'',
    'vCalendar calendar file' :'.ics',
    'Zip archive data' :'.zip',
    'Microsoft PowerPoint 2007+' :'.pptx',
    'JPEG image data' : '.jpg',
    'Python script' : '.py',
    'OpenDocument Spreadsheet' : '.ods',
    'Microsoft Word 2007+' : '.docx',
    'WebM' : '.weba',

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

    # Vérifiez si le fichier PDF est chiffré (protégé par un mot de passe)
    #if pdf.is_encrypted:
    #    print("Le fichier PDF est chiffré et nécessite un mot de passe pour accéder aux métadonnées.")

    return {"Chemin": chemin_du_pdf ,
            "Auteur":meta.author,
            "Chiffré":reader.is_encrypted,
            "Créateur":meta.creator,
            "Sujet": meta.subject ,
            "Titre": meta.title ,
            "Producteur": meta.producer ,
            "Nombre de pages": len(reader.pages)
            }    


def extractImgMeta(chemin_de_img):
    
    # Initialiser un dictionnaire pour stocker les informations
    donnees_image = {}

    # Chargez l'image
    img = Image.open(chemin_de_img)
    donnees_image["Chemin"] = chemin_de_img
    
    # Taille de l'image
    largeur, hauteur = img.size
    donnees_image["Largeur"] = largeur
    donnees_image["Hauteur"] = hauteur

    # Résolution
    resolution = img.info.get('dpi')
    donnees_image["Résolution"] = resolution

    # Profondeur de couleur
    profondeur_couleur = img.mode
    donnees_image["ProfondeurCouleur"] = profondeur_couleur


    # Parameters:	data (bytes) – JPEG, WebP, TIFF, or Exif
    exif_dict = piexif.load(chemin_de_img)

    # Affichage des données EXIF
    # for ifd in exif_dict:
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            #print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
            tagdata = piexif.TAGS[ifd][tag]["name"]
            data = exif_dict[ifd][tag]
            # Imprimez le nom et la valeur du tag
            #print(f"{tagdata}: {data}")
            # Stocker les informations dans le dictionnaire
            donnees_image[tagdata] = data

    # Afficher les données du dictionnaire
    #print(donnees_image)
    return donnees_image
    


def extractDOCXMeta(chemin_du_doc):
    try:
        doc = Document(chemin_du_doc)

        metadata = {}
        metadata['Chemin'] = chemin_du_doc
        
        # Propriétés du document
        core_properties = doc.core_properties
        metadata["Titre"] = core_properties.title
        metadata["Auteur"] = core_properties.author
        metadata["Sujet"] = core_properties.subject
        metadata["Mots-clés"] = core_properties.keywords
        metadata["Dernier modifié par"] = core_properties.last_modified_by
        metadata["Créé le"] = core_properties.created
        metadata["Modifié le"] = core_properties.modified
        # print("Auteur:", doc.core_properties.author)
        # #print("Créateur:", core_properties.creator)
        # print("Sujet:", core_properties.subject)
        # print("Mots-clés", core_properties.keywords)
        # print("Titre:", core_properties.title)
        #print("Producteur:", core_properties.producer)
        #print("Nombre de pages:", len(reader.pages))
        # print("Créé le:", core_properties.created)
        # print("Modifié le:", core_properties.modified)
        metadata["Dernière modification par"] = core_properties.last_modified_by
        metadata["Dernière impression le"] = core_properties.last_printed
        metadata["Type de document"] = core_properties.category
        metadata["Langue"] = core_properties.language
        metadata["Version"] = core_properties.version


        return metadata

    except Exception as e:
        #print(f"Erreur lors de l'extraction des métadonnées : {str(e)}")
        metadata["Erreur lors de l'extraction des métadonnées"] = str(e)
        return metadata



def calculer_md5(chemin_fichier):
    
    commande_powershell = f"Get-FileHash -Algorithm MD5 -Path '{chemin_fichier}' | Select-Object -ExpandProperty Hash"
    
    process = subprocess.Popen(["powershell", "-Command", commande_powershell], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    sortie, erreur = process.communicate()
    
    if process.returncode == 0:
        empreinte_md5 = sortie.strip().decode('utf-8')
        #♣print("Empreinte MD5 du fichier :", empreinte_md5)
    else:
        empreinte_md5 = erreur.decode('utf-16')
        #print("Erreur lors du calcul du hash :", erreur.decode('utf-8'))
    return empreinte_md5


def trouver_ligne_par_valeur(df, valeur):
    
   
    ligne = df[df['Chemin'] == valeur]
    if not ligne.empty:
        return ligne.iloc[0]  # Renvoie la première ligne correspondante
    else:
        return None


def extract_image(video_path, time):
    clip = VideoFileClip(video_path)
    # Obtient l'image à un temps spécifique (en secondes)
    # Amélioration : nommer l'image en reprenant le nom de la viseo et en ajoutant ses secondes
    # Sauvegarde l'image extraite
    clip.save_frame("frame.png", t=time) # saves the frame a t=2s

    
def cut_video_segment(video_path, start_time, end_time):
    

    clip = VideoFileClip(video_path)
    segment = clip.subclip(start_time, end_time)  # Coupe un segment spécifique
    segment.write_videofile("segment_cut.mp4")  # Enregistre le segment coupé
    
    
def extractEXEMeta(exe_path):
    # Chargement du fichier PE
    pe = pefile.PE(exe_path)
    #print(pe.dump_info())
    
    # Initialiser un dictionnaire pour stocker les informations
    metadatExe = {}
    metadatExe["Chemin"] = exe_path

    # Récupérer le point d'entrée (adresse) du programme
    entry_point = pe.OPTIONAL_HEADER. AddressOfEntryPoint
    print(f"Point d'entrée du programme : {hex(entry_point)}")
    metadatExe["Point d'entrée du programme"] = hex(entry_point)

    # Affichage des informations de l'en-tête
    #print("Adresse d'entrée du programme: 0x%x" % pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    #print("Liste des sections:")
    # for section in pe.sections:
    #     print(section.Name.decode().strip('\x00').decode(), hex(section.VirtualAddress), hex(section.Misc_VirtualSize))
    # Parcourir et afficher les sections
    print("Liste des sections :")
    for section in pe.sections:
        # print(section.Name.decode().strip('\x00'))
        # print(hex(section.VirtualAddress), hex(section.Misc_VirtualSize))
        metadatExe[section.Name.decode().strip('\x00')] = hex(section.VirtualAddress) + hex(section.Misc_VirtualSize)


    # Accéder à d'autres parties des métadonnées si nécessaire, par exemple :
    print("Liste des imports:")
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        # print(entry.dll)
        entrImports = ""
        for imp in entry.imports:
            # print('\t', hex(imp.address), imp.name.decode())
            entrImports += '\t' + hex(imp.address) + imp.name.decode()
        metadatExe[entry.dll] = entrImports
            
            
    # Récupérer les symboles exportés
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        export_symbols = pe.DIRECTORY_ENTRY_EXPORT.symbols
        symbolExport = ""
        # print("Symboles exportés :")
        for symbol in export_symbols:
            # Décoder le nom du symbole en UTF-8
            #print(symbol.name.decode('utf-8', 'ignore')) 
            symbolExport += symbol.name.decode('utf-8', 'ignore')
            
    else:
        # print("Aucun symbole exporté trouvé.")
        metadatExe["Symboles exportés"] = "Aucun symbole exporté trouvé."

    # Fermer le fichier PE
    pe.close()
    
    return metadatExe

# Chemin vers le fichier exécutable
def extractELFMeta(elf_file_path):
    
    # Initialiser un dictionnaire pour stocker les informations
    metadatELF = {}
    metadatELF["Chemin"] = elf_file_path
    
    with open(elf_file_path , 'rb') as f:
        elf_file  = ELFFile(f)
        #print(elf_file.header)
        
        # Get the ELF header
        elf_header = elf_file.header        
        metadatELF["Point d'entrée du programme"] = elf_header
        # Extract the entry point
        entry_point = elf_header['e_entry']
        # print(f"Entry point: {entry_point:#x}")
        metadatELF["Point d'entrée du programme"] = entry_point
        
        # Iterate through the sections
        lessections = ""
        for section in elf_file.iter_sections():
           # print(f"Section name: {section.name}, Section type: {section['sh_type']}")
           lessections = lessections + f"Section name: {section.name}, Section type: {section['sh_type']}\n"
        metadatELF["Sections"] = lessections
           
        # Access program headers
        lessegments = ""
        for segment in elf_file.iter_segments():
            # print(f"Segment type: {segment['p_type']}, Virtual address: {segment['p_vaddr']}")
            lessegments = lessegments + f"Segment type: {segment['p_type']}, Virtual address: {segment['p_vaddr']}\n"
        metadatELF["Segments"] = segment['p_vaddr']
            
        # Check if ELF file has a dynamic symbol table = prints out the imported libraries.
        if elf_file.has_dwarf_info():
            importedLib = ""
            dwarf_info = elf_file.get_dwarf_info()
            for CU in dwarf_info.iter_CUs():
                # Check the existence of .dynamic section
                for die in CU.iter_DIEs():
                    if die.tag == 'DW_TAG_dynamic':
                        # Iterate through dynamic symbols for imports
                        dynamic = elf_file.get_section_by_name('.dynamic')
                        for tag in dynamic.iter_tags():
                            if tag.entry.d_tag == 'DT_NEEDED':
                                library_name = tag.elffile.get_string(tag.entry.d_val)
                                # print(f"Imported library: {library_name.decode('utf-8')}")
                                importedLib = importedLib + f"Imported library: {library_name.decode('utf-8')}\n"
            metadatELF["imported libraries"] = importedLib
                                
        # Check if ELF file has a symbol table
        if elf_file.has_dwarf_info():
            exportedSymbols = ""
            dwarf_info = elf_file.get_dwarf_info()
            for CU in dwarf_info.iter_CUs():
                # Check the existence of the .symtab section
                for die in CU.iter_DIEs():
                    if die.tag == 'DW_TAG_compile_unit':
                        # Iterate through the symbol table for exported symbols
                        symtab = elf_file.get_section_by_name('.symtab')
                        if symtab:
                            for symbol in symtab.iter_symbols():
                                if symbol['st_info']['type'] != 'STT_FUNC':
                                    continue
                                symbol_name = symbol.name.decode('utf-8')
                                print(f"Exported symbol: {symbol_name}")
                                exportedSymbols = exportedSymbols + f"Exported symbol: {symbol_name}\n"
            metadatELF["Exported Symbols"] = exportedSymbols
            
        
    return metadatELF

def extractVIDEOMeta(file_path):
    
    clip = VideoFileClip(file_path)
    duration = clip.duration  # Durée de la vidéo en secondes
    resolution = clip.size  # Résolution de la vidéo (largeur, hauteur)
    fps = clip.fps  # Images par seconde (FPS)
    
    return {
        "duration": duration,
        "resolution": resolution,
        "fps": fps
    }

