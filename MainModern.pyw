import customtkinter as ctk
from cryptography.fernet import Fernet
import pathlib
import random
import threading
import time

# Set CustomTkinter appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
        with open(filepath / 'key.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        # If the key file doesn't exist, create it
        key = Fernet.generate_key()
        with open(filepath / 'key.key', 'wb') as key_file:
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

def LoadCoal():
    """Reads how much coal and iron is in the autosave file and sets the variables"""
    global CCount
    global ICount
    try:
        # Generate or load the key
        key = generate_key()
        
        with open(filepath / 'Data.dat', 'rb') as file:
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
        print(f"Error loading data: {e}")
        CCount = 0
        ICount = 0

def MineClick2():
    """Handles the mine button click event"""
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
    """Automatically saves the coal and iron counts every second"""
    # Create a canvas for the save text
    SaveCanvas = ctk.CTkCanvas(root, width=100, height=20, bg="#2b2b2b", highlightthickness=0)
    SaveCanvas.place(relx=0.5, rely=0.115, anchor=ctk.CENTER)
    
    while True:
        try:
            # Generate or load the key
            key = generate_key()
            
            encrypted_data = encrypt_data(str(CCount) + " " + str(ICount), key)
            with open(filepath / 'Data.dat', 'wb') as file:
                file.write(encrypted_data)
            print("Autosave saved at", time.strftime('%X'))
            
            # Show save message
            SaveCanvas.delete("all")
            SaveCanvas.create_text(50, 9, text="Saved", fill="white", font=("Helvetica", 18))
            time.sleep(1.5)
            SaveCanvas.delete("all")
            
        except Exception as e:
            print(f"Error during autosave: {e}")
            # Show error message
            SaveCanvas.delete("all")
            SaveCanvas.create_text(50, 10, text="Save Error", fill="red", font=("Helvetica", 18))
            time.sleep(1.5)
            SaveCanvas.delete("all")
            
        time.sleep(1)

filepath = pathlib.Path(__file__).resolve().parent

# Create the main window
root = ctk.CTk()
root.iconbitmap("icon.ico")
root.title("As a child I yearn for the mines")
root.geometry('600x600')
root.resizable(False, False)

# Create custom fonts using CustomTkinter's font system
title_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold", underline=True)
coal_font = ctk.CTkFont(family="Helvetica", size=16)
iron_font = ctk.CTkFont(family="Helvetica", size=16)
button_font = ctk.CTkFont(family="Helvetica", size=16)
message_font = ctk.CTkFont(family="Helvetica", size=14)

# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Create and place the title label
message = ctk.CTkLabel(
    main_frame,
    text="Mine Clicker!",
    text_color="white",
    font=title_font
)
message.pack(pady=(0, 20))

# Create and place the resource displays
DisplayCoal = ctk.CTkLabel(
    main_frame,
    text=CoalCount,
    text_color="white",
    font=coal_font
)
DisplayCoal.place(relx=0.05, rely=0.05, anchor=ctk.NW)

DisplayIron = ctk.CTkLabel(
    main_frame,
    text=IronCount,
    text_color="white",
    font=iron_font
)
DisplayIron.place(relx=0.05, rely=0.09, anchor=ctk.NW)

# Create and place the mine button
MineClick = ctk.CTkButton(
    main_frame,
    text="Mine",
    font=button_font,
    command=MineClick2,
    width=200,
    height=50
)
MineClick.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

# Load saved data or create new save if not exist
LoadCoal()
CoalCount = C + str(CCount)
IronCount = I + str(ICount)
DisplayCoal.configure(text=CoalCount)
DisplayIron.configure(text=IronCount)

# Start the autosave thread
timer_thread = threading.Thread(target=Autosave)
timer_thread.daemon = True  # makes so you can exit with the autosave on
timer_thread.start()

root.mainloop()
