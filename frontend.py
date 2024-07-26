import streamlit as st
import requests


st.title("Question and Answer")


question = st.text_input("Ask a question:")

if st.button("Get Answer"):
    if question:
        
        response = requests.post(
            "http://localhost:5000/qna",
            json={"question": question}
        )
        
        if response.status_code == 200:
            answer = response.json().get('Answer')
            st.write(f"Answer: {answer}")
        else:
            st.write("Error: Unable to get the answer.")
    else:
        st.write("Please enter a question.")
