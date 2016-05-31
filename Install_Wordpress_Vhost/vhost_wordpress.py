import mysql.connector
import os
conn = mysql.connector.Connect(host='127.0.0.1',user='root',password='trung')
c = conn.cursor()


#Ham sua thong tin theo dong trong 1 file
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
#Ham lay ra tung domain dua vao MANGD va tung domain sub dua vao MANGDSUB trong file domain.txt
MANG = []
def Tach_Dl():
	fp = open('/home/dell/Vhost/domain_user.txt')
	while 1:
		line = fp.readline()
		if not line:
			break
		full = line.split('\n')
		span = full[0].split('#')
		subdomain = span[0].split('.')
		MANG.append([span[0],subdomain[0],span[1],span[2]])	

#Ham cai dat Vhost tuong ung voi moi domain
def Setup_Vhost(domain):
	os.system('mkdir /var/www/'+domain)
	fileconf = domain+".conf"
	linkconf = '/etc/apache2/sites-available/'+fileconf
	serverName = "\tServerName "+domain+"\n"
	serverAlias = "\tServerAlias www."+domain+"\n"
	docmentRoot = "\tDocumentRoot /var/www/"+domain+"/wordpress/\n"
	os.system('cp /etc/apache2/sites-available/000-default.conf '+linkconf)
	replace_line(linkconf, 8, serverName)
	replace_line(linkconf, 9, serverAlias)
	replace_line(linkconf, 11, docmentRoot)
	os.system('sudo a2ensite '+fileconf)

#Ham tao database, user, password tuong ung voi tung domain
def Create_DB(domainsub, user, passwd):
	sql = "CREATE DATABASE IF NOT EXISTS "+domainsub
	c.execute(sql)
	conn.commit()
	sql = "CREATE USER "+user+"@localhost IDENTIFIED BY '"+passwd+"'"
	c.execute(sql)
	conn.commit()
	sql = "GRANT ALL PRIVILEGES ON "+domainsub+".* TO "+user+"@localhost"
	c.execute(sql)
	conn.commit()
	sql = "FLUSH PRIVILEGES"
	c.execute(sql)
	conn.commit()

#Ham cai dat wordpress
def Install_Wordpress(domain, domainsub, user, passwd):
	os.system("cd /var/www/"+domain+"/ && tar -xvzf /home/dell/latest.tar.gz")
	os.system("cd /var/www/"+domain+"/wordpress/ && cp wp-config-sample.php wp-config.php")
	filename = "/var/www/"+domain+"/wordpress/wp-config.php"
	dbname = "\tdefine('DB_NAME', '"+domainsub+"');\n"
	dbuser = "\tdefine('DB_USER', '"+user+"');\n"
	dbpassword = "\tdefine('DB_PASSWORD', '"+passwd+"');\n"
	replace_line(filename, 22,dbname)
	replace_line(filename, 25,dbuser)
	replace_line(filename, 28,dbpassword)
	os.system("chown -R www-data:www-data /var/www/"+domain+"/wordpress/")


def Run():
	Tach_Dl()
	for domain in MANG:
		Setup_Vhost(domain[0])
		Create_DB(domain[1],domain[2],domain[3])
		Install_Wordpress(domain[0],domain[1],domain[2],domain[3])
	os.system('service apache2 restart')
	

Run()
