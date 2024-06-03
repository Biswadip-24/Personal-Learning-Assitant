import streamlit as st
from data_processor import generate_questions, get_answers

@st.experimental_fragment
def app_get_questions(uploaded_file):
    with st.spinner("Generating questions..."):
        questions = generate_questions(uploaded_file)
        st.session_state.questions = questions
        print("Questions added to session state")
        print(st.session_state.questions)
        # st.write("Questions generated successfully!")
        
        
    text = ""
    for i in range(len(st.session_state.questions)):
        text += str(i+1) + ". "+st.session_state.questions[i] + "\n"
    st.text_area("Questions", text, height=400)

@st.experimental_fragment
def app_select_questions():
    print("Current Session state questions 2 : " + str(st.session_state.questions))
    if st.session_state.questions:
        # Create a multi select spinner to choose from the questions
        selected_questions = st.multiselect("Select a question to ask", st.session_state.questions)
        # st.write(selected_questions)
        

        if st.button("Ask"):
            response = get_answers(selected_questions)

            for i in range(len(selected_questions)):
                st.write("Question "+str(i+1)+". "+selected_questions[i])
                with st.chat_message("ai"):
                    st.markdown(response[i])

def main():
    st.set_page_config(page_title="Personal Learning Assistant", page_icon=":brain:")
    st.title("Personal Learning Assistant")
    uploaded_file = st.file_uploader("Upload your study material here", type=["pdf"])

    st.session_state.questions = []

    if uploaded_file is not None:

        if "questions" not in st.session_state:
            st.session_state.questions = []

        print("Current Session state questions 1 : " + str(st.session_state.questions))
        app_get_questions(uploaded_file)
        app_select_questions()

if __name__ == "__main__":
    main()