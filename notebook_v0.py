#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
starter code for your evaluation assignment
"""

# Python Standard Library
import base64
import io
import json
import pprint

# Third-Party Libraries
import numpy as np
import PIL.Image  # pillow


def load_ipynb(filename):
    r"""
    Load a jupyter notebook .ipynb file (JSON) as a Python dict.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    with open(filename,'rb') as file:
        loaded_file=json.loads(file.read())
    return loaded_file


def save_ipynb(ipynb, filename):
    r"""
    Save a jupyter notebook (Python dict) as a .ipynb file (JSON)

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}
        >>> ipynb["metadata"]["clone"] = True
        >>> save_ipynb(ipynb, "samples/minimal-save-load.ipynb")
        >>> load_ipynb("samples/minimal-save-load.ipynb")
        {'cells': [], 'metadata': {'clone': True}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> save_ipynb(ipynb, "samples/hello-world-save-load.ipynb")
        >>> ipynb == load_ipynb("samples/hello-world-save-load.ipynb")
        True

    """
    with open(filename,"w") as file:
        json.dump(ipynb,file)


def get_format_version(ipynb):
    r"""
    Return the format version (str) of a jupyter notebook (dict).

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> get_format_version(ipynb)
        '4.5'

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_format_version(ipynb)
        '4.5'
    """
    format =ipynb['nbformat']
    format_minor = ipynb['nbformat_minor']
    return f"{format}.{format_minor}"


def get_metadata(ipynb):
    r"""
    Return the global metadata of a notebook.

    Usage:

        >>> ipynb = load_ipynb("samples/metadata.ipynb")
        >>> metadata = get_metadata(ipynb)
        >>> pprint.pprint(metadata)
        {'celltoolbar': 'Edit Metadata',
         'kernelspec': {'display_name': 'Python 3 (ipykernel)',
                        'language': 'python',
                        'name': 'python3'},
         'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
                           'file_extension': '.py',
                           'mimetype': 'text/x-python',
                           'name': 'python',
                           'nbconvert_exporter': 'python',
                           'pygments_lexer': 'ipython3',
                           'version': '3.9.7'}}
    """
    metadata =ipynb['metadata']
    return metadata


def get_cells(ipynb):
    r"""
    Return the notebook cells.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> cells = get_cells(ipynb)
        >>> cells
        []

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> cells = get_cells(ipynb)
        >>> pprint.pprint(cells)
        [{'cell_type': 'markdown',
          'id': 'a9541506',
          'metadata': {},
          'source': ['Hello world!\n', '============\n', 'Print `Hello world!`:']},
         {'cell_type': 'code',
          'execution_count': 1,
          'id': 'b777420a',
          'metadata': {},
          'outputs': [{'name': 'stdout',
                       'output_type': 'stream',
                       'text': ['Hello world!\n']}],
          'source': ['print("Hello world!")']},
         {'cell_type': 'markdown',
          'id': 'a23ab5ac',
          'metadata': {},
          'source': ['Goodbye! 👋']}]
    """
    cells=ipynb['cells']
    return cells


def to_percent(ipynb):
    r"""
    Convert a ipynb notebook (dict) to a Python code in the percent format (str).

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_percent(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        # %% [markdown]
        # Hello world!
        # ============
        # Print `Hello world!`:
        # %%
        print("Hello world!")
        # %% [markdown]
        # Goodbye! 👋

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     percent_code = to_percent(ipynb)
        ...     with open(notebook_file.with_suffix(".py"), "w", encoding="utf-8") as output:
        ...         print(percent_code, file=output)
    """
    l=[] #contiendra des strings qu'on fusionnera pour retourner le string final
    cells = get_cells(ipynb)
    for cell in cells : #pour chaque cellule, on récupère les informations nécessaires
        if cell['cell_type']=='markdown':
            l.append('# %% [markdown]')
            l.append('\n')
            for i in cell['source'] : 
                l.append('# ')
                l.append(i)
            l.append('\n')
        if cell['cell_type']=='code':
            l.append('\n')
            l.append('# %%')
            l.append('\n')
            for i in cell['source'] : 
                l.append(i)
            l.append('\n')
            l.append('\n')
    return str("".join(l))


def starboard_html(code):
    return f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Starboard Notebook</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="icon" href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/favicon.ico">
        <link href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.css" rel="stylesheet">
    </head>
    <body>
        <script>
            window.initialNotebookContent = {code!r}
            window.starboardArtifactsUrl = `https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/`;
        </script>
        <script src="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.js"></script>
    </body>
