sudoku = [[f"{i}-{j}" for j in range(9)] for i in range(9)]
squads = [[] for _ in range(9)]
for i in range(9):
    for j in range(9):
        if i <3 and j <3:
            squads[0].append(sudoku[i][j])
        elif i<3 and 2<j<6:
            squads[1].append(sudoku[i][j])
        elif i<3 and 6<j:
            squads[2].append(sudoku[i][j])
        elif 2<i<6 and j <3:
            squads[3].append(sudoku[i][j])
        elif 2<i<6 and 2<j<6:
            squads[4].append(sudoku[i][j])
        elif 2<i<6 and 6<j:
            squads[5].append(sudoku[i][j])
        elif 6<i and j<3:
            squads[6].append(sudoku[i][j])
        elif 6<i and 2<j<6:
            squads[7].append(sudoku[i][j])
        elif 6<i and 6<j:
            squads[8].append(sudoku[i][j])

print(squads)


print("-"*10)

squads = [[] for _ in range(9)]

for i in range(9):
    c = i//3
    for j in range(9):
        t=j//3
        squads[c+t].append(sudoku[i][j])


print(squads)
