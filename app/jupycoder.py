import nbformat
import os
from typing import Any
import re

# Local Module
import chain_inferences
import notebook_modification

class JupyCoder():
    """  
    An object of a Router-based Jupyter Assistant which will infer the intention of the user's query and then realize the 
    corresponding function. 
    """

    def __init__(self, 
                 path: str,
                 llm: Any) -> None:
        self.llm =  llm
        self.path = path

    @staticmethod
    def _cleaning_code_inference(query:str) -> str:
        """
        Cleaning specific to code inference text.

        Args:
            query (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        text = query.replace('\_', '_').replace('`',"").replace("python", "").replace('\#', '#')
        return text
    
    @staticmethod
    def _global_cleaning_cell(query:str) -> str:
        """
        Perform generic cleaning on a cell.

        Args:
            query (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        pattern =r'[=-]{3,}'
        clean_cell = re.sub(pattern, '', query)
        pattern =r' {5,}'
        clean_cell = re.sub(pattern, '', clean_cell)
        pattern = '&#x200B;'
        clean_cell = re.sub(pattern, '', clean_cell)    

        return clean_cell

    def _get_create_code_cell(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Generate code content based on a query and add it into the Jupyter notebook.

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate code for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        list_codes = notebook_modification.get_all_cell(path)
        history = list_codes[-5:]
        code= chain_inferences.chain_code_generation(llm,query, history)
        code = self._cleaning_code_inference(code)
        clean_code = self._global_cleaning_cell(code)
        clean_code = clean_code.split("This code")[0].strip()
        notebook_modification.create_code_cell(path, clean_code)
    
    def _get_create_markdown(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Generate markdown content based on a query and add it into the Jupyter notebook.

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate markdown for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        text = chain_inferences.chain_markdown_generation(llm,query)
        clean_text = self._global_cleaning_cell(text)
        notebook_modification.create_markdown(path, clean_text)

    def _get_update_last_code_cell(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Update the content of the last code cell based on the query. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate code for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        code = notebook_modification.get_last_cell(path) 
        upd_code = chain_inferences.chain_code_update(llm,query, code)
        clean_code = self._cleaning_code_inference(upd_code)
        clean_code = self._global_cleaning_cell(clean_code)
        notebook_modification.update_last_cell(path, clean_code.strip())    

    def _get_update_last_markdown(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Update the content of the last markdown cell based on the query. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate markdown for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        text = notebook_modification.get_last_cell(path)
        upd_markdown = chain_inferences.chain_markdown_update(llm,text, query)
        clean_text = self._global_cleaning_cell(upd_markdown)
        notebook_modification.update_last_markdown(path, clean_text)
    
    def _get_update_selected_code_cell(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Update the content of the selected code cell (marked by a JupyCoder key) based on the query. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate code for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        ind, code = notebook_modification.get_cell_to_update(path)
        code = code.replace('## A MODIFIER ##', '')
        upd_code = chain_inferences.chain_code_update(llm,query, code)
        code = self._cleaning_code_inference(upd_code)
        clean_code = self._global_cleaning_cell(code)
        notebook_modification.update_cell(path, clean_code.strip(), ind)

    def _get_update_selected_markdown(self,
                              llm: Any,
                              query:str, 
                              path: str):
        """
        Update the content of the selected markdown cell (marked by a JupyCoder key) based on the query. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            query (str): The query to generate code for.
            path (str): The path to the notebook.

        Returns:
            None
        """
        ind, text = notebook_modification.get_cell_to_update(path)
        text= text.replace('## A MODIFIER ##', '')
        upd_markdown = chain_inferences.chain_markdown_update(llm,text, query)
        clean_text = self._global_cleaning_cell(upd_markdown)
        notebook_modification.update_cell(path, clean_text, ind)
    
    def _get_explain_last_cell(self,
                              llm: Any,
                              path: str):
        """
        Explain the content of the last code cell and add it into a markdown cell. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            path (str): The path to the notebook.

        Returns:
            None
        """
        code = notebook_modification.get_last_cell(path)
        explication = chain_inferences.chain_code_explanation(llm,code)
        clean_text = self._global_cleaning_cell(explication)
        notebook_modification.create_markdown(path, clean_text)

    def _get_explain_selected_cell(self,
                              llm: Any,
                              path: str):
        """
        Explain the content of a marked code cell (marked by a Jupycoder key) 
        and add it into a markdown cell just after the code cell. 

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            path (str): The path to the notebook.

        Returns:
            None
        """
        ind, code = notebook_modification.get_cell_to_explain(path)
        code = code.replace('## A EXPLIQUER ##', '')
        explication = chain_inferences.chain_code_explanation(llm,code)
        pattern =r' {2,}'
        clean_text = re.sub(pattern, '', explication)
        notebook_modification.update_cell(path, code.strip(), ind)
        notebook_modification.create_explicate_markdown(path, ind, clean_text)

    def _get_summary_all(self,
                              llm: Any,
                              path: str):
        """
        Create a summary of all the code within the notebook and add into a markdown cell at the end of the notebook.

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            path (str): The path to the notebook.

        Returns:
            None
        """
        list_codes = notebook_modification.get_all_cell(path)
        if len(list_codes) > 0 :
            combined_code = '\n'.join(cell for cell in list_codes)
        else: 
            combined_code = 'Pas de code dans ce notebook.'
        resume = chain_inferences.chain_summary(llm,combined_code)
        pattern =r' {2,}'
        clean_text = re.sub(pattern, '', resume)
        notebook_modification.create_markdown(path, clean_text)

    def tools(self,
              llm: Any,
              router_action: str, 
               query:str,
              path: str):
        """
        Perform various notebook modification actions (adding, updating, deleting, explaining) based on the router output.

        Args:
            llm (Any): The large language model object for the LangChain's LLMChain function.
            router_action (str): The action to perform, the answer of the Router LLMChain.
            query (str): The query or content for the action.
            path (str): The path to the notebook.

        Returns:
            None
        """        
        path = path.replace('\\', '/')

        if "create_code_cell" in router_action:
            self._get_create_code_cell(llm,query, path)
        elif "create_markdown" in router_action:
            self._get_create_markdown(llm,query, path)
        elif "update_last_cell" in router_action:
            self._get_update_last_code_cell(llm,query, path)
        elif "update_last_markdown" in router_action:
            self._get_update_last_markdown(llm,query, path)
        elif "update_selected_cell" in router_action:
            self._get_update_selected_code_cell(llm,query, path)
        elif "update_selected_markdown" in router_action:    
            self._get_update_selected_markdown(llm,query, path)
        elif  "delete_last_cell" in router_action:
            notebook_modification.delete_last_cell(path)
        elif "delete_selected_cell" in router_action:
            notebook_modification.delete_cell(path, notebook_modification.get_cell_to_delete(path))
        elif "explain_last_cell" in router_action:
            self._get_explain_last_cell(llm,path)
        elif "explain_selected_cell" in router_action:
            self._get_explain_selected_cell(llm,path)
        elif "summary_all" in router_action:
            self._get_summary_all(llm,path)

    def __call__(self, query:str) -> None:
        """
        Infer the intention of the user's query based on a dictionnary of possible functions. Then, 
        it realizes the action wanted by the user and dynamically update the notebook.

        Args:
            query (str): The query to process.

        Returns:
            None
        """
        action = chain_inferences.chain_router(self.llm, query)
        self.tools( self.llm, action,query, self.path)
    
    def last_version(self) -> None:
        """
        Retrieve the last version of the notebook from backup and save the last version as current version.

        Returns:
            None
        """
        notebook_name = os.path.basename(self.path)
        backup_path = os.path.join("backup", notebook_name)
        with open(backup_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        notebook_modification.save_notebook(self.path, nb)