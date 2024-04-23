from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any

def chain_router(llm: Any, 
                 query:str) -> str:
    """
    Create the LLMChain to query the LLM to select the adequate function to realize the user's query and invoke it.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        query (str): The users' query

    Returns:
        str: The action or function corresponding to the query.
    """
    prompt_router =  """[[INST] Identifie l'action à réaliser en fonction de "QUERY" puis donnes le nom de la fonction à choisir.
    L'utilisateur doit explicitement demander une mise à jour pour utiliser update_last_cell ou update_cell, sinon, il faut toujours créer une nouvelle cellule.
    L'utilisateur doit demander explicitement un markdown pour utiliser une cellule en relation avec les markdowns.
    Si l'utilisateur précise une cellule avec une clé JupyCoder, utilises update_selected_cell, update_selected_markdown ou delete_selected_cell.
    N'ajoute pas d'explication. Se limiter au nom de la requête.
    Si l'utilisateur, précise qu'il fait référence à la dernière cellule, prends les fonctions correspondantes: update_last_cell, update_last_markdown, delete_last_cell ou explain_last_cell.
    
    Voici les fonctions disponibles pour créer une cellule :
    - create_code_cell : Créer une cellule de code avec de nouvelles lignes de code
    - create_markdown : Créer une cellule markdown avec du nouveau texte (explication, contexte)
    
    Voici les fonctions disponibles pour modifier une cellule: 
    - update_last_cell : Mise à jour de la dernière cellule du carnet
    - update_last_markdown : Mise à jour de la dernière cellule markdown
    - update_selected_cell : Met à jour de la cellule de code qui a la clé JupyCoder
    - update_selected_markdown : Met à jour du markdown qui a la clé JupyCoder
    
    Voici les fonctions disponibles pour supprimer une cellule:
    - delete_last_cell : Supprime la dernière cellule
    - delete_selected_cell : Supprime la cellule qui a la clé JupyCoder

    Voici les fonctions pour expliquer une cellule:
    - explain_last_cell : Explique la dernière cellule
    - explain_selected_cell : Explique la cellule qui a la clé JupyCoder

    Voici les fonctions pour résumer le notebook.
    - summary_all : Créer un résumé de tous le notebook
    
    Utilise une fonction des listes précédentes pour répondre à la "QUERY" suivante. 
    "QUERY": 
    {query}
    [/INST] 
    
    Nom de la fonction à choisir:
    """
    prompt_router_templ = PromptTemplate(input_variables=["query"], template=prompt_router)
    chain_router = LLMChain(prompt=prompt_router_templ, llm=llm)
    answer = chain_router.invoke({"query": query})

    return answer["text"].split("choisir:")[1].strip().replace('\_', '_')


def chain_code_generation(llm: Any, 
                          query:str,
                    history: str) -> str:
    """
    Create the LLMChain to generate python code lines based on the user's query and invoke it.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        query (str): The users' query
        history (str): Previous code cells to add context to the new code cell.

    Returns:
        str: The python code lines
    """

    prompt_coder =  """[INST]Génères uniquement les lignes de code python pour réaliser la requête suivante : {query}. 
    Voici l'historique des dernières commandes, si besoin, sers en toi pour améliorer le code: 
    {history}

    Ajoutes du texte supplémentaire comme commentaire si besoin. 
    Si tu crées une fonction, ajoutes un docstring et penses à retourner la variable d'intérêt. 

    Limite ta réponse à des lignes de code. N'ajoutes pas d'explication.
    [/INST] 

    Le code python est:"""
    prompt_coder_templ = PromptTemplate(input_variables=["query", "history"], template=prompt_coder)
    chain_coder = LLMChain(prompt=prompt_coder_templ, llm=llm)
    answer = chain_coder.invoke({"query": query, "history": history})
    response = answer["text"].split("est:")[1].strip()
    if 'Explanation' in response:
        response = response.split("Explanation:")[0].strip()
    if 'Notes' in response:
        response = response.split("Notes:")[0].strip()
    if 'Ce code' in response:
        response = response.split("Ce code")[0].strip()
    if 'Le code' in response:
        response = response.split("Le code")[0].strip()
    if 'Ici' in response:
        response = response.split("Ici")[0].strip()
    if 'This line' in response:
        response = response.split("This line")[0].strip()
    if 'This code' in response:
        response = response.split("This code")[0].strip()
    if 'Explication' in response:
        response = response.split("Explication")[0].strip()
    if 'Notez'  in response:
        response = response.split("Explication")[0].strip()
    if 'Comments:'  in response:
        response = response.split("Comments:")[0].strip()

    return response

