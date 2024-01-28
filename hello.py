import numpy as np 
import re
import sys

def extract_dollar_amount(text):
    # The regular expression pattern for a dollar amount
    pattern = r'\$(\d+)(?=[\.\s]|$)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Remove the dollar sign and convert to integers
    amounts = [int(match) for match in matches]
    
    return amounts


msg="Here we go!"
print(msg)

sampletext = input("Enter your text")
print(sampletext)

dollars = extract_dollar_amount(sampletext)

print(dollars)
