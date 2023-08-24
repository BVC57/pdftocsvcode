import pandas as pd 
import numpy as np

def split(text, part, splitby="/"):
    try:
        return text.split(splitby)[part]
    except:
        return text

def find_values(tables, search_text, col):
    row_idx = find_row_index(tables, search_text)
    if row_idx >= 0:
        return tables[row_idx[0]][col] if tables[row_idx[0]][col] else ""
    return ""

def find_row_index(table, search_text):
    df = pd.DataFrame(table).fillna("")
    mask = np.column_stack([df[col].str.contains(search_text) for col in df.columns])
    # Use np.where to return the indices where the mask is True
    matching_indices = np.where(mask == True)[0]
    return matching_indices        

def find_address(data):
    text = ""
    for row in data[1:]:
        if "D CODE"  in row[1]:
            break
        text += row[1] + " "
    return text

def remove_empty_elements(nested_list):
    if isinstance(nested_list, list):
        return [x for x in nested_list if "".join(x).strip() != ""] 
        # return [x for x in nested_list if "".join(str(elem) for elem in x).strip() != ""]
        
    else:
        # If the input is not a list, return the element
        return nested_list
    
def remove_float_empty_elements(nested_list):
    if isinstance(nested_list, list):
        # return [x for x in nested_list if "".join(x).strip() != ""] 
        return [x for x in nested_list if "".join(str(elem) for elem in x).strip() != ""]
        
    else:
        # If the input is not a list, return the element
        return nested_list
