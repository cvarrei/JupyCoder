import streamlit as st

def main():
    st.set_page_config(
        page_title="JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant",
        page_icon="🎙️",
        layout="wide",
    )

    st.title("JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant")
   
    st.write("""L'application JupyCoder est un outil innovant conçu pour aider les développeurs à générer du code rapidement et efficacement en utilisant un assistant virtuel.""")
    st.write("""Les utilisateurs peuvent interagir avec l'assistant pour exprimer leurs besoins en matière de code.""")
    st.write("""Par la suite, JupyCoder permet au code généré d'être automatiquement envoyé dans votre notebook.""")
    st.markdown("**Commencez par connecter votre notebook à l'application (onglet 1), puis ensuite rentrez votre clé API HuggingFace Inference (onglet 2).**")

if __name__ == "__main__":
    main()