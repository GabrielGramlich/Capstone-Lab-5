import sqlite3

DATABASE = 'juggling_records.sqlite'

def main():
	create_table()
	while True:
		choice = choose_option()
		if choice == 'E':
			break
		else:
			perform_action(choice)


def create_table():
	with sqlite3.connect(DATABASE) as connection:
		connection.execute('CREATE TABLE IF NOT EXISTS records (name text, country text, juggles int)')
	connection.close()


def choose_option():
	valid_choices = ['C','R','U','D','E']
	choice = ''

	choice = input('Would you like to \'C\'reate, \'R\'ead, \'U\'pdate or \'D\'elete a record, or \'E\'xit the program? ').upper()
	while choice not in valid_choices:
		print('Invalid choice. Must select \'C\', \'R\', \'U\', \'D\' or \'E\'.')
		choice = input('Would you like to \'C\'reate, \'R\'ead, \'U\'pdate or \'D\'elete a record, or \'E\'xit the program? ').upper()

	return choice


def perform_action(choice):
	if choice == 'C':
		perform_create()
	elif choice == 'R':
		perform_read()
	elif choice == 'U':
		perform_update()
	elif choice == 'D':
		perform_delete()



def perform_create():
	name = get_info('What is the juggler\'s name? ').title()
	country = get_info('What is the juggler\'s country? ').title()
	juggles = get_info('How many juggles did the juggler juggle? ')
	create_row(name,country,juggles)


def get_info(message):
	response = input(message)
	return response


def create_row(name, country, juggles, table='records'):
	with sqlite3.connect(DATABASE) as connection:
		insert = f'INSERT INTO {table} values (?, ?, ?)'
		connection.execute(insert, (name,country,juggles))
	connection.close()


def perform_read():
	is_all = get_boolean('Would you like to view all records, or just one? (\'A\'/\'o\') ', 'a')
	if is_all:
		rows = read_rows()
	else:
		name = get_info('What is the juggler\'s name? ').title()
		rows = read_row(name)
	display_rows(rows)


def get_boolean(message, true_value):
	is_true = input(message).lower()
	if is_true == true_value:
		return True
	else:
		return False


def read_rows(table='records'):
	results = []

	connection = sqlite3.connect(DATABASE)
	select = f'SELECT * FROM {table}'
	rows = connection.execute(select)
	for row in rows:
		results.append(row)
	connection.close()
	return results


def read_row(value, key='name', rows='*', table='records'):
	results = []

	connection = sqlite3.connect(DATABASE)
	select = f'SELECT {rows} FROM {table} WHERE {key} = ?'
	rows = connection.execute(select, (value,))
	for row in rows:
		results.append(row)
	connection.close()
	return results


def display_rows(rows):
	for row in rows:
		print(f'{row[0]} from {row[1]} juggled {row[2]} juggles!')


def perform_update():
	is_juggles = get_boolean('Update juggles or country? (\'J\'/\'c\') ', 'j')
	name = get_info('For which juggler? ').title()
	if is_juggles:
		juggles = get_info('What is the juggler\'s new juggle record? ')
		update_row(juggles,name,'juggles')
	else:
		country = get_info('What is the juggler\'s new country? ').title()
		update_row(country,name,'country')


def update_row(set_value,where_value,set_column='juggles',where_column='name',table='records'):
	with sqlite3.connect(DATABASE) as connection:
		update = f'UPDATE {table} SET {set_column} = ? WHERE {where_column} = ?'
		connection.execute(update, (set_value,where_value))
	connection.close()


def perform_delete():
	name = get_info('Which juggler would you like to delete? ').title()
	delete_row(name)


def delete_row(delete_value,delete_column='name',table='records'):
	with sqlite3.connect(DATABASE) as connection:
		delete = f'DELETE FROM {table} WHERE {delete_column} = ?'
		connection.execute(delete, (delete_value, ))
	connection.close()


if __name__ == '__main__':
	main()
