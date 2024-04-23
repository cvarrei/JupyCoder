import streamlit as st
from langchain_community.llms import HuggingFaceHub

# Local modules
from jupycoder import JupyCoder
import jupy_app


def main():
    st.set_page_config(
        page_title="JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant",
        page_icon="🎙️",
        layout="wide",
    )

    if "token" not in st.session_state:
        st.session_state.token = ""
    st.sidebar.text_input("Insérer un token Hugging Face 🤗 :", key="token_input", on_change=jupy_app.submit_token, type = 'password')
    st.sidebar.button("Valider", on_click=jupy_app.submit_token)

    if len(st.session_state.token) > 2:
        st.sidebar.write("✅ Token activé") 
        if 'path' in st.session_state:
            llm =  HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                    huggingfacehub_api_token=st.session_state.token,
                                    model_kwargs={"temperature": 0.1, "max_new_tokens": 500})
            JupyAgent = JupyCoder(st.session_state.path, 
                                    llm)
        
    if (len(st.session_state.token) < 2) or ('path' not in st.session_state):
        st.header("👈 Merci de vous connecter à un notebook en cliquant sur l'onglet 'Connexion avec notebook' et de faire valider votre Token HuggingFace avant de procéder.")
    else:
        st.title("JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant")
        st.markdown("---")
        col1, col2 = st.columns([2, 4])

        with col1:
            st.subheader("Enregistrement voix")
            if st.button("🎙️ Enregistrer"):
                text = jupy_app.transcribe_speech()
                JupyAgent(text)
                jupy_app.save_to_history(text)

        with col2:
            if "my_text" not in st.session_state:
                    st.session_state.my_text = ""
            col2a, col2b = st.columns([7, 2])
            with col2a:
                st.subheader("Ecrire une requête")
            with col2b:

                st.button("Effacer 🗑️", on_click=jupy_app.clear)

            with st.form("my_form"):
                text_input = st.text_area("Insérez du texte ici :", key="widget")
                button_clicked = st.form_submit_button("Envoyer")
                if st.session_state.widget:
                    st.session_state.my_text = st.session_state.widget
                    jupy_app.save_to_history(st.session_state.my_text)
            
            if len(text_input) > 3 and button_clicked:
                JupyAgent(text_input)
    
    if (len(st.session_state.token) > 2) and ('path' in st.session_state):
        jupy_app.display_history(agent=JupyAgent)


if __name__ == "__main__":
    main()