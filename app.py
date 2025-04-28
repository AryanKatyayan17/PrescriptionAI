import streamlit as st
from agents.agent_runner import run_agent

if "history" not in st.session_state:
    st.session_state.history=[]

st.set_page_config(page_title="PrescriptionAI", layout="centered")

st.title("AI Prescription Assistant")
st.markdown("Ask any medical question based on medical records and drug interactions")

example_queries=[
    "What is Metformin used for?",
    "What can I prescribe for a diabetic patient with high blood pressure?",
    "Does Lisinopril interact with Ibuprofen?",
    "What drugs are mentioned in the patient history?"
]

st.markdown("Example Queries")
selected_example=st.selectbox("Choose an example:", [""] + example_queries)

user_input=st.text_input("Enter your medical question:", selected_example if selected_example else "")

response_container=st.container()
context_cotainer=st.expander("View Retrieved Patient Records",expanded=False)

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Running your question..."):
            final_answer,retrieved_context=run_agent(user_input)

            st.session_state.history.append({
                "query":user_input,
                "response":final_answer,
                "context":retrieved_context
            })

    else:
        st.warning ("Please enter a queyry to continue")

if st.session_state.history:
    st.markdown("---")
    st.markdown("Chat History")

    for i,entry in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{entry['query']}",expanded=False):
            st.markdown(f"**Response:** {entry['response']}")
            st.markdown("---")
            st.markdown("**Retrieved Patient Context:**")
            st.markdown(entry['context'])
