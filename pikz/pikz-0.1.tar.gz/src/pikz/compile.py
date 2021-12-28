import os
import subprocess
import shutil

AUX_EXTENSIONS = [
    "aux", "log"
]


class LatexCompileError(RuntimeError):
    pass


def compile_latex(filepath: str,
                  outputdir: str = None,
                  clean_files: bool = True) -> str:

    if not os.path.exists(filepath):
        raise FileNotFoundError

    if shutil.which("pdflatex") is None:
        raise RuntimeError(f"pdf latex needs to be installed")

    if outputdir is None:
        outputdir = os.path.dirname(filepath)

    command = f"pdflatex -output-directory={outputdir} -interaction=nonstopmode {filepath}".split()

    compile_process = subprocess.run(command,
                                     stderr=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True)

    if compile_process.returncode != 0:
        out = compile_process.stdout
        error_msg = out[out.find("!"):]
        raise LatexCompileError(error_msg)

    basename = os.path.basename(filepath)
    base, _ = os.path.splitext(basename)

    if clean_files:
        for ext in AUX_EXTENSIONS:
            target = f"{base}.{ext}"
            os.remove(os.path.join(outputdir, target))

    return os.path.join(outputdir, f"{base}.pdf")