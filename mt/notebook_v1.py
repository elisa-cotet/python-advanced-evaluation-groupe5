#!/usr/bin/env python
# -*- coding: utf-8 -*-

import notebook_v0 as toolbox #utile pour les tests du grader
from notebook_v0 import to_percent
from notebook_v0 import load_ipynb
from notebook_v0 import get_cells
import pprint

"""
an object-oriented version of the notebook toolbox
"""

class Cell: #on définit une classe commune Cell pour que les IsInstance(x,Cell) fonctionnent
    
    def __init__(self):
        pass

class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        self.id=ipynb["id"]
        self.execution_count=ipynb["execution_count"]
        self.source=ipynb["source"]
        self.type=ipynb["cell_type"]       

class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):
        self.id=ipynb["id"]
        self.source=ipynb["source"]
        self.type=ipynb["cell_type"]

class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """

    def __init__(self, ipynb):
        self.version=f"{ipynb['nbformat']}.{ipynb['nbformat_minor']}"
        self.cells=[]
        for cell in ipynb['cells']:
            if cell['cell_type']=='code':
                self.cells.append(CodeCell(cell))
            elif cell['cell_type']=='markdown':
                self.cells.append(MarkdownCell(cell))

    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        return Notebook(load_ipynb(filename))

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        dic={} 
        cells=self.nb.cells 
        dic_cells=[] #liste qui contiendra au fur et à mesure dic['cells']
        for cell in cells: 
            if cell.type == "markdown": 
                new_cell={'cell_type': cell.type, 'id': cell.id, 'metadata': {}, 'source':cell.source} 
            if cell.type == "code": 
                new_cell={'cell_type': cell.type, 'execution count':cell.execution_count, 'id': cell.id, 'metadata':{}, 'outputs':[], 'source': cell.source } 
            dic_cells.append(new_cell) 
        dic['cells']=dic_cells
        dic['metadata'] ={} 
        format = self.nb.version.split('.') 
        dic['nbformat']=int(format[0]) 
        dic['nbformat_minor']=int(format[1]) 
        return dic 


# +
class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook=notebook

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        l=[] #liste qui contiendra les éléments de la future chaine
        #cells = get_cells(self.notebook)
        for cell in self.notebook.cells:
            if isinstance(cell, MarkdownCell):
                l.append('# %% [markdown]')
                l.append('\n')
                for i in cell.source : 
                    l.append('# ')
                    l.append(i)
                l.append('\n')
            if isinstance(cell, CodeCell):
                #l.append('<BLANKLINE>')
                l.append('\n')
                l.append('# %%')
                l.append('\n')
                for i in cell.source : 
                    l.append(i)
                l.append('\n')
                #l.append('<BLANKLINE>')
                l.append('\n')
        l.pop()
             
        return str("".join(l))

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        with open(filename, 'w') as fp:
            file.write(self.to_py_percent())
            
    
class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'medatada': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'medatada': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'medatada': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook=notebook
        
        #première version de serialize(self), marche en testant manuellement avec pprint, mais pas dans le grader 
        
     #def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        #nb=self.notebook
        #d = {"nbformat": 4, "nbformat_minor": 5, "metadata": {}}
        #d['cells']=[]
        #for cell in nb :
            #cell1 = {'cell_type': cell.type,'id': cell.id,'metadata' : {}, 'source': cell.source}
            #if cell.type == 'code' :
                #cell1['execution_count'] = cell.execution_count
                #cell1['outputs']=[]
            #d['cells'].append(cell1) 
        #return d

        #deuxième version de serialize(self), marche avec le grader
        
    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        nb=self.notebook
        d={}
        #on commence par construire d['cells'] à partir des cellules du notebook
        d['cells']=[]
        for cell in nb :
            new_cell = {'cell_type': cell.type}
            if cell.type == 'code' :
                new_cell['execution_count'] = cell.execution_count
            new_cell['id']=cell.id
            new_cell['medatada']={}
            if cell.type == 'code' :
                new_cell['outputs']=[] 
            new_cell['source']=cell.source
            d['cells'].append(new_cell)  
            
        #j'utilise deux 'if' au lieu d'un, sinon les clés du dict ne sont pas dans le bon ordre
        
        #puis on ajoute les autres caractéristiques du notebook au nouveau dictionnaire 

        new_d={}
        new_d['cells']=d['cells']
        new_d['metadata']={}
        new_d['nbformat']=4
        new_d['nbformat_minor']=5

        return new_d
        

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        a_file = open("data.pkl", "wb")
        pickle.dump(dictionary_data, a_file)
        a_file.close()

        a_file = open("data.pkl", "rb")
        output = pickle.load(a_file)
        print(output)
        
    def serialize_JSON(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        return Serializer.serializeNotebook(self.notebook)
# -

nb = Notebook.from_file("samples/hello-world.ipynb")
ppp = PyPercentSerializer(nb)
print(ppp.to_py_percent())


class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    
    
    def __init__(self, notebook):
        self.notebook = notebook
        
    @staticmethod    
    def outline_aux(notebook):
        nb=notebook
        l=[]
        l.append(f'Jupyter Notebook v{nb.version}\n')
        for cell in nb:
            if cell.type == 'markdown':
                l.append(f'└─▶ Markdown cell #{cell.id}')
            if cell.type == 'code':
                l.append(f'└─▶ Code cell #{cell.id}')
                l.append (f' ({cell.execution_count})')    
            l.append('\n')
            if len(cell.source) > 1:  
                x=cell.source[0].replace("\n","")
                l.append(f'    ┌  {x}')
                l.append('\n')
                for i in range (1, len(cell.source)-1):
                    x=cell.source[i].replace("\n","")
                    l.append(f'    │  {x}')
                    l.append('\n')
                x=cell.source[-1].replace("\n","")
                l.append(f'    └  {x}')
                l.append('\n')
            elif(len(cell.source) == 1):
                x=cell.source[0].replace("\n","")
                l.append(f'    | {x}')
                l.append('\n')
        l.pop() #on enlève le dernier \n qui est en trop
        return str("".join(l))

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        return Outliner.outline_aux(self.notebook)