def chain_code_update(llm: Any, 
                query: str, 
                code:str) -> str:
    """
    Create the LLMChain to update the selected code cell and invoke it.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        query (str): The users' query
        code (str): The code lines to update

    Returns:
        str: The  updated python code lines
    """        
    prompt_explanation =  """[INST]Update the code to respect the following query : {query}.
    Do not add additional text or explanation. Add commentaries if necessary.
    Do not explain the arguments of the code and do not explain the change lines. Do not use a list.
    
    {code}
    
    Limit yourself to the code lines. 
    [/INST] 

    Updated Code:"""
    prompt_explanation_templ = PromptTemplate(input_variables=["query", "code"], template=prompt_explanation)
    chain_explanation = LLMChain(prompt=prompt_explanation_templ, llm=llm)
    answer = chain_explanation.invoke({"query": query, "code": code})
    response = answer["text"].split("Code:")[1].strip()
    if 'Explanation' in response:
        response = response.split("Explanation:")[0].strip()
    if 'Notes' in response:
        response = response.split("Notes:")[0].strip()
    if 'Ce code' in response:
        response = response.split("Ce code")[0].strip()
    if 'Le code' in response:
        response = response.split("Le code")[0].strip()
    if 'Ici' in response:
        response = response.split("Ici")[0].strip()
    if 'This line' in response:
        response = response.split("This line")[0].strip()
    if 'This code' in response:
        response = response.split("This code")[0].strip()
    if 'Explication' in response:
        response = response.split("Explication")[0].strip()
    if 'Notez'  in response:
        response = response.split("Explication")[0].strip()
    if 'Comments:'  in response:
        response = response.split("Comments:")[0].strip()

    return response


def chain_markdown_generation(llm: Any,
                        query:str) -> str:
    """
    Create the LLMChain to generate markdown content based on the user's query and invoke it.


    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        query (str): The users' query

    Returns:
        str: The markdown content
    """      
    prompt_markdown =  """[INST]Ta tâche est de créer un document markdown.
    {query}.
    Sois bref. Limites toi à un paragraphe. N'ajoutes pas d'onglet Explication.
    [/INST] 

    Markdown:"""
    prompt_markdown_templ = PromptTemplate(input_variables=["query"], template=prompt_markdown)
    chain_markdown = LLMChain(prompt=prompt_markdown_templ, llm=llm)
    answer = chain_markdown.invoke({"query": query})

    return answer["text"].split("Markdown:")[1].strip()

def chain_markdown_update(llm, 
                        text: str,
                        query:str) -> str:
    """
    Create the LLMChain to update the selected markdown cell and invoke it.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        text (str): The markdown content to update
        query (str): The users' query

    Returns:
        str: The markdown content updated
    """   

    prompt_markdown_upd =  """[INST]{query}.
    
    Markdown: 
    {markdown}

    Sois bref. Limites toi à un paragraphe.
    [/INST] 

    Markdown modifié:"""
    prompt_markdown__updtempl = PromptTemplate(input_variables=["query", "markdown"], template=prompt_markdown_upd)
    chain_markdown = LLMChain(prompt=prompt_markdown__updtempl, llm=llm)
    answer = chain_markdown.invoke({"query": query, "markdown":text})

    return answer["text"].split("modifié:")[1].strip()

def chain_code_explanation(llm, 
                        code:str) -> str:
    """
    Create the LLMChain to explain the selected code cell.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        code (str): The code cell to explain

    Returns:
        str: The code cell explanation
    """       
    prompt_explanation =  """[INST]Tu dois expliquer en quelques lignes le code suivant:
    {code}
    
    [/INST] 

    Explication:"""
    prompt_explanation_templ = PromptTemplate(input_variables=["query"], template=prompt_explanation)
    chain_explanation = LLMChain(prompt=prompt_explanation_templ, llm=llm)
    answer = chain_explanation.invoke({"code": code})

    return answer["text"].split("Explication:")[1].strip()

def chain_summary(llm: Any, 
            list_codes: list[str]) -> str:
    """
    Create the LLMChain to explain all the code cells of the notebook.

    Args:
        llm (Any): The large language model object for the LangChain's LLMChain function.
        code (str): The code cells of the notebook

    Returns:
        str: The notebook summary

    """   
    prompt_summary =  """[INST]Ton rôle est de résumer  en language naturel les commandes python réalisée dans ce notebook:
    {codes}
    
    Utilise simplement les lignes de code données. S'il n'y a pas de code, expliques que le notebook est vide.
    Limite toi à un paragraphe. 
    [/INST] 

    Réponse:
    Dans ce notebook,"""
    prompt_summary_templ = PromptTemplate(input_variables=["codes"], template=prompt_summary)
    chain_summary = LLMChain(prompt=prompt_summary_templ, llm=llm)
    answer = chain_summary.invoke({"codes": list_codes})

    return answer["text"].split("Réponse:")[1].strip()       