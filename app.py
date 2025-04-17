import streamlit as st
import pandas as pd

st.title("Cumulative P-TOTAL Calculator")

# Input for number of steps
n = st.number_input("Number of Steps (n):", min_value=1, value=56)

# Initialize table if not in session state
if "ptable" not in st.session_state:
    st.session_state.ptable = pd.DataFrame({
        "P-STEP (%)": [80, 85, 90, 95, 99, 99.5, 99.9, 99.95],
        "Cumulative P-TOTAL": [None] * 8
    })

# Store original before editing
original_df = st.session_state.ptable.copy()

# Editable table
st.session_state.ptable = st.data_editor(
    st.session_state.ptable,
    num_rows="dynamic",
    key="data_editor"
)

# Calculate when button is pressed
if st.button("Calculate"):
    df = st.session_state.ptable.copy()
    
    for i, row in df.iterrows():
        try:
            old_row = original_df.iloc[i] if i < len(original_df) else pd.Series()
            new_pstep = row["P-STEP (%)"]
            new_ptotal = row["Cumulative P-TOTAL"]

            if pd.notna(new_pstep) and (
                pd.isna(old_row.get("P-STEP (%)")) or new_pstep != old_row.get("P-STEP (%)")
            ):
                # User changed P-STEP
                p_step = float(new_pstep) / 100
                p_total = 100 * (p_step ** n)
                df.at[i, "Cumulative P-TOTAL"] = round(p_total, 3)
            elif pd.notna(new_ptotal):
                # User changed P-TOTAL
                p_total = float(new_ptotal) / 100
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
