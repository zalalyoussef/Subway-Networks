import tkinter as tk
from tkinter import ttk
import subprocess

def run_script(city):
        script_name = f"{city}.py"
        subprocess.run(["python", script_name])
# Create the main window of the GUI
main_GUI = tk.Tk()
main_GUI.title("City Selector")
main_GUI.geometry("400x300")
main_GUI.minsize(400, 300)
main_GUI.config(bg="black")
style_GUI = ttk.Style()
style_GUI.theme_use('clam')
style_GUI.configure("TLabel", foreground="white", background="black", font=("Century", 12, 'normal'))
style_GUI.configure("TRadiobutton", foreground="white", background="black", font=("Century", 12, 'normal'))
style_GUI.configure("TButton", font=("Century Gothic", 12, 'normal'), background="black", foreground="white")
label = ttk.Label(main_GUI, text="Select a city:")
label.pack(pady=10)
selected_city_ = tk.StringVar()
FRANCE_cities = ["Lille", "Lyon"]
for city in FRANCE_cities:
    radio_button = ttk.Radiobutton(main_GUI, text=city, variable=selected_city_, value=city)
    radio_button.pack(anchor=tk.W, padx=20, pady=5)
select_button = ttk.Button(main_GUI, text="let's GO to find the shortest ROUTE!", command=lambda: run_script(selected_city_.get()))
select_button.pack(pady=20)
main_GUI.mainloop()
