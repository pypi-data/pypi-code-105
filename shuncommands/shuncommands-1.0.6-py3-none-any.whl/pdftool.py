#!/usr/bin/env python3

from pathlib import Path

import click
from pdfminer.high_level import extract_text
from pikepdf import Pdf


@click.group()
@click.version_option(None, '-v', '--version')
@click.help_option('-h', '--help')
def ctx():
    '''
    \b
    PDF file をあれやこれやしたいがためのコマンド
    '''


@ctx.command()
@click.version_option(None, '-v', '--version')
@click.help_option('-h', '--help')
@click.option('password', '-p',
              help='decrypt password',
              prompt=True,
              hide_input=True)
@click.option('--output', '-o',
              help='output decrypt pdf filename [default: <pdffile>.unlock.pdf]',  # noqa: E501
              type=click.Path())
@click.option('--force', '-f',
              help='<output> override',
              is_flag=True)
@click.argument('pdffile',
                required=True,
                type=click.Path(exists=True))
def unlock(pdffile, output, password, force):
    '''
    パスワード付きPDFファイルを、パスワードなしPDFファイルにコピーする
    '''
    click.echo(f'input pdf file: {pdffile}')
    lockpdf = Pdf.open(pdffile, password=password)
    unlockpdf = Pdf.new()
    unlockpdf.pages.extend(lockpdf.pages)
    if output is None:
        output = Path(pdffile).with_suffix('.unlock.pdf')
    else:
        output = Path(output)
    if output.exists() and not force:
        click.confirm(f'{output} is exists. Do you want to override?',
                      default=True,
                      abort=True,
                      show_default=True)

    unlockpdf.save(output)
    click.echo(f'output pdf file: {output}')


@ctx.command()
@click.version_option(None, '-v', '--version')
@click.help_option('-h', '--help')
@click.option('password', '-p',
              help='decrypt password')
@click.option('--output', '-o',
              help='output filename',
              type=click.Path())
@click.option('--force', '-f',
              help='<output> override',
              is_flag=True)
@click.option('--strip', '-s',
              help='strip to output line',
              is_flag=True)
@click.option('--remove-zero-line', '-0',
              help='remove zero length line and strip',
              is_flag=True)
@click.argument('pdffile',
                required=True,
                type=click.Path(exists=True))
def text(pdffile, output, password, force, strip, remove_zero_line):
    '''
    PDFファイルを、テキストファイルに変換する
    '''
    click.echo(f'input pdf file: {pdffile}')
    if password is not None:
        click.echo('pdf file password: xxx')
    else:
        password = ''
    pdf_text = extract_text(pdffile, password)
    pdf_text_list = pdf_text.split('\n')
    if strip or remove_zero_line:
        _pdf_text_list = [line.strip() for line in pdf_text_list]
        pdf_text_list = _pdf_text_list
    if remove_zero_line:
        _pdf_text_list = [line for line in pdf_text_list if len(line) > 0]
        pdf_text_list = _pdf_text_list
    if not output:
        click.echo('\n'.join(pdf_text_list))
    else:
        output_path = Path(output).expanduser()
        if output_path.exists() and not force:
            click.confirm(f'{output} is exists. Do you want to override?',
                          default=True,
                          abort=True,
                          show_default=True)
        with output_path.open('w') as fd:
            fd.write('\n'.join(pdf_text_list))
        click.echo(f'output to {output}')
