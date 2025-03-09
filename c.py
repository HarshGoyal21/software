from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox


class Criminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Criminal Records System")
        self.root.geometry('1530x790+0+0')
        self.connect_db()

        # ====== Variables ======
        self.var_case_id = StringVar()
        self.var_criminal_no = StringVar()
        self.var_criminal_name = StringVar()
        self.var_nickname = StringVar()
        self.var_arrest_date = StringVar()
        self.var_date_of_crime = StringVar()
        self.var_gender = StringVar() 
        self.var_wanted = StringVar()
        self.var_age = StringVar()
        self.var_occupation = StringVar()
        self.var_birthmark = StringVar()
        self.var_crime_type = StringVar()
        self.var_father_name = StringVar()
        self.var_search_by = StringVar()
        self.var_search_text = StringVar()

        # ====== Title ======
        lbl_title = Label(self.root, text='Criminal Records System Software', 
                          font=('times new roman', 40, 'bold'), bg='black', fg='gold')
        lbl_title.place(x=0, y=0, width=1530, height=70)

        # ====== Police Logo ======
        img_logo = Image.open("images/logo.png").resize((60, 60), Image.LANCZOS)
        self.photo_logo = ImageTk.PhotoImage(img_logo)
        Label(self.root, image=self.photo_logo).place(x=290, y=5, width=60, height=60)

        # ====== Image Frame ======
        self.img_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        self.img_frame.place(x=0, y=70, width=1530, height=160)

        img_files = ["images/police1.jpeg", "images/police2.jpeg", "images/police3.jpeg"]
        x_pos = 0
        self.photos = []
        for file in img_files:
            img = Image.open(file).resize((510, 160), Image.LANCZOS)
            self.photos.append(ImageTk.PhotoImage(img))
            Label(self.img_frame, image=self.photos[-1]).place(x=x_pos, y=0, width=510, height=160)
            x_pos += 510

        # ====== Main Frame ======
        self.main_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        self.main_frame.place(x=10, y=230, width=1500, height=520)

        # ====== Upper Frame ======
        self.upper_frame = LabelFrame(self.main_frame, bd=2, relief=RIDGE, 
                                      text="Criminal Information", font=('times new roman', 15, 'bold'), 
                                      fg='red', bg='white')
        self.upper_frame.place(x=10, y=10, width=1480, height=300)

        # ====== Labels and Entry Fields ======
        labels = [
            ("Case ID", self.var_case_id),
            ("Criminal No", self.var_criminal_no),
            ("Criminal Name", self.var_criminal_name),
            ("Nickname", self.var_nickname),
            ("Arrest Date", self.var_arrest_date),
            ("Date of Crime", self.var_date_of_crime),
            ("Age", self.var_age),
            ("Occupation", self.var_occupation),
            ("Birthmark", self.var_birthmark),
            ("Crime Type", self.var_crime_type),
            ("Father Name", self.var_father_name)
        ]

        row, col = 0, 0
        for text, var in labels:
            Label(self.upper_frame, text=f"{text}:", font=('arial', 12, 'bold'), bg='white').grid(row=row, column=col*2, padx=5, pady=7, sticky=W)
            Entry(self.upper_frame, textvariable=var, font=('arial', 12, 'bold'), width=22).grid(row=row, column=col*2 + 1, padx=5, pady=7)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # ====== Gender ======
        Label(self.upper_frame, text="Gender:", font=('arial', 12, 'bold'), bg='white').grid(row=row, column=0, padx=5, pady=7, sticky=W)
        combo_gender = ttk.Combobox(self.upper_frame, textvariable=self.var_gender, font=('arial', 12, 'bold'), width=20, state='readonly')
        combo_gender['values'] = ('Male', 'Female')
        combo_gender.grid(row=row, column=1, padx=5, pady=7)
        combo_gender.current(0)

        # ====== Most Wanted ======
        Label(self.upper_frame, text="Most Wanted:", font=('arial', 12, 'bold'), bg='white').grid(row=row, column=2, padx=5, pady=7, sticky=W)
        combo_wanted = ttk.Combobox(self.upper_frame, textvariable=self.var_wanted, font=('arial', 12, 'bold'), width=20, state='readonly')
        combo_wanted['values'] = ('Yes', 'No')
        combo_wanted.grid(row=row, column=3, padx=5, pady=7)
        combo_wanted.current(1)

        # ====== Placeholder Image ======
        img_placeholder = Image.open("images/policeman1.jpeg").resize((180, 180), Image.LANCZOS)
        self.photo_placeholder = ImageTk.PhotoImage(img_placeholder)
        lbl_placeholder = Label(self.upper_frame, image=self.photo_placeholder, bg='white')
        lbl_placeholder.place(x=700, y=20, width=180, height=180)

        # ====== Buttons ======
        button_frame = Frame(self.upper_frame, bg="white", bd=0)
        button_frame.place(x=0, y=240, width=640, height=40)

        Button(button_frame, text="Save", command=self.add_data, font=('arial', 12, 'bold'), bg='blue', fg='white', width=15).grid(row=0, column=0, padx=10)
        Button(button_frame, text="Update", command=self.update_data, font=('arial', 12, 'bold'), bg='red', fg='white', width=15).grid(row=0, column=1, padx=10)
        Button(button_frame, text="Clear", command=self.clear_fields, font=('arial', 12, 'bold'), bg='orange', fg='white', width=15).grid(row=0, column=2, padx=10)
        Button(button_frame, text="Delete", command=self.delete_data, font=('arial', 12, 'bold'), bg='green', fg='white', width=12).grid(row=0, column=3, padx=10)

        # ====== Lower Frame ======
        self.lower_frame = LabelFrame(self.main_frame, bd=2, relief=RIDGE, 
                                      text="Criminal Information Table", font=('times new roman', 15, 'bold'), 
                                      fg='red', bg='white')
        self.lower_frame.place(x=10, y=320, width=1480, height=180)

        # ====== Search Frame ======
        self.search_frame = LabelFrame(self.lower_frame, bd=2, relief=RIDGE, 
                                       text="Search Criminal Record", font=('times new roman', 15, 'bold'), 
                                       fg='red', bg='white')
        self.search_frame.place(x=0, y=0, width=1470, height=60)

        # ====== Search By Label ======
        lbl_search_by = Label(self.search_frame, text="Search By:", font=('arial', 12, 'bold'),
                              bg='red', fg='white')
        lbl_search_by.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # ====== Search By Combobox ======
        combo_search = ttk.Combobox(self.search_frame, textvariable=self.var_search_by,
                                    font=('arial', 12, 'bold'), width=20, state='readonly')
        combo_search['values'] = ("Select Option", "Case ID", "Criminal No", "Criminal Name")
        combo_search.grid(row=0, column=1, padx=5, pady=5)
        combo_search.current(0)

        # ====== Search Entry ======
        search_txt = Entry(self.search_frame, textvariable=self.var_search_text,
                           font=('arial', 12, 'bold'), width=30)
        search_txt.grid(row=0, column=2, padx=5, pady=5)

        # ====== Search Button ======
        btn_search = Button(self.search_frame, text="Search", command=self.search_data,
                            font=('arial', 12, 'bold'), bg='blue', fg='white', width=12)
        btn_search.grid(row=0, column=3, padx=5, pady=5)

        # ====== Show All Button ======
        btn_show_all = Button(self.search_frame, text="Show All", command=self.show_all_data,
                              font=('arial', 12, 'bold'), bg='blue', fg='white', width=12)
        btn_show_all.grid(row=0, column=4, padx=5, pady=5)

        # ====== National Crime Agency Text ======
        lbl_agency = Label(self.search_frame, text="NATIONAL CRIME AGENCY", 
                           font=('times new roman', 20, 'bold'), fg='red', bg='white')
        lbl_agency.grid(row=0, column=5, padx=50, pady=5, sticky=W)

        # ====== Criminal Table ======
        self.criminal_table = ttk.Treeview(self.lower_frame, 
                                   columns=("case_id", "criminal_no", "criminal_name", "nickname", 
                                            "arrest_date", "date_of_crime", "gender", "wanted", 
                                            "age", "occupation", "birthmark", "crime_type", "father_name"))

        self.criminal_table.heading("case_id", text="Case ID")
        self.criminal_table.heading("criminal_no", text="Criminal No")
        self.criminal_table.heading("criminal_name", text="Criminal Name")
        self.criminal_table.heading("nickname", text="Nickname")
        self.criminal_table.heading("arrest_date", text="Arrest Date")
        self.criminal_table.heading("date_of_crime", text="Date of Crime")
        self.criminal_table.heading("gender", text="Gender")
        self.criminal_table.heading("wanted", text="Most Wanted")
        self.criminal_table.heading("age", text="Age")
        self.criminal_table.heading("occupation", text="Occupation")
        self.criminal_table.heading("birthmark", text="Birthmark")
        self.criminal_table.heading("crime_type", text="Crime Type")
        self.criminal_table.heading("father_name", text="Father Name")

        self.criminal_table["show"] = "headings"
        self.criminal_table.pack(fill=BOTH, expand=1)

        # Set column width
        for col in ("case_id", "criminal_no", "criminal_name", "nickname", 
                    "arrest_date", "date_of_crime", "gender", "wanted", 
                    "age", "occupation", "birthmark", "crime_type", "father_name"):
            self.criminal_table.column(col, width=100)

        self.fetch_data()  # Load initial data

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost:3306",
                username="root",  # Your MySQL username
                password="12345",  # Your MySQL password
                database="criminal_db"
            )
            self.cursor = self.conn.cursor()
            print("Database connected successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to database:\n{str(e)}")

    def add_data(self):
        if self.var_case_id.get() == "" or self.var_criminal_no.get() == "" or self.var_criminal_name.get() == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                query = """INSERT INTO criminals (
                    case_id, criminal_no, criminal_name, nickname, arrest_date, date_of_crime, 
                    gender, wanted, age, occupation, birthmark, crime_type, father_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                values = (
                    self.var_case_id.get(),
                    self.var_criminal_no.get(),
                    self.var_criminal_name.get(),
                    self.var_nickname.get(),
                    self.var_arrest_date.get(),
                    self.var_date_of_crime.get(),
                    self.var_gender.get(),
                    self.var_wanted.get(),
                    self.var_age.get(),
                    self.var_occupation.get(),
                    self.var_birthmark.get(),
                    self.var_crime_type.get(),
                    self.var_father_name.get()
                )
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("Success", "Record added successfully!")
                self.fetch_data()  # Refresh the table
            except Exception as e:
                messagebox.showerror("Error", f"Error saving data:\n{str(e)}")

    def fetch_data(self):
        try:
            self.cursor.execute("SELECT * FROM criminals")
            rows = self.cursor.fetchall()
            if len(rows) != 0:
                self.criminal_table.delete(*self.criminal_table.get_children())
                for row in rows:
                    self.criminal_table.insert('', END, values=row)
                self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data:\n{str(e)}")

    def update_data(self):
        if self.var_case_id.get() == "" or self.var_criminal_no.get() == "" or self.var_criminal_name.get() == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                query = """UPDATE criminals SET 
                    criminal_no=%s, criminal_name=%s, nickname=%s, arrest_date=%s, 
                    date_of_crime=%s, gender=%s, wanted=%s, age=%s, 
                    occupation=%s, birthmark=%s, crime_type=%s, father_name=%s 
                    WHERE case_id=%s"""
                
                values = (
                    self.var_criminal_no.get(),
                    self.var_criminal_name.get(),
                    self.var_nickname.get(),
                    self.var_arrest_date.get(),
                    self.var_date_of_crime.get(),
                    self.var_gender.get(),
                    self.var_wanted.get(),
                    self.var_age.get(),
                    self.var_occupation.get(),
                    self.var_birthmark.get(),
                    self.var_crime_type.get(),
                    self.var_father_name.get(),
                    self.var_case_id.get()  # This is the case_id to identify the record to update
                )
                self.cursor.execute(query, values)
                self.conn.commit()
                messagebox.showinfo("Success", "Record updated successfully!")
                self.fetch_data()  # Refresh the table
            except Exception as e:
                messagebox.showerror("Error", f"Error updating data:\n{str(e)}")

    def delete_data(self):
        try:
            selected_item = self.criminal_table.selection()[0]
            values = self.criminal_table.item(selected_item)['values']
            case_id = values[0]

            query = "DELETE FROM criminals WHERE case_id=%s"
            self.cursor.execute(query, (case_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data:\n{str(e)}")

    def clear_fields(self):
        self.var_case_id.set("")
        self.var_criminal_no.set("")
        self.var_criminal_name.set("")
        self.var_nickname.set("")
        self.var_arrest_date.set("")
        self.var_date_of_crime.set("")
        self.var_gender.set("")
        self.var_wanted.set("")
        self.var_age.set("")
        self.var_occupation.set("")
        self.var_birthmark.set("")
        self.var_crime_type.set("")
        self.var_father_name.set("")
        self.var_search_by.set("Select Option")
        self.var_search_text.set("")

    def search_data(self):
        search_by = self.var_search_by.get()
        search_text = self.var_search_text.get()
        if search_by == "Select Option":
            messagebox.showerror("Error", "Please select a search option.")
            return

        try:
            query = f"SELECT * FROM criminals WHERE {search_by.lower().replace(' ', '_')} LIKE %s"
            self.cursor.execute(query, ('%' + search_text + '%',))
            rows = self.cursor.fetchall()
            if len(rows) != 0:
                self.criminal_table.delete(*self.criminal_table.get_children())
                for row in rows:
                    self.criminal_table.insert('', END, values=row)
                self.conn.commit()
            else:
                messagebox.showinfo("No Results", "No records found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data:\n{str(e)}")

    def show_all_data(self):
        self.fetch_data()  # Refresh the table to show all records

    def __del__(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    root = Tk()
    obj = Criminal(root)
    root.mainloop()