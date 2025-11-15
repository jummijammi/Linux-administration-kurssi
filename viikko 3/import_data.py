import pandas as pd
import mysql.connector


df = pd.read_csv("meteorite_landings.csv", low_memory=False)


df['year_raw'] = df.get('year')  
df['year'] = pd.to_numeric(df['year'], errors='coerce')

#
df = df.dropna(subset=['year'])


df['year'] = df['year'].astype(int)


df['mass (g)'] = pd.to_numeric(df.get('mass (g)'), errors='coerce')
df = df.dropna(subset=['mass (g)'])

df['reclat'] = pd.to_numeric(df.get('reclat'), errors='coerce')
df['reclong'] = pd.to_numeric(df.get('reclong'), errors='coerce')

#  Yhdistä MySQL, vaidettu käyttäjätiedot githubiin.
conn = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="meteorites"
)
cursor = conn.cursor()


for i, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO landings (name, id_code, nametype, recclass, mass_g, fall_status, year, reclat, reclong)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get('name'),
            row.get('id'),
            row.get('nametype'),
            row.get('recclass'),
            row.get('mass (g)'),
            row.get('fall'),
            row.get('year'),
            row.get('reclat'),
            row.get('reclong'),
        ))
    except mysql.connector.Error as err:
        print(f"Rivi ohitettu: {err}")

conn.commit()
cursor.close()
conn.close()

print(f"{len(df)} riviä tuotu onnistuneesti.")
