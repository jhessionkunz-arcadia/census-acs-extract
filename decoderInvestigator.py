with open('dataOutput/blockGroup-99vars-export-3-20241217-193739.csv', 'rb') as f:
    data = f.read()

problem_byte = data[4708]
print(f"Byte at position 4708: {hex(problem_byte)}")