from textwrap import wrap
import re
import argparse

################################ Define Helper Fields and Functions ################################

rows = 'ABCDEFGHI'
cols = '123456789'

def get_squares():
	# Get squares for standard 3x3 board
	def cross(A,B):
		# Crosses rows and columns
		return [a+b for a in A for b in B] 
	return [cross(row,cols) for row in rows]

def get_units(square):
	# Returns units of given square
	wrapped_rows = wrap(rows,3)
	wrapped_cols = wrap(cols,3)
	row_units = [row+square[1] for row in rows]
	col_units = [square[0]+col for col in cols]
	region_rows = wrapped_rows[rows.index(square[0]) // 3]
	region_cols = wrapped_cols[cols.index(square[1]) // 3]
	region_units = [row+col for  row in region_rows for col in region_cols]
	unit_list = [row_units,col_units,region_units]
	return(unit_list)

def get_peers(square):
	return set([unit for sublist in get_units(square) for unit in sublist if unit != square])

def parse_data(data,number='all'):
	# Parses text file data and yields grids in list form
	# If a certain puzzle is queried, only returns that puzzle
	grid = []
	with open(data) as file:
		line = file.readline()
		if number == 'all':
			while line:
				if re.search('Grid',line):
					grid_num = int(line.rstrip()[4:])
				else:
					grid.append(list(line.rstrip().replace('0','.')))
				line = file.readline()
				if len(grid) == 9:
					yield grid,grid_num
					grid = []
		else:
			match = 'Grid ' + number
			while line.rstrip() != match:
				line = file.readline()
			line = file.readline()
			while line:
				grid.append(list(line.rstrip().replace('0','.')))
				line = file.readline()
				if len(grid) == 9:
					yield grid,number

def convert(grid):
	# Converts string grid to dict grid and vice versa
	if type(grid) is dict:
		return [[grid[row+col] for col in cols] for row in rows]
	elif type(grid) is list:
		dgrid={}
		for i,row in enumerate(rows):
			for j,col in enumerate(cols):
				dgrid[row+col] = grid[i][j]
		return dgrid
	else: return False

def string_grid(grid=get_squares()):
	# Converts list grid into string grid to be displayed
	if type(grid) == dict:
		grid = convert(grid)
	if grid is None: return 'None'
	assert len(grid) == 9
	assert len(grid[0]) == 9
	board_length = len(''.join(grid[0])) + 12
	grid_string = ''''''
	for i,row in enumerate(grid):
		grid_string += ('{} {} {} | {} {} {} | {} {} {}\n').format(*[square for square in row])
		if (i+1) % 3 == 0 and (i+1) != 9:
			grid_string += '-' * board_length + '\n'
	return grid_string

def process_grid(grid):
	# Processes initial grid so that unknown values are the string of possible digits
	lgrid = []
	for row in grid:
		lgrid.append([value if value != '.' else '123456789' for value in row])
	return convert(lgrid)

# Define dictionaries for units and peers
units = {}
peers = {}
for row in rows:
	for col in cols:
		units[row+col] = get_units(row+col)
		peers[row+col] = get_peers(row+col)

################################ Define Strategies ################################  

def eliminate(grid,square):
	assert type(grid) is dict
	if len(grid[square]) == 1:
		value = grid[square]
		for peer in peers[square]:
			grid[peer] = grid[peer].replace(value,'')
	return grid

def only_choice(grid,square):
	assert type(grid) is dict
	if len(grid[square]) > 1:
		for value in grid[square]:
			if all([value not in peer for peer in peers[square]]):
				grid[square] = value
				break
	return grid

def naked_twins(grid,square):
	assert type(grid) is dict
	if len(grid[square]) == 2:
		value = grid[square]
		twin = ''
		for peer in peers[square]:
			if value == grid[peer]:
				twin = peer
				break
		if twin == '': return
		for peer in peers[square].intersection(peers[twin]):
			grid[peer] = grid[peer].replace(value[0],'')
			grid[peer] = grid[peer].replace(value[1],'')
	return grid

def reduce_grid(grid):
	# Reduces grid using all 3 strategies
	prev_grid = {}
	while prev_grid != grid:
		prev_grid = grid.copy()
		for square in grid.keys():
			eliminate(grid,square)
			only_choice(grid,square)
			naked_twins(grid,square)
	return grid

################################ Define Search ################################

def contradiction(grid):
	# Detects wheter or not grid contains contradiction
	for square in grid.keys():
		if len(grid[square]) == 1:
			if grid[square] in [grid[peer] for peer in peers[square]]:
				return False
		elif grid[square] == '':
			return False
	return grid

def solved(grid):
	# Returns True if grid is solved
	return all([len(value) == 1 for value in grid.values()])

def search(grid):
	if grid is False: return False # Previous call to contradiction returns False
	if solved(grid): return grid # Solved puzzle
	min_square = min(grid,key=lambda s: len(grid.get(s)) if len(grid.get(s)) > 1 else 10)
	for value in grid[min_square]:
		newgrid = grid.copy()
		newgrid[min_square] = value
		reduce_grid(newgrid) # Reduce again before searching
		sol = search(contradiction(newgrid))
		if sol is not False: # Found a valid value for min_square
			return sol
	return False # This branch does not correspond to any valid puzzle configurations, backtrack

################################ Main Function ################################

def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-n','--number',type=str,default='all')
	args = parser.parse_args()

	# Main loop
	for grid,number in parse_data('p096_sudoku.txt',args.number):
		print('='*30 + ' Grid {} '.format(number) + '='*30 + '\n')
		print('Unsolved Grid')
		print(string_grid(grid))
		grid = process_grid(grid)
		reduce_grid(grid)
		if solved(grid):
			print('Solved Only Using Contraint Propagation')
			print(string_grid(grid))
		else:
			temp_grid = {k: v if len(v) == 1 else '.' for k,v in grid.items()}
			print('State After Constraint Propagation')
			print(string_grid(temp_grid))
			solution = search(grid)
			print('Solved After Backtracking Search')
			print(string_grid(solution))

if __name__ == '__main__':
	main()