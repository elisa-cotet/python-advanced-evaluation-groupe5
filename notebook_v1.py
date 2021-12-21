#!/usr/bin/env python
# -*- coding: utf-8 -*-
from notebook_v0 import *
"""
an object-oriented version of the notebook toolbox
"""

# +
class Cell:
    
    def __init___:
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

# +
code_cell = CodeCell({
        "cell_type": "code",
        "execution_count": 1,
        "id": "b777420a",
        'source': ['print("Hello world!")']
        })

code_cell.id
code_cell.execution_count
code_cell.source


# -

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

# +
markdown_cell = MarkdownCell({
        "cell_type": "markdown",
        "id": "a9541506",
        "source": [
        "Hello world!\n",
        "============\n",
        "Print `Hello world!`:"
        ]
        })

markdown_cell.id
markdown_cell.source


# +
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
        self.cells_list=[]
        for cell in ipynb['cells']:
            if cell['cell_type']=='code':
                self.cells_list.append(CodeCell(cell))
            elif cell['cell_type']=='markdown':
                self.cells_list.append(MarkdownCell(cell))

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
        return iter(self.cells_list)
    



# -

ipynb = load_ipynb("samples/hello-world.ipynb")
nb = Notebook(ipynb)
isinstance(nb.cells_list, list)
isinstance(nb.cells_list[0], Cell)

nb = Notebook.from_file("samples/hello-world.ipynb")
for cell in nb :
    print(cell.id)


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
                l.append('<BLANKLINE>')
                l.append('\n')
                l.append('# %%')
                l.append('\n')
                for i in cell['source'] : 
                    l.append(i)
                l.append('\n')
                l.append('<BLANKLINE>')
                l.append('\n')
             
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
            json.dump(ipynb, fp)
    
    
    
    
    
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

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        import json
        return json.dumps(self)

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

# +
nb = Notebook.from_file("samples/hello-world.ipynb")
s=Serializer(nb)

pprint.pprint(s.serialize())

# +
nb = Notebook.from_file("samples/hello-world.ipynb")
s = PyPercentSerializer(nb)
s.to_file("samples/hello-world-serialized-py-percent.py")

s
# -

nb = Notebook.from_file("samples/hello-world.ipynb")
ppp = PyPercentSerializer(nb)
print(ppp.to_py_percent())

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

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        
