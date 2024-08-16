import re, sys


def detect_new_item(s):
    r = r"### \*\*(.*?)\*\*"
    x = re.findall(r, s)
    if x:
        return f".SS {x[0]}\n"
    return False

def detect_code_block(s):
    if s == "```\n":
        return True
    return False

def detect_alias(s):
    if "Alias:" in s:
        r = r"Alias: \*(.*?)\*"
        x = re.findall(r, s)
        if x:
            return f".TP\n\\fBAlias:\\fR\n{x[0]}.\n"
        return f".TP\n\\fBAlias:\\fR\nXXXXXXXXX.\n" # uninplemented
    else:
        return False

def detect_inputs(s):
    if "Inputs:" in s:
        r = r"Inputs: \*(.*?)\*"
        x = re.findall(r, s)
        if x:
            return f".TP\n\\fBInputs:\\fR\n{x[0]}.\n"
        else:
            return "LINES" # get lines untill outputs = true
    else:
        return False
    
def detect_outputs(s):
    if "Outputs:" in s:
        return f".TP\n\\fBOutputs:\\fR\n"
    return False

def parse_inputs(s):
    if not s.lstrip()[0] == "*":
        return False
    ws = 0
    if len(s) - len(s.lstrip()):
        ws = len(s) - len(s.lstrip()) 
        ws += 7
    r = r"\* \*(.*?)\*(.*)"
    x = re.findall(r, s)
    if not x:
        r = r"\* (.*?) \- (.*)"
        x = re.findall(r, s)
        if not x or not len(x[0]) == 2:
            x = [[s[1:].lstrip().strip(), ""]]
            print(x)
            if ws:
                return f".RS {ws}\n\[bu] \\fB{x[0][0]}\\fR\n.RE\n" 
            return f"\[bu] \\fB{x[0][0]}\\fR\n\n"
        if ws:
            return f".RS {ws}\n\[bu] \\fB{x[0][0]}\\fR - {x[0][1]}\n.RE\n" 
        return f"\[bu] \\fB{x[0][0]}\\fR - {x[0][1]}\n\n"
    if not len(x[0]) == 2:
        return "XXXXXX"
    if ws:
        return f".RS {ws}\n\[bu] \\fB{x[0][0]}\\fR{x[0][1]}\n.RE\n" 
    return f"\[bu] \\fB{x[0][0]}\\fR{x[0][1]}\n\n"

def detect_examp(s):
    if s == "Example:\n":
        return """.TP
.B Example:
"""
    elif "example" in s.lower():
        return f""".TP
.B Example:
{s}
"""
    else:
        return False

    

nitem = False
falias = False
Lines = False
outsWithoutLines = False
outs = False
exp = False
codep1 = True
roff = ""

ll = 0

# Check if at least one argument is provided
if not len(sys.argv) > 1:
    print("No arguments were provided, pass input full path")

infile = sys.argv[1]
# https://github.com/monero-project/monero-site/blob/master/resources/developer-guides/daemon-rpc.md
with open(infile, 'r') as f:
    for s in f:
        # if ll == 200:
        #     break
        ll += 1
        # s = s.strip()
        print(repr(s), ll)
        if s == "\n":
            roff += "\n"
            print("SPAAACEEE", ll)
            continue
        x = detect_new_item(s)
        if x:
            nitem = True
            roff += x
            continue
        if nitem:
            # look for alias if not add text
            x = detect_alias(s)
            if not x:
                x = detect_inputs(s)
                if x:
                    falias = True
                    nitem = False
                else:
                    roff += s
                    continue
            else:
                falias = True
                nitem = False
                roff += x
                continue
        if falias:
            # finished alias look for inputs otherwise add text
            x = detect_inputs(s)
            if not x:
                roff += s + "\n"
                print("Looking for inputs after alias finished")
                continue
            else:
                if x == "LINES":
                    roff += f".TP\n\\fBInputs:\\fR\n"
                    Lines = True
                    falias = False
                    continue
                else:
                    roff += x + "\n"
                    falias = False
                    Lines = False # skip to outputs 
                    outsWithoutLines = True
                    continue
        if outsWithoutLines:
            x = detect_outputs(s)
            if x:
                roff += x
                outs = True
                outsWithoutLines = False
                continue
            roff += s
            print("finished inputs strings lines looking for output")
            continue
        if Lines:
            # take all input lines parse and add them till outputs
            x = parse_inputs(s)
            if x:
                roff += x
                continue
            # look for outputs if not add text
            x = detect_outputs(s)
            if x:
                roff += x
                outs = True
                Lines = False
                continue
            roff += s
            print("finished inputs strings lines looking for output")
            continue
        if outs:
            x = parse_inputs(s)
            if x:
                roff += x
                continue
            # no out items??? look for example if not add text
            x = detect_examp(s)
            if x:
                roff += x
                outs = False
                exp = True
                continue
            roff += s
            print("finished outs inputs looking for examples")
            continue
        if exp:
            x = detect_code_block(s)
            if x:
                codep1 = True
                roff += ".nf\n.RS 4\n"
                exp = False
                continue
            roff += s
            print("looking for code block expl finish")
            continue
        if codep1:
            x = detect_code_block(s) # code end
            if x:
                codep1 = False
                roff += "\n.RE\n.fi\n"
                exp = True
                # another text/code? add it if not ? try new_item
                continue
            roff += s
            print("looking for code block expl finish")
            continue
        

q = open("pyout.1", "w")
q.write(roff)
q.close()




