from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import pandas as pd

# db 연결
print('connect.db')
conn = sqlite3.connect('PhoneBook.db')
c = conn.cursor()

'''
생성되는 테이블의 사용 용도
id = 고유번호
column1 = 전화번호
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

print('run root window')
# tkinter GUI 생성
root = Tk()
root.title('전화번호부') 
root.geometry('+400+300')
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
entry_number.focus()
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


# csv export
def csv_export():
    print('export_explorer')
    file_path = filedialog.asksaveasfilename(defaultextension='.csv') # 탐색기 실행
    if file_path: # if : 선택한 파일 경로가 있을 경우
        print('export_csv')
        df = pd.read_sql_query("SELECT * from App_DB", conn) # DB에서 데이터 추출하고
        df.to_csv(file_path, index=False, encoding='utf-8-sig') # csv 파일을 utf-8로 저장
        messagebox.showinfo("완료", "파일 저장이 완료되었습니다.") # 완료 메시지
export_button = tk.Button(frame_input, width=10, text='내보내기', command=csv_export)
export_button.grid(row=5, column=0, columnspan=2, padx=25, pady=50, sticky='sw')

# csv import
def csv_import():
    print('import_explorer')
    file_path = filedialog.askopenfilename(defaultextension='.csv') # 탐색기 실행
    if file_path: # if : 선택한 파일 경로가 있을 경우
        print('import_csv')
        df = pd.read_csv(file_path) # csv 데이터를 가져와서
        for row in df.itertuples(): # DB에 데이터 추가
            c.execute("INSERT INTO App_DB (column1, column2, column3, column4, column5) VALUES (?, ?, ?, ?, ?)",
                        (row.column1, row.column2, row.column3, row.column4, row.column5))
        conn.commit() # DB 접속 종료
        load_data()
        messagebox.showinfo("완료", "파일 불러오기가 완료되었습니다.") # 완료 메시지
import_button = tk.Button(frame_input, width=10, text='가져오기', command=csv_import)
import_button.grid(row=5, column=1, columnspan=2, padx=15, pady=50, sticky='se')

# label
text_label = Label(frame_input, text='\n\n\n\n\n\n\n\n 검색 : Ctrl + F\n\n새로고침 : F5\n', anchor='w')
text_label.grid(row=7, column=0, padx=10, pady=5, sticky='sw')

# Frame 2
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


# Treeview 생성
column1 =  '전화번호'
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
tree.column(column2, width=150, anchor="center")
tree.column(column3, width=200, anchor="center")
tree.column(column4, width=200, anchor="center")
tree.column(column5, width=200, anchor="center")

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

def load_data(event=True):
    print('load_data')
    # DB에서 데이터 불러오기
    c.execute("SELECT * FROM App_DB ORDER BY column1 ASC") #column1을 기준으로 오름차순 정렬 (Order By column1 ASC)
    rows = c.fetchall()
    # 트리뷰 초기화
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', text=row[0], values=row[1:]) # 각 아이템의 id 값을 Treeview에 추가
# 프로그램 시작시 DB에 저장된 데이터 불러오기
load_data()

def refresh_data(event=True):
    print('refresh_data')
    messagebox.showinfo('INFO', '새로고침')
    load_data()
root.bind('<F5>', refresh_data)

def save_data(event=True):
    print('save_data')
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
    
    # 선택한 행의 값들 가져오기
    selection = tree.selection()
    if len(selection) == 0:
        return
    values = tree.item(selection[0], 'values')

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
        messagebox.showinfo('INFO', '데이터가 수정되었습니다.')
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
    def on_esc_key(event=True):
        top.destroy()
    top.bind('<Escape>', on_esc_key) # ESC로 창 닫기
tree.bind('<Double-1>', on_double_click)



# Header 클릭을 통한 데이터 정렬
def treeview_sort_column(tv, col, reverse):
    """Treeview 열 정렬 함수"""
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    # 정렬할 데이터가 숫자일 경우
    # l.sort(reverse=reverse, key=lambda x: int(x[0]))
    # 정렬할 데이터가 날짜일 경우
    # l.sort(reverse=reverse, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'))
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    # 다시 한번 클릭 시 정렬 순서를 바꾸기 위해 열 상태를 기록
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
# Tree1과 Tree2의 열 헤더를 클릭 시 정렬
for col in tree['columns']:
    tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))



# Treeview 검색 창 ========================================================================
def search_ctrl_f(event):
    # Toplevel 창 열기
    search_popup = Toplevel(root)
    search_popup.title('검색')
    search_popup.geometry('+800+300')
    # search_popup.iconbitmap('logo.ico')
    search_var = StringVar()
    search_entry = Entry(search_popup, textvariable=search_var, relief='flat', highlightthickness=1)
    search_entry.config(highlightbackground='gray', width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10)
    search_entry.focus()
    
    # 검색을 하는데 첫번째부터 마지막까지 검색하고 결과값이 더 이상 없다면 처음 검색했던 값으로 돌아감
    def search_and_select(tree, search_term):
        # 이전 검색 결과 초기화
        for row in tree.get_children():
            tree.item(row, tags=())
        # 검색어와 일치하는 row만 선택
        found_rows = []
        for row in tree.get_children():
            item = tree.item(row)
            values = item['values']
            if search_term.lower() in str(values).lower():
                found_rows.append(row)
                tree.item(row, tags=('found',))
        if found_rows:
            # 검색 결과를 모두 찾은 경우
            if len(found_rows) > 1:
                # 일치하는 검색 결과를 선택하고 해당 위치로 이동
                if search_and_select.current_result_index >= len(found_rows):
                    search_and_select.current_result_index = 0
                result_row = found_rows[search_and_select.current_result_index]
                search_and_select.current_result_index += 1
            # 검색 결과가 하나인 경우
            else:
                result_row = found_rows[0]
                search_and_select.current_result_index = 0
            
            tree.selection_set(result_row)
            tree.see(result_row)
            return True
        else:
            # 일치하는 검색 결과가 없으면 모든 row 표시
            for row in tree.get_children():
                tree.item(row, tags=())
            search_and_select.current_result_index = 0
            return False
    # 검색 결과의 인덱스를 저장하기 위한 변수 초기화
    search_and_select.current_result_index = 0
    def search_treeview(event=True):
        search_term = search_var.get()
        if search_term:
            found = search_and_select(tree, search_term)
            if not found:
                messagebox.showinfo("검색 결과 없음", "검색어와 일치하는 항목이 없습니다.")
        else:
            messagebox.showinfo("검색어 입력", "검색어를 입력해주세요.")
    # 검색 버튼 생성
    search_button = ttk.Button(search_popup, text='검색', command=search_treeview)
    search_button.grid(row=0, column=2, padx=10, pady=10)
    # 검색창 닫기
    def destroy_search_popup(event=True):
        search_popup.destroy()
    search_entry.bind('<Return>', search_treeview)
    search_entry.bind('<Escape>', destroy_search_popup)
root.bind('<Control-f>', search_ctrl_f)




root.mainloop()