import streamlit as st
import pandas as pd

# Set page title
st.title("Cumulative P-TOTAL Calculator")

# Input for number of steps
n = st.number_input("Number of Steps (n):", min_value=1, value=56)

# Initialize table in session state
if "ptable" not in st.session_state:
    st.session_state.ptable = pd.DataFrame({
        "P-STEP (%)": [80, 85, 90, 95, 99, 99.5, 99.9, 99.95],
        "Cumulative P-TOTAL": [None] * 8
    })

# Show editable table
st.subheader("Edit table below")
st.session_state.ptable = st.data_editor(
    st.session_state.ptable,
    num_rows="dynamic",
    key="data_editor"
)

# Calculate button
if st.button("Calculate"):
    df = st.session_state.ptable.copy()
    for i, row in df.iterrows():
        try:
            if pd.notna(row["P-STEP (%)"]):
                p_step = float(row["P-STEP (%)"]) / 100
                p_total = 100 * (p_step ** n)
                df.at[i, "Cumulative P-TOTAL"] = round(p_total, 3)
            elif pd.notna(row["Cumulative P-TOTAL"]):
                p_total = float(row["Cumulative P-TOTAL"]) / 100
                if p_total <= 0:
                    df.at[i, "P-STEP (%)"] = "Invalid"
                else:
                    p_step = p_total ** (1 / n)
                    df.at[i, "P-STEP (%)"] = round(p_step * 100, 3)
        except:
            df.at[i, "Cumulative P-TOTAL"] = "Err"
            df.at[i, "P-STEP (%)"] = "Err"
    
    # Update session state
    st.session_state.ptable = df
    st.success("Table updated.")
