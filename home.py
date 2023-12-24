import streamlit as st
from sdg_data import GOALS
from run_scrape import run
import time

select_goals_mapping = {}
select_goals = []
for g in GOALS:
  select_goals.append(GOALS[g]["goal"])
  select_goals_mapping[GOALS[g]["goal"]] = g

if 'submitted' not in st.session_state:
  st.session_state.clicked = False
  st.session_state.got_data = None

def click_button():
  st.session_state.clicked = True

st.title("Evaluate a Company's Efforts in Supporting the UN's SDGs.")
form_placeholder = st.empty()
st.session_state.clicked = False
with form_placeholder.container():
  with st.form("my_form"):
    st.subheader("Select the SDG and company you want to investigate")
    st.text_input('Company Name', placeholder="Type Company Name", key='company')
    st.selectbox(
      "Select an SDG Goal to evaluate",
      tuple(select_goals),
      index=None,
      placeholder="Select an SDG goal...",
      key='sdg'
    )
    submitted = st.form_submit_button("Submit", on_click=click_button)
  if submitted:
    form_placeholder.empty()
    sdg = st.session_state.sdg
    company = st.session_state.company
    with form_placeholder.container():
      st.markdown(f" ##### The company you've entered is: `{company}`")
      st.markdown(f" ##### The SDG you selected is: `{sdg}`")
      with st.spinner('Processing, please wait...'):
        st.session_state.got_data = run(select_goals_mapping[st.session_state.sdg], st.session_state.company)
    form_placeholder.empty()
    with form_placeholder.container():
      st.markdown(f" ##### The company you've entered is: `{company}`")
      st.markdown(f" ##### The SDG you selected is: `{sdg}`")
      st.write(f"{st.session_state.got_data}")
    st.session_state.submitted = False

st.divider()
