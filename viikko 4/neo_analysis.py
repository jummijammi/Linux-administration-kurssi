import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

# --- TIETOKANTA ---
host = "localhost"
user = "user"// muutettu käyttäjä githubiin
password = "password"//muutettu salasana githubiin
database = "meteorites"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

st.title("🚀 NASA NEO & Säädata – Analyysit")


# ---------------------------------------------------
#                  VÄLILEHDET
# ---------------------------------------------------
tab1, tab2 = st.tabs(["☄️ NEO-data", "🌦️ Säädata"])


# ---------------------------------------------------
#                     TAB 1 — NEO
# ---------------------------------------------------
with tab1:
    st.header("☄️ NASA Near Earth Objects (NEO)")

    try:
        df = pd.read_sql("SELECT * FROM neo_objects", engine)

        if df.empty:
            st.warning("NEO-taulu on tyhjä.")
        else:
            st.success(f"Ladattu {len(df)} NEO-objektia NASA API:sta")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Virhe tietokantayhteydessä: {str(e)}")


# ---------------------------------------------------
#                     TAB 2 — Weather
# ---------------------------------------------------
with tab2:
    st.header("🌦️ OpenWeatherMap – Säädata")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",// muutettu käyttäjä githubiin
            password="password", //muutettu salasana githubiin
            database="weather_db"
        )

        df_weather = pd.read_sql(
            "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50",
            conn
        )
        conn.close()

        if df_weather.empty:
            st.warning("Säädata-taulu on tyhjä.")
        else:
            st.dataframe(df_weather)

    except Exception as e:
        st.error(f"Virhe säädatan hakemisessa: {str(e)}")
