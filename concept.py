import tkinter as tk
from tkinter import simpledialog
import pickle
import os
import sqlite3
import pyautogui
import time
import webbrowser
import clipboard
import re
import cv2


root = tk.Tk()

connection = sqlite3.connect("concept_data.db")
cursor = connection.cursor()

def insert_data(table_name , student_name , father_phone_number):
    cursor.execute(f"""
        INSERT INTO {table_name} (student_name, father_phone_number) VALUES (?, ?)
    """, (student_name, father_phone_number))
    connection.commit()

def save_data():
    father_numbers = fathers_phone_numbers.get("1.0", tk.END)
    print(father_numbers)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        father_phone_number INTEGER
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_phoneNumber_error (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        father_phone_number TEXT
    )
    """)
    
def print_data(table_name):
    data = cursor.execute(f"""
    SELECT * FROM {table_name}
    """)
    print(data)
    for row in cursor.fetchall():
        student_list.insert("end", row[1])
        student_list.insert("end", row[2])
        print(row)
    enter_message_lable = tk.Label(root, text="الأرقام التي فشل إرسال رسائل لها", font=('calibre', 10, 'bold') , height=2)
    enter_message_lable.grid(row=2 , column=0)
    student_list.grid(row=3 , column=0)

def delete_data(father_phone_number):
    cursor.execute(
        f"""
        DELETE FROM students
        WHERE father_phone_number = {father_phone_number}
        """
    )
    rows_deleted = cursor.rowcount

    if rows_deleted > 0:
        print("تم حذف البيانات بنجاح")
    else:
        print("لم يتم العثور على أي بيانات لحذفها")
    
def startChat():
    save_data()
    students = fathers_phone_numbers.get("1.0", tk.END)
    for student in students.splitlines():
        father_of_student_name, father_phoneNumber = student.split("\t")
        if not student.strip():
            continue
        if isinstance(father_phoneNumber, str):
            if len(father_phoneNumber)!= 10:
                insert_data(table_name='students_phoneNumber_error', student_name=father_of_student_name, father_phone_number=father_phoneNumber)
                print_data(table_name='students_phoneNumber_error')
                print('Invalid ID:', father_phoneNumber)
            else:
                send_button = os.path.join(os.path.dirname(__file__), "send_button.png")
                type_message = os.path.join(os.path.dirname(__file__), "type_message.png")
                whats_app_not_found = os.path.join(os.path.dirname(__file__), "whats_app_not_found.png")
                print('Valid ID:', student)
                welcome_father_of_student= f'{"إزيك يا" + f' {father_of_student_name} '}'
                print(f"father of student : {welcome_father_of_student}")
                message_for_send = enter_message_entry.get("1.0", tk.END)
                message_templet = f'{welcome_father_of_student + f'{message_for_send}'}'
                print(message_templet)
                clipboard.copy(message_templet)
                webbrowser.open('C:\Program Files\Google\Chrome\Application\chrome.exe')
                pyautogui.hotkey('ctrl','t')
                time.sleep(0.5)
                pyautogui.typewrite(f"https://api.whatsapp.com/send/?phone=20{father_phoneNumber}&text=&type=phone_number&app_absent=0")
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(2)
                try:
                    whats_app_not_found_icon = pyautogui.locateOnScreen(whats_app_not_found, confidence=0.9)
                    if whats_app_not_found:
                        print('aheee')
                        pyautogui.moveTo(whats_app_not_found_icon)
                        time.sleep(1)
                        pyautogui.click()
                        insert_data(table_name='students_phoneNumber_error', student_name=father_of_student_name, father_phone_number=father_phoneNumber)
                        continue
                except Exception as e:
                    button3location =  pyautogui.locateCenterOnScreen(type_message, confidence=0.8)
                    time.sleep(1)
                    pyautogui.moveTo(button3location)
                    time.sleep(1)
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.hotkey('ctrl','v')
                    time.sleep(1)
                    button2location =  pyautogui.locateCenterOnScreen(send_button, confidence=0.7)
                    time.sleep(1)
                    pyautogui.moveTo(button2location)
                    time.sleep(1)
                    pyautogui.click()
        else:
            print('Error: ID is not an integer')

    # print_data(table_name='students_phoneNumber_error')        

# Create Entry widgets for input
father_name_var = tk.StringVar()
father_number_var = tk.IntVar()
enter_message_var = tk.StringVar()
father_number_to_delete_var = tk.IntVar()


student_list = tk.Listbox(root, height = 4, 
                  width = 20, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow" , 
                  borderwidth=3)
    
# student_father_lable = tk.Label(root, text="إسم ولي أمر الطالب:", font=('calibre', 10, 'bold'),)
# student_father_entry = tk.Entry(root, textvariable=father_name_var, font=('calibre', 20, 'normal') ,width="20",)

scroll_y = tk.Scrollbar(root)
fathers_phone_numbers = tk.Text(root, width=50 ,height=15, relief='groove', wrap='word',  yscrollcommand=scroll_y.set,font=('calibre', 10, 'bold'))
# father_number_entry = tk.Entry(root, textvariable=father_number_var, font=('calibre', 20, 'normal'))

# fathers_number_label = tk.Label(root, text="أسماء أولياء الأمور المسجله:", font=('calibre', 10, 'bold'))

# save_btn = tk.Button(root, text="Submit", command=save_data, background='red' , foreground='white' , width=20)
send_message_data = tk.Button(root, text="sendMessages", command=startChat , background='red' , foreground='white' , width=15, height=1)
# print_data_button = tk.Button(root, text="printData", command=print_data(table_name='students') , background='red' , foreground='white' , width=20)
delete_data_button = tk.Button(root, text="deleteData", command=delete_data , background='red' , foreground='white' , width=20)

enter_message_lable = tk.Label(root, text="الرساله المراد إرسالها:", font=('calibre', 10, 'bold') , height=2)
enter_message_entry = tk.Text(root, width=50 ,height=15, relief='groove', wrap='word', font=('calibre', 10, 'bold') )


# student_father_lable.grid(row=0 , column=0)
# student_father_entry.grid(row=1, column=0)

fathers_phone_numbers.grid(row=0 , column=1)
# father_number_entry.grid(row=1, column=1)
scroll_y.grid(row=0 , column=4)
scroll_y.config(command=fathers_phone_numbers.yview)
# fathers_number_label.grid(row=0 , column=2)

# save_btn.grid(row=1, column=3)
enter_message_lable.grid(row=0 , column=0)
enter_message_entry.grid(row=0, column=0)
send_message_data.grid(row=3, column=1)

# print_data_button.grid(row=4, column=0)
root.mainloop()
