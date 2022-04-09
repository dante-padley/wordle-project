import fileinput

lines = []
for line in fileinput.input():
    lines.append(line)
    
    
print(lines)