from enum import Enum

class BlockType(Enum):
    heading = "heading"
    quote = "quote"
    code = "code"
    ordered_list = "ordered_list"
    unordered_list = "unordered list"
    paragraph = "paragraph"

def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return "heading"
    
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    
    elif block.startswith(">"):
        block_list = block.split("\n")
        for each in block_list:
            if not each.startswith(">"):
                return "paragraph"
        return "quote" 
    
    elif block.lstrip().startswith(("*", "-")):
        block_list = block.split("\n")
        for line in block_list:
            stripped_line = line.strip()
            if not stripped_line:  # Skip empty lines
                continue
            if not (stripped_line.startswith("*") or stripped_line.startswith("-")):
                return "paragraph"
        return "unordered_list"
    
    elif block[0].isdigit():
        try:
            find_num = block.split(".",1)
            if len(find_num) != 2:  # no period found
                return "paragraph"
            if not find_num[1].startswith(" "):  # no space after period
                return "paragraph"
            first_number = int(find_num[0])
            if first_number != 1:
                return "paragraph"
            
            number_count = first_number
            block_list = block.split("\n")
            for block in block_list:
                find_num = block.split(".",1)
                if len(find_num) != 2:  # no period found
                    return "paragraph"
                if not find_num[1].startswith(" "):  # no space after period
                    return "paragraph"
                next_number = int(find_num[0])
                if next_number != number_count:
                    return "paragraph"
                number_count = number_count +1
            return "ordered_list"
        except ValueError:
            return "paragraph"
    
    else:
        return "paragraph"