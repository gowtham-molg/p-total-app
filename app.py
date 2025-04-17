import streamlit as st
import pandas as pd

# Set page title
st.title("Cumulative P-TOTAL From P-STEP")

# Default values
DEFAULT_PSTEPS = [80, 85, 90, 95, 99, 99.5, 99.9, 99.95]

# Number of steps input
n = st.number_input("Number of Steps (n):", min_value=1, value=56)

# Initialize the table if not present
if "ptable" not in st.session_state:
    st.session_state.ptable = pd.DataFrame({
        "P-STEP (%)": DEFAULT_PSTEPS,
        "Cumulative P-TOTAL": [None] * len(DEFAULT_PSTEPS)
    })

# Editable table
edited_df = st.data_editor(
    st.session_state.ptable,
    num_rows="dynamic",
    key="editor"
)

# Calculate button
if st.button("Calculate"):
    df = edited_df.copy()
    for i, row in df.iterrows():
        try:
            pstep = row["P-STEP (%)"]
            ptotal = row["Cumulative P-TOTAL"]

            if pd.notna(pstep):
                # Forward calculation
                p = float(pstep) / 100
                p_total = 100 * (p ** n)
                df.at[i, "Cumulative P-TOTAL"] = round(p_total, 3)
            elif pd.notna(ptotal):
                # Reverse calculation
                p_total = float(ptotal) / 100
                if p_total <= 0:
                    df.at[i, "P-STEP (%)"] = "Invalid"
                else:
                    p_step = p_total ** (1 / n)
                    df.at[i, "P-STEP (%)"] = round(p_step * 100, 3)
        except:
            df.at[i, "Cumulative P-TOTAL"] = "Err"
            df.at[i, "P-STEP (%)"] = "Err"

    st.session_state.ptable = df
    st.success("Table updated.")
