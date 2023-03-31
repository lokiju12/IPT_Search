


from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import sqlite3

# db 연결
conn = sqlite3.connect('PhoneBook.db')
c = conn.cursor()

'''
생성되는 테이블의 사용 용도
id = 고유번호
column1 = 내선번호
column2 = IP
column3 = 부서
column4 = 성명
column5 = 기타
'''
c.execute('''CREATE TABLE IF NOT EXISTS App_DB
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            column1 TEXT,
            column2 TEXT,
            column3 TEXT,
            column4 TEXT,
            column5 TEXT,
            column6 TEXT
            )''')
conn.commit()


# tkinter GUI 생성
root = Tk()
root.title('전화번호부') 
root.geometry('+800+300')
# root.state('zoomed') # 전체화면
# root.iconbitmap('logo.ico')
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# 입력 프레임
frame_input = Frame()
frame_input.grid(row=0, column=0, padx=10, pady=10, sticky='n')
# 전화번호
label_number = Label(frame_input, text = '전화번호')
label_number.grid(row=0, column=0, padx=5, pady=5)
entry_number = Entry(frame_input)
entry_number.grid(row=0, column=1, padx=5, pady=5)
# IP
label_ip = Label(frame_input, text = 'IP')
label_ip.grid(row=1, column=0, padx=5, pady=5)
entry_ip = Entry(frame_input)
entry_ip.grid(row=1, column=1, padx=5, pady=5)
# 부서
label_team = Label(frame_input, text = '부서')
label_team.grid(row=2, column=0, padx=5, pady=5)
entry_team = Entry(frame_input)
entry_team.grid(row=2, column=1, padx=5, pady=5)
# 성명
label_name = Label(frame_input, text = '성명')
label_name.grid(row=3, column=0, padx=5, pady=5)
entry_name = Entry(frame_input)
entry_name.grid(row=3, column=1, padx=5, pady=5)
# 기타
label_etc = Label(frame_input, text = '기타')
label_etc.grid(row=4, column=0, padx=5, pady=5)
entry_etc = Entry(frame_input)
entry_etc.grid(row=4, column=1, padx=5, pady=5)







frame_treeview = Frame()
frame_treeview.grid(row=0, column=1, padx=10, pady=10, sticky='n')

tree = ttk.Treeview(frame_treeview)
tree.grid(row=2, column=0, columnspan=2, pady=0)

yscrollcommand = ttk.Scrollbar(frame_treeview, orient=VERTICAL, command=tree.yview)
yscrollcommand.grid(row=2, column=2, pady=0)
yscrollcommand.grid_configure(sticky='ns')

# tree.tag_configure('Treeview.Heading', **{'font': font})
tree.configure(height=22)
tree.configure(yscrollcommand=yscrollcommand.set)
tree.columnconfigure(0, weight=1)
tree.rowconfigure(0, weight=1)
tree.grid_configure(sticky='nsew')


# Treeview1 생성

column1 = '내선번호'
column2 = 'IP'
column3 = '부서'
column4 = '성명'
column5 = '기타'

# Treeview 열 설정
tree['columns'] = (
                    column1, 
                    column2, 
                    column3, 
                    column4, 
                    column5, 
                    )
tree['show'] = 'headings' # id 값 숨기기

tree.column(column1, width=100, anchor="center")
tree.column(column2, width=100, anchor="center")
tree.column(column3, width=100, anchor="center")
tree.column(column4, width=100, anchor="center")
tree.column(column5, width=100, anchor="center")

tree.heading(column1, text='전화번호')
tree.heading(column2, text='IP')
tree.heading(column3, text='부서')
tree.heading(column4, text='성명')
tree.heading(column5, text='기타')






def next_entry(event):
    widget = event.widget
    widget.tk_focusNext().focus()
    return "break"
entry_number.bind('<Return>', next_entry)
entry_ip.bind('<Return>', next_entry)
entry_team.bind('<Return>', next_entry)
entry_name.bind('<Return>', next_entry)


def load_data():
    # DB에서 데이터 불러오기
    c.execute("SELECT * FROM App_DB ORDER BY column1 ASC") #column1을 기준으로 오름차순 정렬 (Order By column1 ASC)
    rows = c.fetchall()
    # 트리뷰 초기화
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', text=row[0], values=row[1:]) # 각 아이템의 id 값을 Treeview에 추가
    print('load_data!!')
# 프로그램 시작시 DB에 저장된 데이터 불러오기
load_data()


