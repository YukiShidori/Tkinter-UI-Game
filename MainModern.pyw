import customtkinter as ctk
from cryptography.fernet import Fernet
import pathlib
import random
import threading
import time

class MineClicker:
    def __init__(self):
        """Initialize the game"""
        self.filepath = pathlib.Path(__file__).resolve().parent
        self.resources = {
            'coal': 0,
            'iron': 0,
            'diamond': 0
        }
        self.multipliers = {
            'coal': 1,
            'iron': 1,
            'diamond': 1
        }
        self.resource_labels = {}
        
        # Initialize encryption
        self.key = self.generate_key()
        
        # Create main window
        self.root = self.setup_window()
        
        # Create UI elements
        self.setup_ui()
        
        # Load saved data
        self.load_data()
        
        # Start autosave
        self.start_autosave()
        
        # Start main loop
        self.root.mainloop()

    def setup_window(self):
        """Create and configure the main window"""
        root = ctk.CTk()
        root.iconbitmap("icon.ico")
        root.configure(bg_color='#242525')
        root.title("Mine Clicker!")
        root.geometry('600x600')
        root.resizable(False, False)
        return root

    def setup_ui(self):
        """Create all UI elements"""
        # Create fonts
        self.title_font = ctk.CTkFont(family="Helvetica", size=20, underline=True, weight="bold")
        self.resource_font = ctk.CTkFont(family="Helvetica", size=16)
        self.button_font = ctk.CTkFont(family="Helvetica", size=14)

        # Create title
        message = ctk.CTkLabel(
            self.root,
            bg_color='#242525',
            text_color="White",
            text="Mine Clicker!",
            font=self.title_font
        )
        message.pack()

        # Create resource displays
        self.resource_labels['coal'] = ctk.CTkLabel(
            self.root,
            bg_color='#242525',
            text_color="White",
            text="Coal: 0",
            font=self.resource_font
        )
        self.resource_labels['coal'].place(relx=0.05, rely=0.05, anchor=ctk.NW)

        self.resource_labels['iron'] = ctk.CTkLabel(
            self.root,
            bg_color='#242525',
            text_color="White",
            text="Iron: 0",
            font=self.resource_font
        )
        self.resource_labels['iron'].place(relx=0.05, rely=0.09, anchor=ctk.NW)

        self.resource_labels['diamond'] = ctk.CTkLabel(
            self.root,
            bg_color='#242525',
            text_color="White",
            text="Diamond: 0",
            font=self.resource_font
        )
        self.resource_labels['diamond'].place(relx=0.05, rely=0.13, anchor=ctk.NW)

        # Create mine button
        mine_button = ctk.CTkButton(
            self.root,
            fg_color='#154970',
            text_color="White",
            text="Mine",
            command=self.mine_click,
            hover_color='#154970',
            font=self.button_font
        )
        mine_button.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # Create shop button
        shop_button = ctk.CTkButton(
            self.root,
            fg_color='#154970',
            text_color="White",
            text="Shop",
            command=self.shop_click,
            hover_color='#154970',
            font=self.button_font
        )
        shop_button.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

    def shop_click(self):
        """Handle shop button click"""
        print("Shop clicked")
        self.shop_window()

    def shop_window(self):
        """Create shop window"""
        shop_window = ctk.CTkToplevel(self.root)
        shop_window.title("Shop")
        shop_window.geometry('400x300')
        shop_window.resizable(False, False)
        shop_window.configure(bg_color='#242525')

        # Create shop items with better organization
        self.shop_items = [
            {'name': 'Coal Multiplier', 'price': 10, 'resource': 'coal', 'multiplier': 1, 'type': 'multiplier', 'current': self.multipliers['coal']},
            {'name': 'Iron Multiplier', 'price': 20, 'resource': 'iron', 'multiplier': 1, 'type': 'multiplier', 'current': self.multipliers['iron']},
            {'name': 'Diamond Multiplier', 'price': 30, 'resource': 'diamond', 'multiplier': 1, 'type': 'multiplier', 'current': self.multipliers['diamond']}
        ]

        # Create shop item labels and buttons
        self.item_labels = []
        for i, item in enumerate(self.shop_items):
            # Create item label
            label = ctk.CTkLabel(
                shop_window,
                bg_color='#242525',
                text_color="White",
                text=f"{item['name']} x{item['current']}: {item['price']} {item['resource'].capitalize()}",
                font=self.resource_font
            )
            label.place(relx=0.1, rely=0.1 + 0.1*i, anchor=ctk.W)
            self.item_labels.append(label)

            # Create buy button
            button = ctk.CTkButton(
                shop_window,
                fg_color='#154970',
                text_color="White",
                text="Buy",
                command=lambda item=item, index=i: self.buy_item(item, shop_window, index),
                hover_color='#154970',
                font=self.button_font
            )
            button.place(relx=0.9, rely=0.1 + 0.1*i, anchor=ctk.E)

        # Create close button
        close_button = ctk.CTkButton(
            shop_window,
            fg_color='#154970',
            text_color="White",
            text="Close",
            command=shop_window.destroy,
            hover_color='#154970',
            font=self.button_font
        )
        close_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

    def buy_item(self, item, shop_window, index):
        """Handle item purchase"""
        # Check if player has enough resources
        if self.resources[item['resource']] >= item['price']:
            # Deduct price
            self.resources[item['resource']] -= item['price']
            
            # Update item based on type
            if item['type'] == 'multiplier':
                self.multipliers[item['resource']] += item['multiplier']
                item['current'] = self.multipliers[item['resource']]
            
            # Update display
            self.update_display()
            
            # Update specific item label
            self.item_labels[index].configure(text=f"{item['name']} x{item['current']}: {item['price']} {item['resource'].capitalize()}")
            
            # Save data
            self.save_data()
        else:
            # Show insufficient resources message
            ctk.CTkMessagebox(title="Error", message=f"Not enough {item['resource']}!")

    def generate_key(self):
        """Generate or load encryption key"""
        try:
            with open(self.filepath / 'key.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.filepath / 'key.key', 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt_data(self, data, key):
        """Encrypt the data using the key"""
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data, key):
        """Decrypt the data using the key"""
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode()

    def save_data(self):
        """Save game data"""
        try:
            key = self.generate_key()
            # Save resources and multipliers
            data = f"{self.resources['coal']} {self.resources['iron']} {self.resources['diamond']} "
            data += f"{self.multipliers['coal']} {self.multipliers['iron']} {self.multipliers['diamond']}"
            encrypted_data = self.encrypt_data(data, key)
            with open(self.filepath / 'Data.dat', 'wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """Load saved game data"""
        try:
            key = self.generate_key()
            with open(self.filepath / 'Data.dat', 'rb') as file:
                encrypted_data = file.read()
                if encrypted_data:
                    decrypted_data = self.decrypt_data(encrypted_data, key)
                    data = decrypted_data.strip().split()
                    # Load resources
                    self.resources['coal'] = int(data[0])
                    self.resources['iron'] = int(data[1])
                    self.resources['diamond'] = int(data[2])
                    # Load multipliers
                    self.multipliers['coal'] = int(data[3])
                    self.multipliers['iron'] = int(data[4])
                    self.multipliers['diamond'] = int(data[5])
        except Exception as e:
            print(f"Error loading data: {e}")
            self.resources = {'coal': 0, 'iron': 0, 'diamond': 0}
            self.multipliers = {'coal': 1, 'iron': 1, 'diamond': 1}

    def mine_click(self):
        """Handle mine button click"""
        # Generate resources with multipliers
        self.resources['coal'] += random.randint(1, 3) * self.multipliers['coal']
        IronChance = random.randint(1, 100)
        if IronChance >= 35:
            self.resources['iron'] += 1 * self.multipliers['iron']
        DiamondChance = random.randint(1, 100)
        if DiamondChance >= 95:
            self.resources['diamond'] += 1 * self.multipliers['diamond']
        self.update_display()

    def update_display(self):
        """Update resource display labels"""
        for resource, label in self.resource_labels.items():
            label.configure(text=f"{resource.capitalize()}: {self.resources[resource]}")

    def start_autosave(self):
        """Start autosave thread"""
        threading.Thread(target=self.autosave, daemon=True).start()

    def autosave(self):
        """Autosave game data every 30 seconds"""
        while True:
            try:
                key = self.generate_key()
                data = f"{self.resources['coal']} {self.resources['iron']} {self.resources['diamond']} "
                data += f"{self.multipliers['coal']} {self.multipliers['iron']} {self.multipliers['diamond']}"
                encrypted_data = self.encrypt_data(data, key)
                with open(self.filepath / 'Data.dat', 'wb') as file:
                    file.write(encrypted_data)
            except Exception as e:
                print(f"Error autosaving data: {e}")
            time.sleep(30)

# Create and run the game
if __name__ == "__main__":
    # Set CustomTkinter appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    game = MineClicker()
