"""Module to run the entire template notebook"""

import os
import shutil
import unittest
import subprocess

import nbformat

from tess_atlas import run_toi


SINGLE_TRANSIENT = 103 
MULTI_TRANSIENT = 178 # has 3 planets


class NotebookRunnerTestCase(unittest.TestCase):
    def setUp(self):
        self.start_dir = os.getcwd()
        self.version = "TEST"
        self.outdir = f"../notebooks/{self.version}"
        os.makedirs(self.outdir, exist_ok=True)

    def tearDown(self):
        os.chdir(self.start_dir)
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)

    def test_notebook_creation(self):
        notebook_fn = run_toi.create_toi_notebook_from_template_notebook(
            toi_number=723, version=self.version, quickrun=True
        )
        self.assertTrue(os.path.exists(notebook_fn))

        try:
            with open(notebook_fn) as f:
                notebook = nbformat.read(f, as_version=4)
                nbformat.validate(notebook)
        except nbformat.ValidationError:
            self.fail(f"{notebook_fn} is an invalid notebook")

    def test_notebook_execution(self):
        notebook_fn = run_toi.create_toi_notebook_from_template_notebook(
            toi_number=MULTI_TRANSIENT, version=self.version, quickrun=True
        )
        success = run_toi.execute_toi_notebook(
            notebook_fn, version=self.version
        )
        self.assertTrue(success)
        subprocess.check_call(f"git rm {notebook_fn} -f", shell=True)
        self.assertTrue(os.path.exists(notebook_fn.replace(".ipynb", ".netcdf")))



if __name__ == "__main__":
    unittest.main()
