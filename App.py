from tkinter import *
from tkinter import ttk, simpledialog
from tkinter import messagebox
import DataBase
import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime
import time

departmentManager = {30, 29, 28, 27, 26}


class Ordinaryworkertkinter:

    def __init__(self, encodeListKnown, user_id):
        self.user_id = user_id
        self.log_in_window = LogIn()

    def change(self, find_by, user_df, main_window):
        try:
            ordinary_worker = DataBase.OrdinaryWorker()
            surname_to_search = simpledialog.askstring("Пошук", "Введіть прізвище, за яким можна знайти працівника:")
            if surname_to_search is None:
                raise
            matching_rows = ordinary_worker.data[ordinary_worker.data['Surname'] == surname_to_search]

            if surname_to_search in ordinary_worker.data["Surname"].values and surname_to_search in user_df["Surname"].values:
                match find_by:
                    case 'Name':
                        found_name = matching_rows.iloc[0]['Name']
                        new_name = simpledialog.askstring("Заміна", "Старе ім'я {} Введіть нове ім'я працівника:".format(found_name))
                        if new_name is None:
                            raise
                        ordinary_worker.setName(surname_to_search, new_name)
                    case 'Salary':
                        found_salary = matching_rows.iloc[0]['Salary']
                        new_salary = simpledialog.askstring("Заміна", "Стара заробітня плата: {} грн. Введіть нову зарплату для працівника (числом):".format(found_salary))
                        if new_salary is None:
                            raise
                        try:
                            new_salary = float(new_salary)
                            if new_salary <= 0:
                                messagebox.showinfo(
                                    message="Зарплата має бути більше 0, пожалійте працівника, йому ж сімʼю кормити)")
                                raise
                            ordinary_worker.setSalary(surname_to_search, new_salary)
                        except ValueError:
                            messagebox.showinfo(message="Введене значення не є числом.")
                    case 'Rating':
                        found_rating = matching_rows.iloc[0]['Rating']
                        new_rating = simpledialog.askstring("Заміна", "Старий рейтинг: {}.Введіть новий рейтинг працівника(від 0 до 5):".format(found_rating))
                        if new_rating is None:
                            raise
                        if "." in new_rating:
                            new_rating = new_rating.replace('.', ',')
                        try:
                            new_rating = float(new_rating)
                            if 5 >= new_rating >= 0:
                                ordinary_worker.setRating(surname_to_search, new_rating)
                            else:
                                messagebox.showinfo(message="Введене значення не є числом від 0 до 5.")
                        except ValueError:
                            messagebox.showinfo(message="Введене значення не є числом від 0 до 5.")
            else:
                messagebox.showinfo(message="Прізвище {} не знайдено в, доступній вам, базі данних, вводити потрібно коректне прізвище працівника.".format(surname_to_search))
        except ValueError:
            pass
        main_window.destroy()
        Ordinaryworkertkinter.mainWindow(self)

    def mainWindow(self):
        def main_back():
            main_window.destroy()
            log_in_window.logInWindowShow(encodeListKnown)

        main_window = Tk()
        ordinary_worker = DataBase.OrdinaryWorker()

        main_window.grid_columnconfigure(0, minsize=200)
        main_window.grid_columnconfigure(1, minsize=710)
        main_window.grid_columnconfigure(3, minsize=120)

        main_window.grid_rowconfigure(0, minsize=50)
        main_window.grid_rowconfigure(1, minsize=150)
        main_window.grid_rowconfigure(2, minsize=150)
        main_window.grid_rowconfigure(3, minsize=150)
        main_window.grid_rowconfigure(4, minsize=50)

        main_window.title("DataBase")

        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()

        x = (screen_width - 1200) // 2
        y = (screen_height - 700) // 2

        main_window.geometry('{}x{}+{}+{}'.format(1200, 700, x, y))
        main_window.resizable(width=False, height=False)

        new_font = ('Helvetica', 25)

        skip = Label(main_window, text='')
        skip.grid(row=4, column=0)

        button = Button(main_window, text="Exit", font=new_font, command=exit)
        button.grid(row=5, column=3)
        button = Button(main_window, text="Back", font=new_font, command=main_back)
        button.grid(row=5, column=2)

        tree = ttk.Treeview(main_window, columns=list(ordinary_worker.data.columns), show="headings")

        for col in ordinary_worker.data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        if self.user_id == 31:
            for i, row in ordinary_worker.data.iterrows():
                tree.insert("", "end", values=list(row))

            label1 = Label(main_window, font=new_font, text="Change")
            label1.grid(row=0, column=0)

            button = Button(main_window, text="Name", font=new_font,
                            command=lambda: self.change("Name", ordinary_worker.data, main_window))
            button.grid(row=1, column=0)
            button = Button(main_window, text="Salary", font=new_font,
                            command=lambda: self.change("Salary", ordinary_worker.data, main_window))
            button.grid(row=2, column=0)
            button = Button(main_window, text="Rating", font=new_font,
                            command=lambda: self.change("Rating", ordinary_worker.data, main_window))
            button.grid(row=3, column=0)

            tree.grid(row=1, column=1, columnspan=3, rowspan=3, stick='wens')

        elif self.user_id in departmentManager:

            label = Label(main_window, font=new_font, text="Change")
            label.grid(row=0, column=0)

            button = Button(main_window, text="Name", font=new_font,
                            command=lambda: self.change("Name", managers_df, main_window))
            button.grid(row=1, column=0)
            button = Button(main_window, text="Salary", font=new_font,
                            command=lambda: self.change("Salary", managers_df, main_window))
            button.grid(row=2, column=0)
            button = Button(main_window, text="Rating", font=new_font,
                            command=lambda: self.change("Rating", managers_df, main_window))
            button.grid(row=3, column=0)

            tree.insert("", "end", values=list(ordinary_worker.data.iloc[self.user_id]))
            match self.user_id:
                case 26:
                    num = 0
                    managers_df = ordinary_worker.data.iloc[[0, 1, 2, 3, 4]]
                    for i in range(5):
                        tree.insert("", "end", values=list(ordinary_worker.data.iloc[num]))
                        num = num + 1
                case 27:
                    num = 5
                    managers_df = ordinary_worker.data.iloc[[5, 6, 7, 8, 9]]
                    for i in range(5):
                        tree.insert("", "end", values=list(ordinary_worker.data.iloc[num]))
                        num = num + 1

                case 28:
                    num = 10
                    managers_df = ordinary_worker.data.iloc[[10, 11, 12, 13, 14]]
                    for i in range(5):
                        tree.insert("", "end", values=list(ordinary_worker.data.iloc[num]))
                        num = num + 1
                case 29:
                    num = 15
                    managers_df = ordinary_worker.data.iloc[[15, 16, 17, 18, 19]]
                    for i in range(5):
                        tree.insert("", "end", values=list(ordinary_worker.data.iloc[num]))
                        num = num + 1
                case 30:
                    num = 20
                    managers_df = ordinary_worker.data.iloc[[20, 21, 22, 23, 24, 25]]
                    for i in range(6):
                        tree.insert("", "end", values=list(ordinary_worker.data.iloc[num]))
                        num = num + 1
            tree.grid(row=1, column=1, columnspan=3, rowspan=3, stick='wens')

        else:
            tree.insert("", "end", values=list(ordinary_worker.data.iloc[self.user_id]))
            tree.grid(row=2, column=1, columnspan=2, rowspan=1, stick='wens')
        main_window.mainloop()


