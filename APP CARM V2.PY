#Autor: fATON
#Date: 2021-10-20
#Version: 1.2
#Description: This is a simple app to control a PTZ camera using OpenCV and Tkinter.




import tkinter as tk, cv2 ;from PIL import Image, ImageTk
# Créer une classe pour rendre l'app plus jolie 

class Interface:
   def __init__(self, master):
        self.master = master
        self.cameras = [] 
        self.master.title("APP CARM ")
        self.master.geometry("800x600")
        self.master.resizable(0, 0)
        #self.master.iconbitmap("icon.ico")
        self.master.config(cursor="arrow")
        
class Camera:
    def __init__(self, ip_address, username="", password=""):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.cap = None
        self.out = None
    
    def connect(self):
        url = f"rtsp://{self.username}:{self.password}@{self.ip_address}/live"
        self.cap = cv2.VideoCapture(url)
    
    def start_recording(self, filename):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    def stop_recording(self):
        if self.out is not None:
            self.out.release()
            self.out = None
    
    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

class CameraAppUI:
    def __init__(self, master):
        self.master = master
        self.cameras = []
        
        # Créer un widget pour entrer l'adresse IP de la caméra
        self.ip_label = tk.Label(master, text="Adresse IP")
        self.ip_label.grid(row=0, column=0)
        self.ip_entry = tk.Entry(master)
        self.ip_entry.grid(row=0, column=1)
        
        # Créer un widget pour entrer le nom d'utilisateur de la caméra
        self.username_label = tk.Label(master, text="Nom d'utilisateur")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=1)
        
        # Créer un widget pour entrer le mot de passe de la caméra
        self.password_label = tk.Label(master, text="Mot de passe")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1)
        
        # Créer un bouton pour se connecter à la caméra
        self.connect_button = tk.Button(master, text="Connecter", command=self.connect_camera)
        self.connect_button.grid(row=3, column=0, columnspan=2)
        
        # Créer un widget pour afficher le flux en direct
        self.video_label = tk.Label(master)
        self.video_label.grid(row=4, column=0, columnspan=2)
        
        # Créer un bouton pour enregistrer la vidéo
        self.record_button = tk.Button(master, text="Enregistrer", command=self.start_recording)
        self.record_button.grid(row=5, column=0)
        
        # Créer un bouton pour arrêter l'enregistrement de la vidéo
        self.stop_button = tk.Button(master, text="Arrêter", command=self.stop_recording)
        self.stop_button.grid(row=5, column=1)
    
    def connect_camera(self):
        # Récupérer l'adresse IP, le nom d'utilisateur et le mot de passe entrés par l'utilisateur
        ip_address = self.ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Créer une nouvelle instance de la classe Camera et se connecter à la caméra
        camera = Camera(ip_address, username, password)
        camera.connect()
        self.cameras.append(camera)
        
        # Afficher le flux en direct de la caméra
        self.show_video(camera)
    
    def show_video(self, camera):
        frame = camera.get_frame()
        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.master.after(10, self.show_video, camera)
    
    def start_recording(self):
        for camera in self.cameras:
            camera.start_recording(f"camera_{self.cameras.index(camera)}.mp4")
    
    def stop_recording(self):
        for camera in self.cameras:
            camera.stop_recording()

root = tk.Tk()
app = CameraAppUI(root)
Interface = Interface(root)
root.mainloop()