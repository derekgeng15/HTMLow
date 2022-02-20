#!/usr/bin/env python3


def create_sections(boxes: list, step: int = 1) -> list:
    s_e = []
    for i in range(len(boxes)):
        s_e.append((boxes[i][step], i))
        s_e.append((boxes[i][step] + boxes[i][step + 2], i))
    s_e.sort()
    i = 0
    tot_size = 0
    tot_oth = 0
    output = []
    while i < len(s_e):
        curr = {}
        curr_boxes = []
        curr[s_e[i][1]] = 1
        curr_boxes.append(boxes[s_e[i][1]])
        if step == 1:
            tot_oth = max(tot_oth, boxes[s_e[i][1]][2])
        elif step == 0:
            tot_oth = max(tot_oth, boxes[s_e[i][1]][3])
        lwr = s_e[i][0]
        upr = 0
        i += 1
        while not len(curr) == 0:
            if s_e[i][1] in curr:
                upr = s_e[i][0]
                del curr[s_e[i][1]]
            else:
                curr_boxes.append(boxes[s_e[i][1]])
                curr[s_e[i][1]] = 1
            i += 1
        tot_size += upr - lwr
        if len(curr_boxes) > 1:
            output.append(create_sections(curr_boxes, 1 - step))
        else:
            output.append(tuple(curr_boxes[0]))
    return [output, (tot_size, tot_oth)]



# container properties
#   flex-direction will be determined by step (1 = row, 2 = column)
#   justify content should always be "space-evenly"
#   align-items should be "stretch"
#   align-content should be "space-around"
# item properties
#   flex-grow determined by proportions of boxes


def generate_content(page, depth: int, element: tuple, step: int, thing: str):
    page.write('    ' * depth + f'<div style="display:flex; padding:10px; flex-direction:{thing}; justify-content: space-evenly; align-items:stretch">\n')
    if element[-2] == 'text':
        page.write('    ' * (depth + 1) + f'<div style="flex-grow:{element[2 + step]}; text-align:center;border: 1px solid; padding:30px; font-family: Poppins, sans-serif;">\n')
        page.write('    ' * (depth + 2) + element[-1] + '\n')
        page.write('    ' * (depth + 1) + '</div>\n')
    elif element[-2] == 'button':
        page.write('    ' * (depth + 1) + f'<button style="flex-grow:{element[2 + step]}; text-align:center;border: 1px solid; padding:30px; font-family: Poppins, sans-serif;">\n')
        page.write('    ' * (depth + 2) + element[-1] + '\n')
        page.write('    ' * (depth + 1) + '</button>\n')
    elif element[-2] == 'header':
        page.write('    ' * (depth + 1) + f'<h1 style="flex-grow:{element[2 + step]}; text-align:center;border: 1px solid; padding:30px; font-family: Poppins, sans-serif;">\n')
        page.write('    ' * (depth + 2) + element[-1] + '\n')
        page.write('    ' * (depth + 1) + '</h1>\n')
    page.write('    ' * depth + '</div>\n')


def create_content(page, nested_boxes: list, step: int = 1, depth: int = 3):
    for element in nested_boxes[0]:
        if type(element) == tuple:
            generate_content(page, depth, element, step, 'column')
        else:
            thing = 'row'
            if step == 0:
                thing = 'column'
            page.write('    ' * depth + f'<div style="display:flex; flex-grow:{element[-1][1]}; flex-direction:{thing}; justify-content: space-evenly; align-items:stretch; align-content:space-around">\n')
            create_content(page, element, 1 - step, depth+1)
            page.write('    ' * depth + '</div>\n')



def create_html(filename: str, nested_boxes: list, path :str = ""):
    page = None
    if path == "":
        page = open(filename, 'w')
    else:
        page = open(path + "\\" + filename, 'w')
    template = open('main_template.html', 'r')
    lines = template.readlines()
    i = 0
    while not lines[i].strip() == '<!--break-->':
        page.write(lines[i])
        i += 1
    create_content(page, nested_boxes)
    page.write(lines[i+1])
    page.write(lines[i+2])
    page.write(lines[i+3])
    

data = [
['5', '10', '700', '100', 'header', 'My Website'],
['10', '150', '150', '110', 'button', 'MIT'],
['200', '150', '200', '105', 'button', 'HHS'],
['10', '265', '400', '200', 'text', 'Im just tryna be inside of you before you wake up'],
['500', '150', '205', '330', 'text', 'Derek G. Tejas K. Pradyun K. Samay D.']
]

for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j].isnumeric():
            data[i][j] = int(data[i][j])
nested_boxes = create_sections(data)
create_html('page.html', nested_boxes)

