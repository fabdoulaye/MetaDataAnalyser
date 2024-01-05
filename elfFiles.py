# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 20:44:27 2023

@author: hp
"""

from elftools.elf.elffile import ELFFile

# Chemin vers le fichier exécutable
elf_file_path  = 'C:/Users/hp/Documents/MSEFC/ue7_Forensic1/RAM/Dump-tools/Comae-Linux/DumpIt'

with open(elf_file_path , 'rb') as f:
    elf_file  = ELFFile(f)
    print(elf_file.header)
    
    # Get the ELF header
    elf_header = elf_file.header
    # Extract the entry point
    entry_point = elf_header['e_entry']
    print(f"Entry point: {entry_point:#x}")
    
    # Iterate through the sections
    for section in elf_file.iter_sections():
       print(f"Section name: {section.name}, Section type: {section['sh_type']}")
       
    # Access program headers
    for segment in elf_file.iter_segments():
        print(f"Segment type: {segment['p_type']}, Virtual address: {segment['p_vaddr']}")
        
    # Check if ELF file has a dynamic symbol table = prints out the imported libraries.
    if elf_file.has_dwarf_info():
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
                            print(f"Imported library: {library_name.decode('utf-8')}")
                            
    # Check if ELF file has a symbol table
    if elf_file.has_dwarf_info():
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