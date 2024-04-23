import streamlit as st

# Local module
import jupy_app

st.set_page_config(
        page_title="JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant",
        page_icon="🔗",
        layout="wide",
    )

st.subheader("Connecter votre notebook")
st.text_input("", key="path_input", on_change=jupy_app.submit_path, placeholder= "Insérez le chemin de votre Notebook Jupyter ici")
st.button("Connecter", on_click=jupy_app.submit_path)
if "path" in st.session_state: 
    st.write("✅ Chemin activé")
    st.write(f"Directory : {st.session_state.path}")