</html>
"""


def to_starboard(ipynb, html=False):
    r"""
    Convert a ipynb notebook (dict) to a Starboard notebook (str)
    or to a Starboard HTML document (str) if html is True.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_starboard(ipynb))
        # %% [markdown]
        Hello world!
        ============
        Print `Hello world!`:
        # %% [python]
        print("Hello world!")
        # %% [markdown]
        Goodbye! 👋

        >>> html = to_starboard(ipynb, html=True)
        >>> print(html) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        <!doctype html>
        <html>
        ...
        </html>

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     starboard_html = to_starboard(ipynb, html=True)
        ...     with open(notebook_file.with_suffix(".html"), "w", encoding="utf-8") as output:
        ...         print(starboard_html, file=output)
    """
    #même procédé que pour to_percent, avec quelques adaptations du contenu de la chaine
    def to_staraux(ipynb):
        l=[]
        cells = get_cells(ipynb)
        for cell in cells :
            if cell['cell_type']=='markdown':
                l.append('# %% [markdown]')
                l.append('\n')
                for i in cell['source'] : 
                    l.append(i)
                l.append('\n')
            if cell['cell_type']=='code':
                l.append('# %% [python]')
                l.append('\n')
                for i in cell['source'] : 
                    l.append(i)
                l.append('\n')
        l.pop() #on enlève le dernier saut de ligne ('\n') qui est en trop
        return str("".join(l))
        
    if html==True:
        return starboard_html(to_staraux(ipynb)) #passage en html
    else:
        return to_staraux(ipynb)


# Outputs
# ------------------------------------------------------------------------------
def clear_outputs(ipynb):
    r"""
    Remove the notebook cell outputs and resets the cells execution counts.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
        >>> clear_outputs(ipynb)
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': None,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    #pour chaque cellule de type code, on réinitialise execution_count et outputs
    cells = get_cells(ipynb)
    for cell in cells :
        if cell['cell_type']=='code': 
            cell['execution_count']=None
            cell['outputs']=[]


# +
def get_stream(ipynb, stdout=True, stderr=False):
    r"""
    Return the text written to the standard output and/or error stream.

    Usage:

        >>> ipynb = load_ipynb("samples/streams.ipynb")
        >>> print(get_stream(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        >>> print(get_stream(ipynb, stdout=False, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
        >>> print(get_stream(ipynb, stdout=True, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
        """
    l=[]
    cells = get_cells(ipynb)
    for cell in cells :
        if cell['cell_type']=='code':
            d=cell['outputs']
            if stdout==True:
                if d[0]['name']=='stdout': #on récupère 👋 Hello world! 🌍
                    l.append(d[0]['text'][0])
            if stderr==True:
                if d[0]['name']=='stderr': #on récupère 🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
                    l.append(d[0]['text'][0])
    if len(l)==2: #si on a les deux, on les joint
        return "".join(l)
    else:
        return l[0]         
    
def get_exceptions(ipnyb):
    
    r"""
    Return all exceptions raised during cell executions.
    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_exceptions(ipynb)
        []

        >>> ipynb = load_ipynb("samples/errors.ipynb")
        >>> errors = get_exceptions(ipynb)
        >>> all(isinstance(error, Exception) for error in errors)
        True
        >>> for error in errors:
        ...     print(repr(error))
        TypeError("unsupported operand type(s) for +: 'int' and 'str'")
        Warning('🌧️  light rain')
    """      
    errors = []
    for cell in get_cells(ipynb):
        try: 
            errors.append(eval(f"{cell['outputs'][0]['ename']}(\"{cell['outputs'][0]['evalue']}\")"))
        except:
            pass
    return errors

    #le grader ne marche pas avec 
    #ipynb = load_ipynb("samples/errors.ipynb")
    #errors = get_exceptions(ipynb)
    #parce qu'il dit que len(errors) != 2 alors qu'en testant manuellement ça marche...

def get_images(ipynb):
    r"""
    Return the PNG images contained in a notebook cells outputs
    (as a list of NumPy arrays).

    Usage:

        >>> ipynb = load_ipynb("samples/images.ipynb")
        >>> images = get_images(ipynb)
        >>> images # doctest: +ELLIPSIS
        [array([[[ ...]]], dtype=uint8)]
        >>> grace_hopper_image = images[0]
        >>> np.shape(grace_hopper_image)
        (600, 512, 3)
        >>> grace_hopper_image # doctest: +ELLIPSIS
        array([[[ 21,  24,  77],
                [ 27,  30,  85],
                [ 33,  35,  92],
                ...,
                [ 14,  13,  19]]], dtype=uint8)
    """
    #ne marche pas
    #ce que j'ai essayé de faire : 
    #récupérer le tableau avec toutes les valeurs des pixels, le nettoyer et utiliser plt.imshow()
    #mais je n'arrive pas à bien le nettoyer, il reste des \n que je n'arrive pas à enlever :c

    l=[]

    import ast

    for k in range (len(get_images(ipynb))):
        x=get_images(ipynb)[k]
        y=x.replace(',\n','')
        z=y.replace(' ','')
        a=z.replace('[ ','[')
        b=a.replace(",'\n'","")
        #c=ast.literal_eval(b) le literal_eval ne marche pas
        #print(a)
        l.append(b)
        
    print(l) #on vérifie à quoi l ressemble

    import matplotlib.pyplot as plt #ne marche pas car il reste des NaN dans l
    plt.imshow(get_images(l))


# -

ipynb = load_ipynb("samples/hello-world.ipynb")
get_exceptions(ipynb)

# +
ipynb = load_ipynb("samples/errors.ipynb")
errors = get_exceptions(ipynb)

print(len(errors))

all(isinstance(error, Exception) for error in errors)
# -

ipynb = load_ipynb("samples/images.ipynb")
ipynb


