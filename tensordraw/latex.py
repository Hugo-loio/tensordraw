import subprocess
import os
import tempfile

from ._drawable import Drawable

LATEX_PREAMBLE = r"\usepackage{amsmath,amssymb,dsfont}"

class Latex(Drawable):
    def __init__(self, latex_str, **kwargs):
        self.latex_str = latex_str
        self.preamble = kwargs.get('preamble', "")
        self.output = ""

        self._tmpdir = tempfile.TemporaryDirectory(prefix="tensordraw")
        self.compile()

        super().__init__(**kwargs)

    def compile(self):
        with tempfile.NamedTemporaryFile(dir=self._tmpdir.name, suffix=".tex", 
                                         delete=False) as temp:
            
            print(f"Temp file {temp.name}")

            #full_tex = fr"""
            #\documentclass{{standalone}}
            #{LATEX_PREAMBLE}
            #{self.preamble}
            #\begin{{document}}
            #{self.latex_str}
            #\end{{document}}
            #"""
            #
            #with open(tex_path, "w") as f:
            #    f.write(full_tex)
            #    
            ## Run pdflatex
            #subprocess.run(
            #    ["pdflatex", "-interaction=nonstopmode", "formula.tex"],
            #    cwd=tmpdir, stdout=subprocess.DEVNULL
            #)

    def draw(self, context):
        if(self.output == ""):
            #raise RuntimeError("No latex compiled output found")
            print("oi")

    def limits(self, R):
        return (0,0,0,0)
        
    def __del__(self):
        # The TemporaryDirectory object automatically cleans up when
        # its reference count hits zero, but we can be explicit:
        self._tmpdir.cleanup()
