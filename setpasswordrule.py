

import re
def applyRUle(rule,text):
    if rule:
        text = "thetext rule matches th policy"
    else:
        text = "the text doesnot matches the policy"

    return text        
txt = input("enter the text to check the policy of ths password: ")
pattern = re.compile("^[A-Z]{3}[^A-Za-z0-9]@^[a-z]{0,2}[0-9]{2,4}$")
# rule = re.fullmatch(pattern,text)
rule = pattern.fullmatch(text)

print(applyRUle(rule))


