# JupyCoder: Your LowCost GenAI MultiModal Jupyter Coding Assistant

This repository contains the algorithm for an LLM application designed to be a multi-model Jupyter coding assistant. Through voice or text input, the user can interact with his notebook and generate lines of code and markdown. They can also delete, update or even add an explanation for a specific cell. Finally, you can quickly add a summary of the notebook. Its simplicity makes it ideal for local implementation of LLM applications. This current version works with Mixtral-8x7B (thanks to its easy access through the HuggingFace inference API) and LangChain. This algorithm is a perfect example of implementing code inference through an LLM application.

The Medium article is available here: 

/!\ Project by Clovis Varangot-Reille, Dounya Bourhani, Nousra Chaibati & Joseph Pelham

*The creators of this tool provide no warranty or assurance regarding its performance, dependability, or suitability for any specific purpose.*

# First, import the repository and start the Streamlit App - 

```
git clone https://github.com/cvarrei/JupyCoder.git

cd app
py -m venv venv

(Linux/MacOS)
source venv/bin/activate
(Windows)
cd venv
Scripts\activate
cd ..

pip install -r requirements.txt
streamlit run homepage.py
```
# Then, navigate within the Streamlit App

Upon accessing the application's home page, users are presented with a gateway to its functionality. The home page serves as the primary interface for navigating through the application's features and functionalities.

<p align="center">
  <img src="/images/homepage.PNG" width="500" title="homepage">
</p>

You must follow the following steps in the right order: 

## 1. Notebook Connection Page:

This page is designated for establishing a connection between your notebook device and the application's backend infrastructure. Through this interface, users will be able to write the exact path of their notebook. For example: */home/user/projects/my_project/notebooks/data_analysis.ipynb*

<p align="center">
  <img src="/images/page1.PNG" width="500" title="page 1">
</p>

## Action Page:

The second page is dedicated to the execution of the application's ecosystem. Users first authenticate by integrating their HuggingFace Inference API token. Once authentication has been successfully completed, the action page is displayed. 

<p align="center">
  <img src="/images/page2.PNG" width="500" title="page 2">
</p>

A dual-interface approach empowers users to articulate queries via voice or text input, fostering flexibility in interaction. On the left, the user will be able to record his voice while giving his query.  On the right, it will be able to write its query. There is a small button to delete the current text input. 

In the Jupycoder algorithm, we access the Jupyter notebook, edit the JSON file underneath it, and then rewrite the file in order to update it dynamically. Thus, we included a button to access the last version of the notebook (just before the last action took place). This file will be saved in a backup folder underneath. 

<p align="center">
  <img src="/images/precedent.PNG" width="500" title="page 2">
</p>

With a click, users can export the query historical data into a downloadable TXT file.
