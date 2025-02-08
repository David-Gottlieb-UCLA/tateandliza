import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit App Title
st.title("Tate & Liza Pelipper Pre-Damage Calculator")

# User Input Section
level = st.number_input("Pelipper's Level", min_value=25, max_value=42, step=1, value=30)
defense = st.number_input("Pelipper's Defense Stat", min_value=40, max_value=100, step=1, value=67)
sp_def = st.number_input("Pelipper's Special Defense Stat", min_value=40, max_value=100, step=1, value=58)

# Full list of Gen 3 Natures
natures = [
    "Hardy", "Lonely", "Brave", "Adamant", "Naughty",
    "Bold", "Docile", "Relaxed", "Impish", "Lax",
    "Timid", "Hasty", "Serious", "Jolly", "Naive",
    "Modest", "Mild", "Quiet", "Bashful", "Rash",
    "Calm", "Gentle", "Sassy", "Careful", "Quirky"
]

nature = st.selectbox("Pelipper's Nature", natures, index=0)

# Function to get damage calculations from KinglerCalc
def get_damage_calculations(level, defense, sp_def, nature):
    # URL of KinglerCalc (this assumes a scrape-friendly version of the site)
    url = "https://www.kinglercalc.com"
    
    # Simulate submitting the form by passing the data in the request
    params = {
        "pokemon": "Pelipper",
        "level": level,
        "defense": defense,
        "sp_def": sp_def,
        "nature": nature,
        "opponent": "Tate & Liza's Claydol",
        "move1": "Psychic",
        "move2": "AncientPower"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            # Extract Psychic min damage and AncientPower max damage
            min_psychic = int(soup.find("span", {"id": "psychic_min"}).text.strip())
            max_ancientpower = int(soup.find("span", {"id": "ancientpower_max"}).text.strip())

            # Check viability
            if min_psychic <= max_ancientpower:
                return "Non-Viable", min_psychic, max_ancientpower

            return min_psychic, max_ancientpower
        except AttributeError:
            return None, None

    return None, None

# Fetch Damage Calculations
if st.button("Calculate Safe HP Range"):
    result = get_damage_calculations(level, defense, sp_def, nature)

    if result == "Non-Viable":
        st.error("⚠️ Your Pelipper is not viable! There is no safe HP range.")
    elif result[0] is not None and result[1] is not None:
        safe_min_hp = result[1] + 1  # Max AncientPower roll + 1
        safe_max_hp = result[0]  # Min Psychic roll

        st.success(f"✅ Safe HP Range for Pelipper: {safe_min_hp} - {safe_max_hp}")
    else:
        st.error("⚠️ Could not fetch data from KinglerCalc. Please try again later.")
