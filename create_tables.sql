drop table if exists todos;
create table todos (
	id integer primary key autoincrement, 
	todo_text text not null, 
	priority integer, 
	completed boolean not null

	
); 