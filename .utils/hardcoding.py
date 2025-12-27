import os, sys, json, csv, re

def remove_comments(source_code):
    clean_code = []
    inside_multiline_comment = False

    for line in source_code:
        # check if inside a multi-line comment block
        if inside_multiline_comment:
            if "'''" in line or '"""' in line:
                inside_multiline_comment = False
                # remove everything up to the closing triple quotes
                line = line.split("'''", 1)[-1] if "'''" in line else line.split('"""', 1)[-1]
            continue  

        # single-line comments
        singleline_index = line.find("#")
        if singleline_index != -1:
            line = line[:singleline_index]  # remove the comment starting from #

        # multi-line comments
        multiline_start = line.find("'''") if "'''" in line else line.find('"""')
        if multiline_start != -1:
            inside_multiline_comment = True
            # remove everything after the opening triple quotes
            line = line[:multiline_start]

        # add cleaned line if not empty
        if line.strip():
            clean_code.append(line)

    return clean_code

def preprocess(source_code):
    if type(source_code) == list:
        code = remove_comments(source_code)
        processed_code = ""
        for line in code:
            if not line.strip():
                continue
            processed_code += line + " "
        code = processed_code
    else:
        code = source_code

    return code.replace("\n", "")

def check_hardcoding(source_code, answer, dtype, qnum):
    '''
    Want to check the following cases:
        - `var_name = answer`
        - `return answer`
        - answer is the last line (i.e answer is being outputed without being modified)
    '''

    expected = preprocess(answer)
    code = preprocess(source_code)

    assignment_pattern =  lambda x : rf"\s*([a-zA-Z_]\w*)\s*=\s*({re.escape(x)})\b\s*"
    output_pattern = lambda x : rf"^\s*({re.escape(x)})\b\s*"
    return_pattern = lambda x: rf"\s*return\s+({re.escape(x)})\b" 
    function_pattern = r"def\s+(\w+)\s*\("

    output = []

    if dtype == "bool" or dtype == "NoneType":
        return output

    # CASE 1: answer is assigned to a variable and outputted later
    assignment_regex = re.compile(assignment_pattern(expected))
    assignments = assignment_regex.findall(code)
    
    for var, value in assignments:
        output_regex = re.compile(output_pattern(var))
        found = output_regex.findall(source_code[-1])

        if found:
            output.append(f"The value `{value}` was assigned to the variable `{var}` and used as the result of question {qnum}.")

    # CASE 2: answer is outputted directly
    output_regex = re.compile(output_pattern(expected))
    found = output_regex.findall(source_code[-1])

    if found:
        output.append(f"`{expected}` was hardcoded as the result of question {qnum}.")
    
    # CASE 3: hardcoded answer is returned from a function
    return_regex = re.compile(return_pattern(expected))
    function_regex = re.compile(function_pattern)
    
    # find all functions and their start positions
    function_positions = [
        (match.group(1), match.start()) for match in function_regex.finditer(code)
    ]
    
    # find all return matches
    return_matches = return_regex.finditer(code)
    
    # map return values to the functions they belong to
    results = []
    
    for match in return_matches:
        return_start = match.start()
        # find the function enclosing the return statement
        enclosing_function = None
        for func_name, func_start in function_positions:
            if func_start < return_start:
                enclosing_function = func_name
            else:
                break
        results.append((enclosing_function, match.group(1)))
    
    for func, value in results:
        output_regex = re.compile(output_pattern(func))
        found = output_regex.findall(source_code[-1])

        if found:
            output.append(f"The value '{value}' is returned by the function '{func}' and used as the result of question {qnum}.")
            break

    return output
