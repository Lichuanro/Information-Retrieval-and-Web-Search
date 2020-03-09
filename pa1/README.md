Getting started
===============

Install Conda
-------------
We will use Conda to obtain a standard installation of Python and related useful packages. If you aren't already using it, please install it using the platform-specific instructions provided on the [Conda installation page](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Create a New Environment
------------------------
We have provided an environment file for this assignment.
To create a new environment with the correct packages, run

     conda env create -f environment.yml


This will create a new environment named cs276-pa1. You can activate it by running

     conda activate cs276-pa1

Once you are done working on the assignment, you can deactivate it by running

     conda deactivate

If you’ve got conda v4.4+, you should use `conda activate cs276-pa1` and similarly `conda deactivate`


Open Jupyter Notebook
---------------------
We'll be using a Jupyter notebook to do our assignment. You can start a new session with

      jupyter notebook

This will start a local server which you can then connect with using a local browser.
