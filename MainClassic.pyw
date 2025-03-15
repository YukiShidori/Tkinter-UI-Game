import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from cryptography.fernet import Fernet
import pathlib
import random
import threading
import time

CCount = 0
C = "Coal: "
CoalCount = C + str(CCount)
ICount = 0
I = "Iron: "
IronCount = I + str(ICount)

def generate_key():
    """Generate a key and save it to a file if it doesn't exist"""
    try:
        # Try to open the key file, if it exists
        with open('key.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        # If the key file doesn't exist, create it
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
        return key

def encrypt_data(data, key):
    """Encrypt the data using the key"""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """Decrypt the data using the key"""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

def LoadCoal():# reads how much coal is in the autosave file and then sets the variable for it
    global CCount
    global ICount
    try:
        # Generate or load the key
        key = generate_key()
        
        with open('Data.dat', 'rb') as file:
            encrypted_data = file.read()
            if encrypted_data:  # Check if file is not empty
                decrypted_data = decrypt_data(encrypted_data, key)
                CCount = int(decrypted_data.strip().split()[0])
                ICount = int(decrypted_data.strip().split()[1])
            else:
                CCount = 0
                ICount = 0
    except FileNotFoundError:
        CCount = 0
        ICount = 0
    except ValueError:
        CCount = 0
        ICount = 0
    except Exception as e:
        print(f"Error loading coal: {e}")
        CCount = 0
        ICount = 0

def MineClick2():
    global CCount
    RandCoalNum = random.randint(1, 3)
    global ICount
    RandIronNum = random.randint(1, 3)
    ICount += RandIronNum
    CCount += RandCoalNum
    print("Click Detected: C " + str(CCount) + " I " + str(ICount))
    CoalCount = C + str(CCount)
    IronCount = I + str(ICount)
    DisplayCoal.configure(text=CoalCount)
    DisplayIron.configure(text=IronCount)

def Autosave():
    while True:
        try:
            # Generate or load the key
            key = generate_key()
            
            encrypted_data = encrypt_data(str(CCount) + " " + str(ICount), key)
            with open('Data.dat', 'wb') as file:
                file.write(encrypted_data)
            print("Autosave saved at", time.strftime('%X'))
            DisplaySave = tk.Label(root, bg='#242525', fg="White", text="Saved")
            DisplaySave.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            time.sleep(1.5)
            DisplaySave.config(text=" ")
        except Exception as e:
            print(f"Error during autosave: {e}")
            DisplaySave = tk.Label(root, bg='#242525', fg="Red", text="Save Error")
            DisplaySave.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            time.sleep(1.5)
            DisplaySave.config(text=" ")
        time.sleep(1)

filepath = pathlib.Path(__file__).resolve().parent

# Generate or load encryption key
generate_key()

root = tk.Tk()
root.iconbitmap("icon.ico")
root.configure(bg='#242525')
root.title("Mine Clicker!")
root.geometry('600x600')
root.resizable(False, False)

#       Fonts
underline = font.Font(family="Helvetica", size=16, underline=True)

#       MainPlacements
DisplayCoal = tk.Label(root, bg='#242525', fg="White", text=CoalCount)
DisplayIron = tk.Label(root, bg='#242525', fg="White", text=IronCount)
message = tk.Label(root, bg='#242525', fg="White", text="Mine Clicker!", font=underline)
MineClick = tk.Button(root, bg='#154970', fg="White", text="Mine", command=MineClick2, activebackground='#154970', activeforeground='White')
MineClick.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
message.pack()
DisplayCoal.place(relx=0.05, rely=0.05, anchor=tk.NW)
DisplayIron.place(relx=0.05, rely=0.09, anchor=tk.NW)

#load saved data/create new save if not exist
LoadCoal()
CoalCount = C + str(CCount)
IronCount = I + str(ICount)
DisplayCoal.configure(text=CoalCount)
DisplayIron.configure(text=IronCount)

# start the autosave
timer_thread = threading.Thread(target=Autosave)
timer_thread.daemon = True  # makes so you can exit with the autosave on
timer_thread.start()

root.mainloop()