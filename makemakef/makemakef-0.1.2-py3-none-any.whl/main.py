import argparse
import os
import re
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Set, Tuple


class FortranFile(object):
    """Fortran file class.
    """

    def __init__(self, filepath: Path, osuffix: str = '.o'):
        self.filepath: Path = filepath
        self.objname: str = self.filepath.stem + osuffix
        self.def_modules, self.use_modules = \
            FortranFile.search_module(filepath)

    @classmethod
    def search_module(cls, filepath: Path) -> Tuple[Set[str], Set[str]]:
        """Search modules defined in the file and modules on which the file depends.

        Parameters
        ----------
        filepath : Path
            filepath to be searched

        Returns
        -------
        Tuple[Set[str], Set[str]]
            names of the modules defined in the file, names of the modules on which the file depends
        """
        def_modules: Set[str] = set()
        use_modules: Set[str] = set()
        with open(filepath, 'r', encoding='utf-8') as f:
            def_m = re.compile(r'^module +(\w+)$')
            use_m = re.compile(r'^use +(\w+)$')
            for line in f:
                line = line.strip()
                m = def_m.match(line)
                if m:
                    def_modules.add(m.group(1))
                m = use_m.match(line)
                if m:
                    use_modules.add(m.group(1))

        return def_modules, use_modules

    def is_dependent_on(self, target: 'FortranFile') -> bool:
        """True if dependents on target file.

        Parameters
        ----------
        target : FortranFile
            target file

        Returns
        -------
        bool
            True if dependents on target file
        """
        return len(self.use_modules & target.def_modules) > 0

    @property
    def filename(self) -> str:
        return str(self.filepath)

    def __str__(self) -> str:
        return self.filename


def search_fortran_files(root: Path,
                         suffix: str = '.f90',
                         recursive: bool = False,
                         osuffix='.o') -> List[FortranFile]:
    if recursive:
        fortran_filepathes = root.glob(f'**/*{suffix}')
    else:
        fortran_filepathes = root.glob(f'*{suffix}')

    fortran_files = []
    for filepath in fortran_filepathes:
        fortran_file = FortranFile(filepath, osuffix=osuffix)
        fortran_files.append(fortran_file)

    return fortran_files


def create_dependencies(fortran_files: List[FortranFile]) -> Dict[FortranFile, FortranFile]:
    dependencies = {fortran_file: list()
                    for fortran_file in fortran_files}

    for file1, file2 in combinations(fortran_files, 2):
        if file1.is_dependent_on(file2):
            dependencies[file1].append(file2)
        if file2.is_dependent_on(file1):
            dependencies[file2].append(file1)

    return dependencies


def create_makefile(args,
                    fortran_files: List[FortranFile],
                    dependencies: Dict[FortranFile, FortranFile],
                    flags: List[str],
                    build_dir: Path,
                    osuffix: str,
                    ):
    objs: List[str] = [(build_dir / file.objname).as_posix()
                       for file in fortran_files]
    mods: List[str] = []
    for file in fortran_files:
        for mod in file.def_modules:
            mod_path = build_dir / '{}.mod'.format(mod)
            mods.append((mod_path).as_posix())

    with open('Makefile', 'w', encoding='utf-8') as f:
        f.write('.PHONY: all clean\n')
        f.write('\n')

        f.write('PROGRAM = {}\n'.format(args.program))
        f.write('OBJS = \\\n\t{}\n'.format(' \\\n\t'.join(objs)))
        f.write('\n')
        f.write('MODS = \\\n\t{}\n'.format(' \\\n\t'.join(mods)))
        f.write('\n')

        f.write('FC = {}\n'.format(args.fc))
        f.write('FLAGS = {}\n'.format(' '.join(flags)))
        f.write('\n')

        f.write('RM = rm -f\n')
        f.write('\n')
        f.write('ifeq ($(OS),Windows_NT)\n')
        f.write('\tRM = powershell del\n')
        f.write('endif\n')
        f.write('\n')

        f.write('all: $(PROGRAM)\n')
        f.write('\t./$(PROGRAM)\n')
        f.write('\n')

        f.write('$(PROGRAM): $(OBJS)\n')
        f.write('\t$(FC) $(FLAGS) -o $(PROGRAM) $^\n')
        f.write('\n')

        for fortran_file in fortran_files:
            obj_to_create = (build_dir / fortran_file.objname).as_posix()

            dependent_objs = [(build_dir / dependent_file.objname).as_posix()
                              for dependent_file in dependencies[fortran_file]]

            dependent_files = '{} '.format(
                fortran_file.filename) + ' '.join(dependent_objs)

            f.write(f'{obj_to_create}: {dependent_files}\n')
            f.write(f'\t$(FC) $(FLAGS) -c $< -o {obj_to_create}\n')
            f.write('\n')

        f.write('clean:\n')
        f.write('\t-$(RM) $(PROGRAM)\n')
        f.write(f'\t-$(RM) {build_dir.as_posix()}/*{osuffix}\n')
        f.write(f'\t-$(RM) {build_dir.as_posix()}/*.mod\n')


def arg_parse():
    parser = argparse.ArgumentParser(description='Makefileを自動で作成する.')

    parser.add_argument('directory', help='Target source directory')
    parser.add_argument('--builddir', '-b', default='build',
                        help='Build directory')
    parser.add_argument('--program', '-p',  default='main.exe',
                        help='Program name to build')
    parser.add_argument('--flags', '-flags', type=str, default='',
                        help='Flags to use')
    parser.add_argument('--suffix', '-suffix', default='.f90',
                        help='Extension of Fortran')
    parser.add_argument('--osuffix', '-osuffix', default='.o',
                        help='Object file suffix')
    parser.add_argument('-fc', '--fc', default='gfortran',
                        help='Fortran compiler to use')
    parser.add_argument('--recursive', '-rc',
                        action='store_true', help='Search recursively')

    return parser.parse_args()


def main():
    args = arg_parse()

    fortran_files = search_fortran_files(
        root=Path(args.directory),
        suffix=args.suffix,
        recursive=args.recursive)
    if len(fortran_files) == 0:
        return

    dependencies = create_dependencies(fortran_files)
    flags = args.flags

    build_dir = Path(args.builddir)
    build_dir.mkdir(exist_ok=True)
    create_makefile(args,
                    fortran_files,
                    dependencies,
                    flags,
                    build_dir=build_dir,
                    osuffix=args.osuffix)


if __name__ == '__main__':
    main()
