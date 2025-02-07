
import streamlit as st

# Function to calculate Safe HP Range
def calculate_safe_hp(level, defense, sp_def):
    # AncientPower Max Damage Calculation (Gen 3)
    ancient_power_damage = (((2 * level / 5 + 2) * 60 * 74 / defense) / 50 + 2) * 2 * 1.06
    min_safe_hp = int(ancient_power_damage) + 1  # Add 1 to ensure survival

    # Psychic Min Damage Calculation (Gen 3)
    psychic_damage = (((2 * level / 5 + 2) * 90 * 74 / sp_def) / 50 + 2) * 1.5 * 0.85
    max_safe_hp = int(psychic_damage)  # AI must always see a kill

    return min_safe_hp, max_safe_hp

# Streamlit UI
st.title("Pelipper Safe HP Calculator (Gen 3 - Pokémon Emerald)")
st.write("Enter your Pelipper's stats to determine its correct Safe HP range.")

# User Inputs
level = st.number_input("Pelipper's Level", min_value=25, max_value=42, value=30, step=1)
defense = st.number_input("Pelipper's Defense Stat", min_value=30, max_value=100, value=60, step=1)
sp_def = st.number_input("Pelipper's Special Defense Stat", min_value=30, max_value=100, value=50, step=1)

# Calculate Safe HP Range when button is clicked
if st.button("Calculate Safe HP Range"):
    min_hp, max_hp = calculate_safe_hp(level, defense, sp_def)

    if min_hp > max_hp:
        st.error("⚠️ This Pelipper is NOT viable! There is no valid Safe HP range.")
    else:
        st.success(f"✅ Safe HP Range: {min_hp} - {max_hp}")
        st.info("Ensure Pelipper's HP is in this range before battle to bait Psychic properly.")
