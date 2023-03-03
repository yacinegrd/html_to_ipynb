from glob import glob
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import json 
import os

def init_nb():
    return {
    "metadata": {
    "kernelspec": {
        "display_name": "base",
        "language": "python",
        "name": "python3" 
    },
    "language_info": {
        "name": "python",
        "version": "3.9.16"
    },
    },
    "nbformat": 4,
    "nbformat_minor": 2,
    "cells" : [],
    }

def isMarkdown(cell):
    return 'jp-MarkdownCell' in cell['class']

def isCode(cell):
    return 'jp-CodeCell' in cell['class']

def add_code_cell(cell, notebook):
    code = cell.find(class_='CodeMirror')
    
    source = code.get_text().strip()
    
    in_count = cell.find(class_='jp-InputPrompt')
    in_count = ''.join(filter(str.isdigit, in_count.get_text()))
    in_count = int(in_count) if in_count != '' else 0
    
    notebook["cells"].append(
    {
        "cell_type" : "code",
        "execution_count": in_count, # integer or null
        "metadata" : {},
        "source" : source,
        "outputs": []
    })
    
    return notebook

def add_markdown_cell(cell, notebook):
    content = str (cell.find(class_='jp-MarkdownOutput'))
    #content = ''.join(line.strip('/n') for line in content)    
    content = "".join(line.strip() for line in content.split("\n"))
    source = md(content, heading_style="ATX")
    notebook["cells"].append(
    {
        "cell_type" : "markdown",
        "metadata" : {},
        "source" : source,
    })
    
    return notebook

def html_to_ipynb(file, notebook):
    with open(file) as f:
        soup = BeautifulSoup(f, 'html.parser')

    cells = soup.find_all(class_='jp-Cell')

    for cell in cells:
        if isMarkdown(cell):
            notebook = add_markdown_cell(cell, notebook)
        if isCode(cell):
            notebook = add_code_cell(cell, notebook)
    
    return notebook

def save_ipynb(file_name, notebook, out_dir='out'):
    file_name = file_name.split('/')
    file_name = './'  + out_dir + '/' + file_name[-1]

    if not out_dir in os.listdir('./'):
        os.mkdir('./' + out_dir)
    with open(file_name.replace('.html', '.ipynb'), "w") as outfile:
        json.dump(notebook, outfile)

file_names = glob('./html/*html')
# print(file_names[1].replace('.html', '.json'))
for file in file_names:
    # initialise a new notebook json
    notebook = init_nb()

    notebook = html_to_ipynb(file, notebook)

    save_ipynb(file, notebook)
    
    

