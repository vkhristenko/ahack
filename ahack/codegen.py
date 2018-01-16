"""
Code Generation Module: generate code for given mnemonics of the Hack Assembly Language
"""

import defs

def dest(dest_string):
    if dest_string == None:
        return "000"
    else:
        return defs.dests[dest_string]

def comp(comp_string):
    return defs.comps[comp_string]

def jump(jump_string):
    if jump_string == None:
        return "000"
    else:
        defs.jumps[jump_string]
