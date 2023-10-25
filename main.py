import streamlit as st
import tkinter as tk
from tkinter import filedialog
import pathlib


root = tk.Tk()
root.withdraw()
file_path=""

if st.button("Click for Open Folder"):
    file_path = filedialog.askdirectory()
    st.write('You selected `%s`' % file_path)

root.mainloop()