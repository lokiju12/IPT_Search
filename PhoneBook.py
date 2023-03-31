


from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3

# db 연결
conn = sqlite3.connect('PhoneBook.db')
c = conn.cursor()

'''
생성되는 테이블의 사용 용도
column1 = 내선번호
column2 = IP
column3 = 부서
column4 = 성명
column5 = 기타입력
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
root.geometry('+1100+300')
# root.state('zoomed') # 전체화면
# root.iconbitmap('logo.ico')
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# 입력 프레임
frame_input = Frame()
frame_input.pack(side='left')
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
# 기타입력
label_etc = Label(frame_input, text = '기타입력')
label_etc.grid(row=4, column=0, padx=5, pady=5)
entry_etc = Entry(frame_input)
entry_etc.grid(row=4, column=1, padx=5, pady=5)

# 엔트리 데이터
number = entry_number.get()
ip = entry_ip.get()
team = entry_team.get()
name = entry_name.get()
etc = entry_etc.get()



def save_data(event=True):
    # DB에 데이터 추가
    c.execute("SELECT MAX(id) FROM App_DB")
    last_id = c.fetchone()[0]
    if last_id is None:
        last_id = 0
    new_id = last_id + 1
    c.execute("INSERT INTO App_DB (id, column1, column2, column3, column4, column5) VALUES (?, ?, ?, ?, ?, ?)",
                    (new_id, number, ip, team, name, etc))
    conn.commit()
    # 트리뷰에 데이터 추가
    tree.insert('', 'end', text=new_id, values=(number, ip, team, name, etc))
    # # 입력란 초기화 하기
    # ent1.delete(0, tk.END)
    # ent2.delete(0, tk.END)
    # ent3.delete(0, tk.END)
    # ent4.delete(0, tk.END)
    print('save_data!!')

entry_etc.bind('<Return>', save_data)














frame_treeview = Frame()
frame_treeview.pack(side='right')

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
column5 = '기타입력'

# Treeview 열 설정
tree['columns'] = (column1, 
                    column2, 
                    column3, 
                    column4, 
                    column5, 
                    )
tree['show'] = 'headings'

tree.column(column1, stretch=NO, minwidth=0, width=0) # 폭 조정으로 column1을 숨김
tree.column(column2, width=100, anchor="center")
tree.column(column3, width=100, anchor="center")
tree.column(column4, width=100, anchor="center")
tree.column(column5, width=100)


tree.heading(column1, text='전화번호')
tree.heading(column2, text='IP')
tree.heading(column3, text='부서')
tree.heading(column4, text='성명')
tree.heading(column5, text='기타입력')









root.mainloop()