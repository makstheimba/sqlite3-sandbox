import sqlite3
from random import choice

def name_generator(num):
    firstnames = ('Augusta', 'Leonard', 'Leilani', 'Jeanine', 'Cassi', 'Librada', 'Ruth', 'Adriana', 'Mindi', 'Nell')
    lastnames = ('Smith', 'Jones', 'Brown', 'Johnson', 'Williams', 'Miller', 'Davis', 'Taylor', 'Wilson')
    for i in range(num):
        yield (choice(firstnames), choice(lastnames))

#Максимальное количество записей в таблице
max_entries = 20

#Создание двух БД в RAM и заполнение данными
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
for table_name in ("ppl1", "ppl2"):
    cur.execute("create table {tn} (id integer primary key, first text, last text, "
                "unique(first, last) on conflict ignore)".format(tn = table_name))
    cur.executemany("insert into {tn} (first, last) values (?, ?)".format(tn = table_name), name_generator(max_entries))

#Печатаем обе таблицы
print("\nСоздание двух БД")
print("\nppl1", *cur.execute("select * from ppl1").fetchall(), sep="\n")
print("\nppl2", *cur.execute("select * from ppl2").fetchall(), sep="\n")

#Находим одинаковые записи в таблицах
print("\nОдинаковые записи в таблицах")
cur.execute("select ppl1.id, ppl2.id, ppl1.first, ppl1.last from ppl1, ppl2 "
            "where ppl1.first = ppl2.first and ppl1.last = ppl2.last")
print("\nid1, id2, first, last", *cur.fetchall(), sep="\n")

#Удаляем из ppl1 записи, которые есть в ppl2
print("\nУдаляем из ppl1 записи, которые есть в ppl2")
cur.execute("delete from ppl1 where exists (select * from ppl2 where ppl1.last = ppl2.last and ppl1.first = ppl2.first)")
print("\nppl1", *cur.execute("select * from ppl1").fetchall(), sep="\n")

#Добавляем в ppl1 все записи с именами Ruth, Leonard или Cassi, которые есть в ppl2
print("\nДобавляем в ppl1 все записи с именами Ruth, Leonard или Cassi, которые есть в ppl2")
cur.execute("insert into ppl1 (first, last) select first, last from ppl2 where first in ('Ruth', 'Leonard', 'Cassi')")
print("\nppl1", *cur.execute("select * from ppl1").fetchall(), sep="\n")