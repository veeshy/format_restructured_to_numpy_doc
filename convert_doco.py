#!/usr/bin/ python3
import os
''''
A script to convert restructured text comments of the generic form to numpy doc string format
'''
def early_return_conversion_and_detection(cl, indent_space):
    """
    Checks for early return if quotes in the string
    Parameters
    ----------
    cl - str
        the line to check if a string is present
    Returns
    -------

    """
    skip_rest_of_conversion = False
    if '"""' in cl:
        cl = cl.rstrip().rstrip('"')
        cl += '\n{0}"""'.format(indent_space)
        skip_rest_of_conversion = True

    return cl, skip_rest_of_conversion

def convert_comments(lines):
    converted_lines = []

    line_iter = iter(lines)
    for line in line_iter:
        if '"""' in line.lstrip()[0:3]:
            first_param_encountered = True
            first_return_encountered = True
            skip_rest_of_conversion = False
            # take executuion away from the outer for loop until another """ found
            # goto next line

            indent_space = ' ' * (len(line) - len(line.lstrip()))

            # check if the comment followed the """ and ended with """:
            if '"""' in line.strip().lstrip('"'):
                # single line comment found, make it multi lined and remove """ to be added in
                converted_lines.append('{0}"""\n{0}{1}\n{0}"""\n'.format(indent_space, line.strip().strip('"')))
                # flag to move on
                skip_rest_of_conversion = True
            elif line.strip().strip('"'):
                # single line comment found on the same line is quotes
                converted_lines.append('{0}"""\n{0}{1}\n'.format(indent_space, line.strip().strip('"')))
                # keep going in case rest of doc string present properly

            else:
                converted_lines.append('{0}"""\n'.format(indent_space))

            if skip_rest_of_conversion:
                # move to next iter
                pass
            else:
                for comment_line in line_iter:
                    if ':param' in comment_line:
                        if first_param_encountered:
                            converted_lines.append('\n{0}Parameters\n{0}----------\n'.format(indent_space))
                            first_param_encountered = False

                        cl = comment_line.replace(':param ', '')

                        # replace the : after the actual param with a colon, type then a newline and 8 spaces
                        # check for ': ' or ':', this breaks if : present in doc string :(
                        if ': ' in cl:
                            cl = cl.replace(': ', ' : type\n{0}    '.format(indent_space))
                        elif ':' in cl:
                            cl = cl.replace(':', ' : type\n{0}    Doc for parameter.'.format(indent_space))

                        cl, skip_rest_of_conversion = early_return_conversion_and_detection(cl, indent_space)
                        converted_lines.append(cl)

                    elif ':return' in comment_line:
                        if first_return_encountered:
                            converted_lines.append('\n{0}Returns\n{0}----------\n'.format(indent_space))
                            first_return_encountered = False
                        # do not return the name of the variable, just the type
                        rl = '{0}type\n{0}    Doc for return.\n'.format(indent_space)
                        rl, skip_rest_of_conversion = early_return_conversion_and_detection(rl, indent_space)
                        converted_lines.append(rl)

                    elif '"""' in comment_line:
                        converted_lines.append('{0}"""\n'.format(indent_space))
                        break
                    else:
                        converted_lines.append(comment_line)

                    if skip_rest_of_conversion:
                        break

        else: # do not touch code
            converted_lines.append(line)

    return converted_lines

if __name__ == "__main__"""
    edit_in_place = False
    extension_to_parse = '.py'
    files = [f for f in os.listdir() if f.endswith(extension_to_parse)]

    # to select a single file:
    #files = ['file_name.ext']
    
    for file in files:
        with open(file, 'r') as f:
            updated = convert_comments(f.readlines())
        
        new_file = file if edit_in_place else 'converted_' + file
        with open(new_file, 'w') as o:
            for l in updated:
                o.write(l)

