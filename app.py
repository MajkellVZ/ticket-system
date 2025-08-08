import pandas as pd
import streamlit as st
from core.filter import load_data, apply_filters
from core.gemini import run_gemini_prompt
from core.prompt import format_suggestion_prompt, format_main_causes_prompt

st.title("Ticket Filtering System")

df = load_data()

st.sidebar.header("Apply Filters")

priority = st.sidebar.multiselect("Priority", options=df["priority"].dropna().unique())
category = st.sidebar.multiselect("Category", options=df["category"].dropna().unique())
subcategory = st.sidebar.multiselect("Subcategory", options=df["subcategory"].dropna().unique())
assignment_group = st.sidebar.multiselect("Assignment Group", options=df["assignment_group"].dropna().unique())
state = st.sidebar.multiselect("State", options=df["state"].dropna().unique())

created_range = st.sidebar.date_input("Created On Range", [])
updated_range = st.sidebar.date_input("Updated On Range", [])

filters = {
    "priority": priority,
    "category": category,
    "subcategory": subcategory,
    "assignment_group": assignment_group,
    "state": state,
}

if len(created_range) == 2:
    filters["created_range"] = tuple(pd.to_datetime(created_range))

if len(updated_range) == 2:
    filters["updated_range"] = tuple(pd.to_datetime(updated_range))

filtered_df = apply_filters(df, filters)

st.subheader("Filtered Results")
st.write(f"{len(filtered_df)} rows found")
st.dataframe(filtered_df)

st.subheader("Suggest Fixes for Causes")

if st.button("Generate Main Causes and Fix Suggestions"):

    if filtered_df.empty:
        st.warning("No filtered data to analyze.")
    else:
        causes_prompt = format_main_causes_prompt(filtered_df)

        with st.spinner("🔍 Identifying root causes..."):
            causes_response = run_gemini_prompt(causes_prompt)

        st.subheader("Gemini-Generated Causes")
        st.code(causes_response)

        causes_list = [line.strip("-• ").strip() for line in causes_response.splitlines() if line.strip()]
        if causes_list:
            solution_prompt = format_suggestion_prompt(causes_list)

            with st.spinner("💡 Suggesting solutions..."):
                solution_response = run_gemini_prompt(solution_prompt)

            st.subheader("💡 Gemini-Suggested Fixes")
            st.write(solution_response)
        else:
            st.warning("No causes found in Gemini response to generate suggestions.")
