#POINT:Python の外部/標準ライブラリを読み込む仕組み。
#POINT:Python では { } ではなく インデント でブロックを表現する。
import pymssql
import datetime

#PONT:変数への代入/Pythonでは型宣言が不要
SERVER = 'localhost'       # または 'localhost\\SQLEXPRESS'
USER = 'sa'
PWD = 'Pa$$w0rd'
BDD = 'PINGOUINS'
cnx = pymssql.connect(SERVER, USER, PWD, BDD)

#POINT:cursor=>イテレーターとしてクエリの検索結果を持っている
#Combien il y a-t-il de pingouins au total ?
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(id_pingouin) AS total_pingouins FROM Pingouins;')
#ou SELECT COUNT(*) AS total_pingouins FROM Pingouins;
for row in cursor:
    print(row)
    print(row[0])

#Pour chaque espèce, combien il y a-t-il d’individus ?
#POINT: Python の辞書（dict）を使って列名でアクセスできる。/列名でアクセスできるように
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT espece, COUNT(*) AS nb_individus FROM Pingouins GROUP BY espece')
#fetchall() で結果をまとめて取得
for row in cursor.fetchall():
    print(row['espece'], row['nb_individus'])

#Combien il y a-t-il d’espèces ?
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT COUNT(DISTINCT espece) AS nb_especes FROM Pingouins')
result = cursor.fetchone()
print("Combien il y a-t-il d’espèces ? Nombre d'espèces :", result['nb_especes'])

#Pour chaque île, combien il y a-t-il d’individus ?
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT ile, COUNT(*) AS nb_individus FROM Pingouins GROUP BY ile')

for row in cursor.fetchall():
    print(row['ile'], row['nb_individus'])

# Combien il y a-t-il d’îles ?
cursor = cnx.cursor()
cursor.execute('SELECT  COUNT(DISTINCT ile) AS nb_iles FROM Pingouins;')
#ou SELECT COUNT(*) AS total_pingouins FROM Pingouins;
for row in cursor:
    print(row)
    print(row[0])

#Quelle est la longueur moyenne des becs ?
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT AVG(longueur_bec) AS longueur_moyenne FROM Pingouins WHERE longueur_bec IS NOT NULL')
result = cursor.fetchone()
#POINT:Python の print は , で複数の値を並べて出力できる。
print("Longueur moyenne des becs :", round(result['longueur_moyenne'], 2), "mm")

#Quelle est la plus grande profondeur de bec ?
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT MAX(profondeur_bec) AS profondeur_max FROM Pingouins WHERE profondeur_bec IS NOT NULL')
result = cursor.fetchone()
print("Plus grande profondeur de bec :", result['profondeur_max'], "mm")

#Combien il y a-t-il de pingouins pour chaque sexe ?
#fetchall
cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT sex, COUNT(*) AS nb_individus FROM Pingouins GROUP BY sex')

for row in cursor.fetchall():
    print(row['sex'], row['nb_individus'])

#Quel est l’âge du plus jeune pingouin ?

current_year = datetime.date.today().year

cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT MAX(annee_naissance) AS annee_plus_recente FROM Pingouins WHERE annee_naissance IS NOT NULL')
result = cursor.fetchone()

age_plus_jeune = current_year - result['annee_plus_recente']
print("Âge du plus jeune pingouin :", age_plus_jeune, "ans")


#Quel est l’âge du pingouin le plus âgé ?
#fetchone
current_year = datetime.date.today().year

cursor = cnx.cursor(as_dict=True)
cursor.execute('SELECT MIN(annee_naissance) AS annee_plus_ancienne FROM Pingouins WHERE annee_naissance IS NOT NULL')
result = cursor.fetchone()

age_plus_vieux = current_year - result['annee_plus_ancienne']
print("Âge du plus vieux pingouin :", age_plus_vieux, "ans")
