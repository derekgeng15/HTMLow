#!/usr/bin/env python3

def generate_cols(cols: list, page):
    template = open('col_template.html', 'r')
    lines = template.readlines()
    for col in cols:
        page.write(lines[0])
        page.write(f'                   {col}\n')
        page.write(lines[1])


def generate_rows(rows: list, page):
    template = open('row_template.html', 'r')
    lines = template.readlines()
    for cols in rows:
        page.write(lines[0])
        generate_cols(cols, page)
        page.write(lines[1])

def main(filename: str, rows: list):
    page = open(filename, 'w')
    template = open('main_template.html', 'r')
    lines = template.readlines()
    i = 0
    while not lines[i].strip() == '<!--break-->':
        page.write(lines[i])
        i += 1
    generate_rows(rows, page)
    page.write(lines[i+1])
    page.write(lines[i+2])
    page.write(lines[i+3])