def save_data(event=True):
    global conn, c, tree
    number = entry_number.get()
    ip = entry_ip.get()
    team = entry_team.get()
    name = entry_name.get()
    etc = entry_etc.get()
    c.execute("INSERT INTO App_DB (column1, column2, column3, column4, column5) VALUES (?, ?, ?, ?, ?)", (number, ip, team, name, etc))
    conn.commit()
    messagebox.showinfo('알림', '저장이 완료되었습니다.')
    entry_number.delete(0, END)
    entry_ip.delete(0, END)
    entry_team.delete(0, END)
    entry_name.delete(0, END)
    entry_etc.delete(0, END)
    entry_number.focus_set()
    load_data()
entry_etc.bind('<Return>', save_data)


def delete_data(event=True):
    global conn, c, tree
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning('경고', '삭제할 데이터를 선택해주세요.')
        return
    if messagebox.askyesno('삭제', '되돌릴 수 없습니다.\n\n삭제하시겠습니까?'):
        for item in selected_item:
            item_id = tree.item(item, 'text')
            c.execute("DELETE FROM App_DB WHERE id=?", (item_id,))
            conn.commit()
            tree.delete(item)
        messagebox.showinfo('알림', '삭제가 완료되었습니다.')
# Delete 키 바인딩
tree.bind('<Delete>', delete_data)


def on_double_click(event):
    # 선택한 행의 값들 가져오기
    selection = tree.selection()
    if len(selection) == 0:
        return
    values = tree.item(selection[0], 'values')
    
    # Toplevel 창 열기
    top = Toplevel(root)
    top.title('수정')
    top.geometry('+1000+400')
    # top.iconbitmap('logo.ico')
    # Frame
    new_ent_frame = Frame(top)
    new_ent_frame.pack(padx=20, pady=20)
    
    new_lab1 = Label(new_ent_frame, text='IP')
    new_lab1.grid(row=0, column=0, sticky=W)
    new_ent1 = Entry(new_ent_frame, width=30, relief='flat', highlightthickness=1)
    new_ent1.config(highlightbackground='gray')
    new_ent1.grid(row=0, column=1, padx=10, pady=10)
    new_ent1.focus() # new_ent1에 프롬프트 설정
    
    new_lab2 = Label(new_ent_frame, text='부서')
    new_lab2.grid(row=1, column=0, sticky=W)
    new_ent2 = Entry(new_ent_frame, width=30, relief='flat', highlightthickness=1)
    new_ent2.config(highlightbackground='gray')
    new_ent2.grid(row=1, column=1, padx=10, pady=10)
    
    new_lab3 = Label(new_ent_frame, text='성명')
    new_lab3.grid(row=2, column=0, sticky=W)
    new_ent3 = Entry(new_ent_frame, width=30, relief='flat', highlightthickness=1)
    new_ent3.config(highlightbackground='gray')
    new_ent3.grid(row=2, column=1, padx=10, pady=10)
    
    new_lab4 = Label(new_ent_frame, text='기타')
    new_lab4.grid(row=3, column=0, sticky=W)
    new_ent4 = Entry(new_ent_frame, width=30, relief='flat', highlightthickness=1)
    new_ent4.config(highlightbackground='gray')
    new_ent4.grid(row=3, column=1, padx=10, pady=10)
    
    # 기존 DB 데이터를 ent에 입력
    # new_ent1.insert(0, values[1])  
    # new_ent2.insert(0, values[2])  
    # new_ent3.insert(0, values[3])  
    # new_ent4.insert(0, values[4])  
    
    def update_data(event=True):
        global conn, c, tree
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('오류', '데이터를 선택해주세요.')
            return
        old_data = tree.item(selected_item, 'values')
        ip = new_ent1.get()
        team = new_ent2.get()
        name = new_ent3.get()
        etc = new_ent4.get()
        c.execute("UPDATE App_DB SET column2=?, column3=?, column4=?, column5=? WHERE column1=?", (ip, team, name, etc, old_data[0]))
        conn.commit()
        # Toplevel 창 닫기
        top.destroy()
        messagebox.showinfo('알림', '데이터가 수정되었습니다.')
        
        entry_ip.delete(0, END)
        entry_team.delete(0, END)
        entry_name.delete(0, END)
        entry_etc.delete(0, END)
        
        entry_number.focus_set()
        load_data()
    new_ent1.bind('<Return>', next_entry)
    new_ent2.bind('<Return>', next_entry)
    new_ent3.bind('<Return>', next_entry)
    new_ent4.bind('<Return>', update_data)
tree.bind('<Double-1>', on_double_click)

root.mainloop()