class LogIn:
    @staticmethod
    def logInWindowShow(encodeListKnown):
        def faceId():
            path = 'KnownFaces'
            classNames = []
            myList = os.listdir(path)

            for cls in myList:
                curImg = cv2.imread(f'{path}/{cls}')
                classNames.append(os.path.splitext(cls)[0])

            cap = cv2.VideoCapture(0)
            
            start_time = time.time()
            while time.time() - start_time < 3:
                success, img = cap.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = classNames[matchIndex]
                        cv2.destroyAllWindows()
                        time.sleep(1)
                        cap.release()
                        verifiedFace = None
                        match name:
                            case "Роман":
                                verifiedFace = 30
                            case "Ольчик":
                                verifiedFace = 0
                            case "Максим":
                                verifiedFace = 31
                        tryToEnter(2, verifiedFace)
                        return
                              
            messagebox.showwarning("Лице не розпізнано", "Спробуйте ще раз, або увійдіть за логіном та паролем.")
                
    
        def tryToEnter(variant, id):
            user_data = {
            "BlueFox23": "4H7G9T",
            "CyberNinja88": "K2F8J6",
            "SilverDragon42": "3D5L9P",
            "NeonScribe77": "Q6R2X7",
            "StarGazer99": "Y1Z8K4",
            "TechPioneer61": "7N9S3E",
            "CosmicJoker73": "I6U2V5",
            "QuantumCoder55": "8W3M1O",
            "DreamWeaver27": "F7C9D2",
            "PixelPirate66": "5G4H8Q",
            "JungleExplorer45": "A2I3B6",
            "ElectricPhantom18": "9K7J1L",
            "LunaGuardian84": "1M6N8T",
            "BinaryAdventurer70": "V4S5O3",
            "EmeraldEnigma52": "U6X9P2",
            "SolarSeeker39": "R3E7W4",
            "StormChaser64": "8F2D1Z",
            "DataSculptor47": "T9Y5G6",
            "AuroraWizard21": "H1O4C7",
            "TerraVoyager59": "6V3I8B",
            "AquaMystic75": "2X9Q5N",
            "TimeTraveler53": "7L1K4M",
            "StealthHacker29": "3P6A9R",
            "AlphaCentauri7": "Z8U7W2",
            "GalacticScribe12": "4G5T1S",
            "InfinityNebula63": "J2E9N3",
            "MysticSorcerer26": "8D7H6Q",
            "QuantumQuasar33": "B1F4V5",
            "PhoenixFlame81": "O2X6C3",
            "CodeSleuth44": "5Y9I7P",
            "StarshipCaptain92": "6R3W8K",
            "StarshipCommander17": "9T2X4F"
        }
            match variant:
                case 1:
                    password = password_input.get()
                    username = login_input.get()
                    if username in user_data and user_data[username] == password:
                        log_in.destroy()
                        user_id = list(user_data.keys()).index(username)
                        ordinary_worker_window = Ordinaryworkertkinter(encodeListKnown, user_id)
                        ordinary_worker_window.mainWindow()
                    else:
                        password_input.delete(0, END)
                        login_input.delete(0, END)
                        messagebox.showinfo(message='Wrong username or password!')
                case 2:
                    log_in.destroy()
                    ordinary_worker_window = Ordinaryworkertkinter(encodeListKnown, id)
                    ordinary_worker_window.mainWindow()
        log_in = Tk()

        log_in.title("Enter to database")

        screen_width = log_in.winfo_screenwidth()
        screen_height = log_in.winfo_screenheight()

        x = (screen_width - 350) // 2
        y = (screen_height - 140) // 2

        log_in.geometry('{}x{}+{}+{}'.format(350, 140, x, y))

        log_in.resizable(width=False, height=False)

        frame = Frame(log_in)
        frame.place(relwidth=1, relheight=1)

        title1 = Label(frame, text="Username", )
        title1.pack()

        login_input = Entry(frame, bg='white', fg='black', )
        login_input.pack()

        title2 = Label(frame, text="Password", )
        title2.pack()

        password_input = Entry(frame, bg='white', fg='black', show="*")
        password_input.pack()

        btn_sign_in = Button(frame, text="Sign in", command=lambda: tryToEnter(1, 0), width=5)
        btn_sign_in.pack(side="left", padx=45)

        btn_face_id = Button(frame, text="Face ID", command=faceId, width=5)
        btn_face_id.pack(side="right", padx=45)

        log_in.mainloop()


log_in_window = LogIn()

path = 'KnownFaces'
myList = os.listdir(path)
images = []
for cls in myList:
        curImg = cv2.imread(f'{path}/{cls}')
        images.append(curImg)
def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

encodeListKnown = findEncodings(images)
print("Все завантажено успішно")

log_in_window.logInWindowShow(encodeListKnown)
