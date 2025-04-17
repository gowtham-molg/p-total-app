import streamlit as st
import pandas as pd

st.title("Cumulative P-TOTAL Calculator (Two-Way)")

# Input for number of steps
n = st.number_input("Number of Steps (n):", min_value=1, value=56)

# ---------- Table 1: P-STEP → P-TOTAL ----------
st.subheader("P-STEP (%) → Cumulative P-TOTAL")

if "pstep_table" not in st.session_state:
    st.session_state.pstep_table = pd.DataFrame({
        "P-STEP (%)": [80, 85, 90, 95, 99, 99.5, 99.9, 99.95],
        "Cumulative P-TOTAL": [None] * 8
    })

pstep_df = st.data_editor(
    st.session_state.pstep_table,
    num_rows="dynamic",
    key="pstep_editor"
)

if st.button("Calculate P-TOTAL"):
    for i, row in pstep_df.iterrows():
        try:
            if pd.notna(row["P-STEP (%)"]):
                p = float(row["P-STEP (%)"]) / 100
                total = 100 * (p ** n)
                pstep_df.at[i, "Cumulative P-TOTAL"] = round(total, 3)
        except:
            pstep_df.at[i, "Cumulative P-TOTAL"] = "Err"
    st.session_state.pstep_table = pstep_df
    st.success("Cumulative P-TOTALs updated.")

# ---------- Table 2: P-TOTAL → P-STEP ----------
st.subheader("Cumulative P-TOTAL → P-STEP (%)")

if "ptotal_table" not in st.session_state:
    st.session_state.ptotal_table = pd.DataFrame({
        "Cumulative P-TOTAL": [90, 95, 98, 99, 99.5],
        "P-STEP (%)": [None] * 5
    })

ptotal_df = st.data_editor(
    st.session_state.ptotal_table,
    num_rows="dynamic",
    key="ptotal_editor"
)

if st.button("Calculate P-STEP"):
    for i, row in ptotal_df.iterrows():
        try:
            if pd.notna(row["Cumulative P-TOTAL"]):
                total = float(row["Cumulative P-TOTAL"]) / 100
                if total <= 0:
                    raise ValueError
                p = total ** (1 / n)
                ptotal_df.at[i, "P-STEP (%)"] = round(p * 100, 3)
        except:
            ptotal_df.at[i, "P-STEP (%)"] = "Err"
    st.session_state.ptotal_table = ptotal_df
    st.success("P-STEPs updated.")
