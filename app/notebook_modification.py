from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import nbformat
import os
import shutil
from typing import Any

def create_notebook(nb_path:str)-> None:
    """
    Create a new Jupyter notebook and save it to the specified path.

    Args:
        nb_path (str): The path where the new Jupyter notebook will be saved.

    Returns:
        None
    """    
    notebook = new_notebook()
    with open(nb_path, 'w') as f:
        nbformat.write(notebook, f)

def load_notebook(nb_path: str)-> Any:
    """
    Load a Jupyter notebook from a file and create a backup copy of the original file.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        Any: The loaded Jupyter notebook object.
    """

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    if not os.path.exists('backup'):
        os.makedirs('backup')
    notebook_name = os.path.basename(nb_path)
    backup_path = os.path.join("backup", notebook_name)
    shutil.copyfile(nb_path, backup_path)

    return nb

def save_notebook(nb_path: str, 
                    nb: Any) -> None:    
    """
    Save the Jupyter notebook.

    Args:
        nb_path (str): The path where the Jupyter notebook will be saved.
        nb (Any): The Jupyter notebook object to be saved.

    Returns:
        None
    """
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    
def create_code_cell(nb_path: str, 
                        content: str) -> None:
    """
    Create a new code cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The content of the code cell.

    Returns:
        None
    """
    nb = load_notebook(nb_path)   
    new_cell = new_code_cell(content)
    nb.cells.append(new_cell)
    save_notebook(nb_path, nb)
    
def create_markdown(nb_path: str, 
                        content: str) -> None:
    """
    Create a new markdown cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The content of the markdown cell.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    new_cell = new_markdown_cell(content)
    nb.cells.append(new_cell)
    save_notebook(nb_path, nb)

def create_explicate_markdown(nb_path: str,
                    ind: int, 
                    content: str) -> None:
    """
    Create a new markdown cell at a specified index in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        ind (int): The index where the markdown cell will be inserted.
        content (str): The content of the markdown cell.

    Returns:
        None
    """
    ind = ind[0]
    nb = load_notebook(nb_path)
    new_cell = new_markdown_cell(content)
    nb.cells.insert(ind+1,new_cell)
    save_notebook(nb_path, nb)

def update_last_cell(nb_path: str, 
                        content: str) -> None:
    """
    Update the content of the last cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The new content for the last cell.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    cell_id = len(nb.cells)-1
    cell = nb.cells[cell_id]
    cell.source = content
    save_notebook(nb_path, nb)

def update_cell(nb_path: str, 
                content: str, 
                cell_id: int)  -> None:
    """
    Update the content of a specific code cell (at a specific id) in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The new content for the cell.
        cell_id (int): The index of the cell to update.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    if cell_id[0] < len(nb.cells):
        cell = nb.cells[cell_id[0]]
        cell.source = content
        save_notebook(nb_path, nb)
    else:
        print("L'index de cellule spécifié est invalide.")

def update_markdown(nb_path: str, 
                content: str, 
                cell_id: int)  -> None:
    """
    Update the content of a specific markdown cell (at a specific id) in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The new content for the cell.
        cell_id (int): The index of the cell to update.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    if cell_id > 0 and cell_id <= len(nb.cells):
        cell = nb.cells[cell_id-1]
        if cell.cell_type == "markdown":
            cell.source = content
        else:
            print(f"Modification impossible car la cellule {cell_id} est une cellule de code.")
        save_notebook(nb_path, nb)
    else:
        print("L'index de cellule spécifié est invalide.")

def update_last_markdown(nb_path: str, 
                        content: str) -> None:
    """
    Update the content of the last markdown cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        content (str): The new content for the last markdown cell.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    cell_id = len(nb.cells)-1
    cell = nb.cells[cell_id]
    if cell.cell_type == "markdown":
        cell.source = content
    else:
        print(f"Modification impossible car la cellule {cell_id} est une cellule de code.")
    save_notebook(nb_path, nb)

def delete_last_cell(nb_path: str) -> None:
    """
    Delete the last cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        None
    """
    nb = load_notebook(nb_path)
    cell_id = len(nb.cells)-1
    del nb.cells[cell_id]
    save_notebook(nb_path, nb)

def delete_cell(nb_path: str, cell_id: int)-> None:
    """
    Delete a specific cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.
        cell_id (int): The index of the cell to delete.

    Returns:
        None
    """
    nb = load_notebook(nb_path)    
    if cell_id[0] > 0 and cell_id[0] <= len(nb.cells):
        del nb.cells[cell_id[0]]
        save_notebook(nb_path, nb)
    else:
        print("L'index de cellule spécifié est invalide.")

def get_last_cell(nb_path: str)-> str:
    """
    Retrieve the content of the last cell in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        str: The content of the last cell.
    """
    nb = load_notebook(nb_path)
    last_cell = nb.cells[len(nb.cells)-1]
    return last_cell.source

def get_cell_to_update(nb_path: str)-> tuple[int, str]:
    """
    Retrieve the index and content of a cell marked for update with a JupyCoder key in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        tuple: A tuple containing the index and content of the cell marked for update.
    """
    nb = load_notebook(nb_path)
    all_codes = [cell["source"] for cell in nb.cells]
    ind_update = [ind for ind, cell in enumerate(all_codes)  if '## A MODIFIER ##' in cell]
    code = all_codes[ind_update[0]]

    return ind_update,code 

def get_cell_to_delete(nb_path: str)-> int:
    """
    Retrieve the indices of cells marked by a JupyCoder key for deletion in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        int: An integer containing the index of the cell marked for deletion.
    """
    nb = load_notebook(nb_path)
    all_codes = [cell["source"] for cell in nb.cells]
    ind_delete = [ind for ind, cell in enumerate(all_codes)  if '## A SUPPRIMER ##' in cell]

    return ind_delete

def get_cell_to_explain(nb_path: str)-> tuple[int, str]:
    """
    Retrieve the index and content of a cell marked for explanation  by a JupycoderKey in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        tuple: A tuple containing the index and content of the cell marked for explanation.
    """
    nb = load_notebook(nb_path)
    all_codes = [cell["source"] for cell in nb.cells]
    ind_update = [ind for ind, cell in enumerate(all_codes)  if '## A EXPLIQUER ##' in cell]
    code = all_codes[ind_update[0]]
    return ind_update, code 
    
def get_all_cell(nb_path: str)-> list[str]:
    """
    Retrieve the content of all code cells in a Jupyter notebook.

    Args:
        nb_path (str): The path to the Jupyter notebook file.

    Returns:
        list: A list containing the content of all code cells.
    """
    nb = load_notebook(nb_path)
    all_codes = [cell["source"] for cell in nb.cells if cell.get('cell_type') == 'code']
    return all_codes