import streamlit as st
import pandas as pd

# Default values
DEFAULT_PSTEPS = [80, 85, 90, 95, 99, 99.5, 99.9, 99.95]

st.title("Cumulative P-TOTAL Calculator")

# Input for number of steps
n = st.number_input("Number of Steps (n):", min_value=1, value=56)

# Editable table
st.subheader("Edit P-STEP (%) or Cumulative P-TOTAL")
df = pd.DataFrame({
    "P-STEP (%)": DEFAULT_PSTEPS,
    "Cumulative P-TOTAL": [None] * len(DEFAULT_PSTEPS)
})

edited_df = st.data_editor(df, num_rows="dynamic", key="ptable")

# Button to trigger calculation
if st.button("Calculate"):
    for i, row in edited_df.iterrows():
        try:
            if pd.notna(row["P-STEP (%)"]):
                p_step = float(row["P-STEP (%)"]) / 100
                p_total = 100 * (p_step ** n)
                edited_df.at[i, "Cumulative P-TOTAL"] = round(p_total, 3)
            elif pd.notna(row["Cumulative P-TOTAL"]):
                p_total = float(row["Cumulative P-TOTAL"]) / 100
                if p_total <= 0:
                    edited_df.at[i, "P-STEP (%)"] = "Invalid"
                else:
                    p_step = p_total ** (1 / n)
                    edited_df.at[i, "P-STEP (%)"] = round(p_step * 100, 3)
        except:
            edited_df.at[i, "Cumulative P-TOTAL"] = "Err"
            edited_df.at[i, "P-STEP (%)"] = "Err"

# No second table display here — only editable table above
