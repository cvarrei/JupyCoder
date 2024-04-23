import speech_recognition as sr
import pyperclip
import streamlit as st


def transcribe_speech() -> str:
    """
    Transcribe speech to text with Google Web Speech API.

    Returns:
        str: The transcribed text.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Dites quelque chose...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        st.write("Analyse de l'audio...")
        text = recognizer.recognize_google(audio_data, language='fr-FR')
        st.write("Vous avez dit : ", text)
        return text
    except sr.UnknownValueError:
        st.write("Impossible de comprendre l'audio")
        return ""
    except sr.RequestError as e:
        st.write("Erreur lors de la requête à l'API Google : ", e)
        return ""

def save_to_history(request: str) -> None:
    """
    Save a request to the session history.

    Args:
        request (str): The request to be saved.

    Returns:
        None
    """
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if request:
        st.session_state['history'].append(request)


def display_history(agent):
    """
    Display the history of requests in a Streamlit app.

    Args:
        agent: The agent object.

    Returns:
        None
    """
    col1, col2, col3 = st.columns([7, .5, 3])
    # Create a container with a border
    with col1:
        with st.container():
            st.markdown('<br></br>', unsafe_allow_html=True)
            col_d, col_b = st.columns([4, 1])
            with col_d:
                st.markdown("Pour retourner en arrière dans le notebook, cliquez sur le bouton:")
            with col_b:
                if st.button("⚠️ Précédent"):
                    agent.last_version()
            st.markdown('<br></br>', unsafe_allow_html=True)
        with st.container(border = False):
            st.markdown("---")  # Add a horizontal line for separation
            # Create a horizontal layout
            header_col, download_col = st.columns([12, 3])

            # Display the "Historique" title
            with header_col:
                st.subheader("Historique :")

            # Display the download button in the right column
            with download_col:
                if 'history' in st.session_state:
                    download_history()
            if 'history' in st.session_state:
            # Reverse the order of the history list
                reversed_history = reversed(st.session_state['history'])
                for idx, request in enumerate(reversed_history):
                    # Use columns to align the copy button to the right side
                    col1a, col1b = st.columns([12, 2])
                    # Display the request
                    with col1a:
                        st.write(f"{request}")
                        st.markdown("---")
                    # Add a button to copy the request to clipboard
                    if col1b.button(f"Copier", key=f"copy_button_{idx}"):
                        pyperclip.copy(request)

        with col3:
            st.subheader("Aide :")
            st.markdown("<b>Création d'une cellule / markdown</b>", unsafe_allow_html=True)
            st.text("• Crée une cellule ...")
            st.text("• Crée un markdown ...")
            st.markdown("""
                        <b>Requête sur une cellule / markdown spécifique</b><br>
                        <span style='font-size: 12px;'><i>Clés Jupycoder possibles : ## A MODIFIER ## ; ## A SUPPRIMER ## ; ## A EXPLIQUER ##</i></span>""", unsafe_allow_html=True)
            st.text("• Modifie ... avec la clé Jupycoder")
            st.text("• Supprime ... avec la clé Jupycoder")
            st.text("• Explique ... avec la clé Jupycoder")
            st.markdown("<b>Requête sur la dernière cellule / markdown</b>", unsafe_allow_html=True)
            st.text("• Modifie la dernière cellule ...")
            st.text("• Supprime la dernière cellule ...")
            st.text("• Expliquer la dernière cellule ...")
            st.markdown("<b>Expliquer le notebook</b>", unsafe_allow_html=True)
            st.text("• Résume le notebook")


def download_history() -> None:
    """
    Download the requests history as a text file.

    Returns:
        None
    """
    if 'history' in st.session_state:
        history = st.session_state['history']
        history_str = '\n'.join(history)
        st.download_button(
            label="Télécharger",
            data=history_str,
            file_name='history.txt',
            mime='text/plain',
        )

def submit_path():
    """
    Submit the Jupyter Notebook path provided by the user.

    Returns:
        None
    """
    if "path" not in st.session_state:
            st.session_state.path = ""
    if st.session_state.path_input:
        st.session_state.path = st.session_state.path_input

def submit_token():
    """
    Submit the HuggingFace Inference API token provided by the user.

    Returns:
        None
    """
    if "token" not in st.session_state:
            st.session_state.token = ""
    if st.session_state.token_input:
        st.session_state.token = st.session_state.token_input
        st.session_state.token_input = ""

def clear() -> None:
    """ 
    Clear the input.
    
    Returns:
        None
    """
    st.session_state.widget = ""