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
    """
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
    #import json
    #f = open(filename,)
    #return json.loads(filename)

    json_file_path = filename

    with open(json_file_path, 'r') as j:
        contents = json.loads(j.read())
    return contents


load_ipynb("samples/minimal.ipynb")


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
    
    with open(filename, 'w') as fp:
        json.dump(ipynb, fp)


ipynb = load_ipynb("samples/hello-world.ipynb")
save_ipynb(ipynb, "samples/hello-world-save-load.ipynb")
ipynb == load_ipynb("samples/hello-world-save-load.ipynb")


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


ipynb = load_ipynb("samples/hello-world.ipynb")
get_format_version(ipynb)


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


ipynb = load_ipynb("samples/metadata.ipynb")
metadata = get_metadata(ipynb)
pprint.pprint(metadata)


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
    cells =ipynb['cells']
    return cells


ipynb = load_ipynb("samples/minimal.ipynb")
cells = get_cells(ipynb)
cells

ipynb = load_ipynb("samples/hello-world.ipynb")
print(ipynb)
cells = get_cells(ipynb)
pprint.pprint(cells)


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
    
    l=[]
    cells = get_cells(ipynb)
    for k in range (len(cells)) :
        cell=cells[k]
        if cell['cell_type']=='markdown':
            l.append('# %% [markdown]')
            l.append('\n')
            for i in cell['source'] : 
                l.append('# ')
                l.append(i)
            l.append('\n')
        if cell['cell_type']=='code':
            l.append('# %%')
            l.append('\n')
            for i in cell['source'] : 
                l.append(i)
            l.append('\n')
             
    return str("".join(l))


ipynb = load_ipynb("samples/hello-world.ipynb")
print(to_percent(ipynb))



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
    def to_staraux(ipynb):
        l=[]
        cells = get_cells(ipynb)
        for k in range (len(cells)) :
            cell=cells[k]
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
        return str("".join(l))
        
    if html==True:
        return starboard_html(to_staraux(ipynb))
    else:
        return to_staraux(ipynb)


# +
ipynb = load_ipynb("samples/hello-world.ipynb")
print(to_starboard(ipynb))

html = to_starboard(ipynb, html=True)
print(html)


# -

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
    cells = get_cells(ipynb)
    for k in range (len(cells)) :
        cell=cells[k]
        if cell['cell_type']=='code':
            cell['execution_count']=None
            cell['outputs']=[]



# +
ipynb =        {'cells': [{'cell_type': 'markdown',
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

clear_outputs(ipynb)
pprint.pprint(ipynb)


# -

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
    
                        #'outputs': [{'name': 'stdout',
                                 #'output_type': 'stream',
                                 #'text': ['Hello world!\n']}],
    l=[]
    
    
    cells = get_cells(ipynb)
    for k in range (len(cells)) :
        cell=cells[k]
        if cell['cell_type']=='code':
            d=cell['outputs']
            if stdout==True:
                if d[0]['name']=='stdout':
                    #x=d[0]['text'][0]
                    #y=x.replace('\n','')
                    l.append(d[0]['text'][0])
                    #print(d[0]['text'][0])
            if stderr==True:
                if d[0]['name']=='stderr':
                    #a=d[0]['text'][0]
                    #w=a.replace('\n','')
                    l.append(d[0]['text'][0])
                    #print(d[0]['text'][0])
    if len(l)==2:
        return "".join(l)
    else:
        return l[0]         

ipynb = load_ipynb("samples/streams.ipynb")
#print(ipynb)
print(get_stream(ipynb))
print(get_stream(ipynb, stdout=False, stderr=True))
print(get_stream(ipynb, stdout=True, stderr=True))


def get_exceptions(ipynb):
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
    cells = get_cells(ipynb)
    for k in range (len(cells)) :
        cell=cells[k]
        if cell['cell_type']=='code':
            d=cell['outputs']
            if d[0]['output_type']=='error':
                errors.append((d[0]["ename"],d[0]["evalue"]))
                #errors.append(f'{d[0]["ename"]}("{d[0]["evalue"]}")')
    return errors


dans ename de output
classe expection

# +
ipynb = load_ipynb("samples/errors.ipynb")
errors = get_exceptions(ipynb)
print(all(isinstance(error, Exception) for error in errors))
for error in errors:
    print(repr(error))

#isinstance(TypeError("unsupported operand type(s) for +: 'int' and 'str'"), Exception)
#isinstance(Warning("🌧️  light rain"), Exception)
# -

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
    errors = []
    cells = get_cells(ipynb)
    for k in range (len(cells)) :
        cell=cells[k]
        if cell['cell_type']=='code':
            d=cell['outputs']
            if len(d)>0:
                if 'image/png' not in d[0]['data'].keys():
                    return d[0]['data']['text/plain']


ipynb = load_ipynb("samples/images.ipynb")
ipynb

# +
ipynb = load_ipynb("samples/images.ipynb")
#print(get_images(ipynb))

l=[]

import ast

for k in range (len(get_images(ipynb))):
    x=get_images(ipynb)[k]
    y=x.replace(',\n','')
    z=y.replace(' ','')
    a=z.replace('[ ','[')
    b=a.replace(",'\n'","")
    #c=ast.literal_eval(b)
    #print(a)
    l.append(b)

l

#get_images(ipynb)
# -

 #import matplotlib.pyplot as plt
#plt.imshow(get_images(ipynb))
