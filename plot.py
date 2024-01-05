# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 00:17:10 2023

@author: hp
"""

import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')  # Set the backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd

def create_figure():
    # Generate some data (replace with your own data)
    df = pd.read_csv("Metadonnees.csv")

    # Create a figure and plot the data
    figure = Figure(figsize=(6, 6))
    ax = figure.subplots()
    sns.countplot(data=df, x="Extension MIME", ax=ax)

    return figure

def main():
    root = tk.Tk()
    canvas = FigureCanvasTkAgg(create_figure(), master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    root.mainloop()

if __name__ == "__main__":
    main()
