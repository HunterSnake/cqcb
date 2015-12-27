insert tb_page_type (id,ename,cname,dest_folder) values (1,'new','新闻中心','news'),
					(2,'introduce','企业咨询','introduces'),
					(3,'process','办事流程','process'),
					(4,'law','政策法规','laws'),
					(5,'template','合同文本','templates'),
					(6,'announcement','最新公告','announcements');
select * from tb_page_type;

describe tb_sources;
select * from tb_sources
insert tb_sources (typeId,firstpageurl,pagecount, re_page_dest, re_page_replacement, re_title, re_link)
	values(1, 'http://www.cqcb.net/cqcb_net/news/list_1.htm', 8, 'list_\d+')