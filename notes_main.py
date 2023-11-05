from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import json

app = QApplication([])

notes = {
    "Welcome" : {
        'текст' : "Это хорошо",
        'теги' : ['добро', 'инструкця']
    }
}

with open("notes_data.json", "w", encoding = "utf8") as file:
    json.dump(notes, file)

notes_win = QWidget()
notes_win.setWindowTitle('Memo')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Заметки')

button_note_create = QPushButton('Create')
button_note_del = QPushButton('Del')
button_note_save = QPushButton('Save')

field_tag = QLineEdit()
field_tag.setPlaceholderText('W t...')

field_text = QTextEdit()

button_tag_add = QPushButton('Add')
button_tag_del = QPushButton('Otcrep')
button_tag_search = QPushButton('Search...')

list_tags = QListWidget()
list_tags_lable = QLabel('List')

layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()

col2.addWidget(list_notes_label)
col2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)

row2 = QHBoxLayout()
row2.addWidget(button_note_save)

col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(list_tags_lable)
col2.addWidget(list_tags)
col2.addWidget(field_tag)

row3 = QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_note_del)

row4 = QHBoxLayout()
row4.addWidget(button_note_create)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add", "Name")
    if ok and note_name != "":
        notes[note_name] = {"текст":"", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Not selected')

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Not selected')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Not selected')

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('Not selected')

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Search" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('kys')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'kys':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Search')
        print(button_tag_search.text())
    else:
        pass

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


notes_win.show()

with open('notes_data.json', 'r', encoding='utf8') as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()