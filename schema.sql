SHOW ENGINE INNODB STATUS;

drop table tb_page_type
create table tb_page_type (id int not null,
						  ename varchar(255) not null unique,
                          cname varchar(255) not null unique,
                          dest_folder varchar(255) not null,
                          primary key (id));


drop table tb_sources;                     
create table tb_sources ( id int not null auto_increment,
						  typeId int not null,
						  firstpageurl varchar(255) not null unique,
                          pagecount int not null,
                          re_page_dest varchar(255) not null,
                          re_page_replacement varchar(255) not null,
                          re_title varchar(255) not null,
                          re_link varchar(255) not null,
                          primary key (id),
                          constraint foreign key(typeId) references tb_page_type(id)
                          ON DELETE  RESTRICT  ON UPDATE CASCADE);
                                                  

describe tb_sources;
select * from tb_sources;
                          
create table tb_titles (id int not null auto_increment,
						typeId int not null,
						title varchar(255) not null,
						link varchar(255) not null,
						primary key (id),
						constraint foreign key(typeId) references tb_page_type(id)
						ON DELETE  RESTRICT  ON UPDATE CASCADE);
describe tb_titles;
                          
						