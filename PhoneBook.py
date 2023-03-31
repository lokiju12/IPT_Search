


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
root.geometry('+1100+300')
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




def save_data(event=None):
    print('save_data!!')
    global conn, c, tree
    # entry widget에서 값 가져오기
    number = entry_number.get()
    ip = entry_ip.get()
    team = entry_team.get()
    name = entry_name.get()
    etc = entry_etc.get()
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
    # 데이터 새로 고침
    load_data()
    # 입력란 초기화 하기
    entry_number.delete(0, 'end')
    entry_ip.delete(0, 'end')
    entry_team.delete(0, 'end')
    entry_name.delete(0, 'end')
    entry_etc.delete(0, 'end')
    # 포커스 이동
    entry_number.focus()
# 엔터키 바인딩
entry_etc.bind('<Return>', save_data)






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
tree['columns'] = (column1, 
                    column2, 
                    column3, 
                    column4, 
                    column5, 
                    )
tree['show'] = 'headings'



# tree.column(column1, stretch=NO, minwidth=0, width=0) # 폭 조정으로 column1을 숨김
tree.column(column1, width=100, anchor="center")
tree.column(column2, width=100, anchor="center")
tree.column(column3, width=100, anchor="center")
tree.column(column4, width=100, anchor="center")
tree.column(column5, width=100)

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
    # 트리뷰에 데이터 추가
    for row in rows:
        tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
    print('load_data!!')
# 프로그램 시작시 DB에 저장된 데이터 불러오기
load_data()

# Treeview 더블 클릭을 통한 데이터 수정
def on_double_click(event):
    print('on_double_click')
    # 선택한 행의 값들 가져오기
    selection = tree.selection()
    if len(selection) == 0:
        return
    values = tree.item(selection[0], 'values')
    
    # Toplevel 창 열기
    top = Toplevel(root)
    top.title('수정')
    top.geometry('+800+300')
    # top.iconbitmap('logo.ico')
    # Frame
    new_ent_frame = Frame(top)
    new_ent_frame.pack(padx=20, pady=20)
    
    new_lab2 = Label(new_ent_frame, text='IP')
    new_lab2.grid(row=1, column=0, sticky=W)
    new_ent2 = Entry(new_ent_frame, width=30)
    new_ent2.grid(row=1, column=1, padx=10, pady=10)
    
    new_lab3 = Label(new_ent_frame, text='부서')
    new_lab3.grid(row=2, column=0, sticky=W)
    new_ent3 = Entry(new_ent_frame, width=30)
    new_ent3.grid(row=2, column=1, padx=10, pady=10)
    
    new_lab4 = Label(new_ent_frame, text='성명')
    new_lab4.grid(row=3, column=0, sticky=W)
    new_ent4 = Entry(new_ent_frame, width=30)
    new_ent4.grid(row=3, column=1, padx=10, pady=10)
    
    new_lab5 = Label(new_ent_frame, text='기타')
    new_lab5.grid(row=4, column=0, sticky=W)
    new_ent5 = Entry(new_ent_frame, width=30)
    new_ent5.grid(row=4, column=1, padx=10, pady=10)
    
    # 기존 DB 데이터를 ent에 입력
    # new_ent2.insert(0, values[1]) # IP
    # new_ent3.insert(0, values[2]) # 부서
    # new_ent4.insert(0, values[3]) # 성명
    # new_ent5.insert(0, values[4]) # 기타
    # Save
    def edit_item(event=None): # 이벤트 동작될 수 있음
        if messagebox.askyesno("EDIT", "변경된 내용은 복구할 수 없습니다.\n저장하려면 YES를 누르세요."):
            # 변경된 값 가져오기
            new_value2 = new_ent2.get()
            new_value3 = new_ent3.get()
            new_value4 = new_ent4.get()
            new_value5 = new_ent5.get()
            # DB 업데이트 [변경 내용이 있는 항목만 업데이트]
            row_id = values[0]
            if new_value2:
                c.execute("UPDATE App_DB SET column2 = ? WHERE id = ?", (new_value2, row_id))
            if new_value3:
                c.execute("UPDATE App_DB SET column3 = ? WHERE id = ?", (new_value3, row_id))
            if new_value4:
                c.execute("UPDATE App_DB SET column4 = ? WHERE id = ?", (new_value4, row_id))
            if new_value5:
                c.execute("UPDATE App_DB SET column5 = ? WHERE id = ?", (new_value5, row_id))
            conn.commit()
            # Toplevel 창 닫기
            top.destroy()
            # Treeview 업데이트
            load_data()
    # 저장버튼
    save_button = Button(top, text='변경하기', command=edit_item, relief='groove')
    save_button.pack(padx=15, pady=15)
    
    # bind
    new_ent2.focus()
    new_ent2.bind('<Return>', next_entry)
    new_ent3.bind('<Return>', next_entry)
    new_ent4.bind('<Return>', next_entry)
    new_ent5.bind('<Return>', edit_item)
    top.bind('<Escape>', lambda event: top.destroy())
    
    # 열과 높이 설정
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)
tree.bind('<Double-1>', on_double_click)
tree.bind('<F2>', on_double_click)





root.mainloop()