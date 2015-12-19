import os
import time
import psycopg2
import urlparse
import hashlib
import json
from bottle import Bottle, response, request
from psycopg2.extras import RealDictCursor

app = Bottle(__name__)
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])



@app.route('/signup/<username>/<email>/<phone_no>/<passwd>')
def signup(username,email,phone_no,passwd):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = username
	var2 = email
	var3 = phone_no
	var4 = passwd

	hash_object = hashlib.sha256(str(var4))
	new_passwd = str(hash_object.hexdigest())

	sql = "INSERT INTO public.\"User\" VALUES ('"+str(var1)+"','"+str(var2)+"','"+str(var3)+"','"+new_passwd+"')"

	cur.execute(sql)

	conn.commit()
	cur.close()
	conn.close()

	return "1"

@app.route('/login/<username>/<passwd>')
def signup(username,passwd):

	response.headers['Access-Control-Allow-Origin'] = '*'

	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = username
	var2 = passwd

	hash_object = hashlib.sha256(str(var2))
	new_passwd = str(hash_object.hexdigest())

	sql = "SELECT passwd FROM public.\"User\" WHERE username='"+str(var1)+"'"

	cur.execute(sql)

	res = cur.fetchone()
	res = str(res[0])

	if new_passwd == res :
		return "{\"login\":{\"status\":\"1\"}}"
	else :
		return "{\"login\":{\"status\":\"0\"}}"


@app.post('/new_poll')
def new_poll():

	response.headers['Access-Control-Allow-Origin'] = '*'

	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	image_url = "http://kqulo.com/poll_images/"

	cur = conn.cursor()

	var1 = request.forms.get('p_user')
	var2 = request.forms.get('p_name')
	var3 = request.forms.get('p_location')

	#return str(var2)

	
	sql = "SELECT COUNT(*) FROM public.\"Polls\" WHERE p_user='"+str(var1)+"'"

	cur.execute(sql)

	res = cur.fetchone()
	res = res[0]

	p_id = str(var1)+"_"+str(res + 1)
	p_image = image_url+p_id+".jpg"

	os.environ['TZ'] = 'Asia/Calcutta'
	time.tzset()

	p_date = str(time.strftime("%d-%m-%Y"))
	p_time = str(time.strftime("%H:%M:%S"))

	sql = "INSERT INTO public.\"Polls\" VALUES ('"+p_id+"','"+str(var1)+"','"+str(var2)+"','"+str(var3)+"','"+p_image+"',0,0,'"+p_date+"','"+p_time+"')"

	cur.execute(sql)

	conn.commit()
	cur.close()
	conn.close()

	return "{\"new_poll\":{\"status\":\"1\"}}"

@app.route('/up_vote/<p_user>/<p_name>')
def up_vote(p_user,p_name):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = p_user
	var2 = p_name

	sql = "SELECT EXISTS(SELECT p_up_vote FROM public.\"Votes\" WHERE p_user='"+str(var1)+"' AND p_name='"+str(var2)+"')"

	cur.execute(sql)

	res = cur.fetchone()

	if(res == "false"):
		sql = "INSERT INTO public.\"Votes\" (p_name,p_user,p_up_vote,p_down_vote,v_date,v_time) VALUES ('"+str(var2)+"','"+str(var1)+"',1,0,'"+v_date+"','"+v_time+"')"
		
		cur.execute(sql)

		conn.commit()



		sql = "SELECT p_up_votes,p_down_votes FROM public.\"Polls\" WHERE p_name='"+str(var2)+"'"

		cur.execute(sql)

		res = cur.fetchall()

		up_vote_count = res[0][0]
		down_vote_count = res[0][1]

		if down_vote_count == 0:
			down_vote_count = 1

		sql = "UPDATE public.\"Polls\" SET p_up_votes="+str(up_vote_count+1)+",p_down_votes="+str(down_vote_count-1)+" WHERE p_name='"+str(var2)+"'"

		cur.execute(sql)

		conn.commit()
		cur.close()
		conn.close()

		return "1"

		

	else:

		sql = "SELECT p_up_vote FROM public.\"Votes\" WHERE p_user='"+str(var1)+"'AND p_name='"+str(var2)+"'"

		cur.execute(sql)

		res = cur.fetchall()

		length = len(res)

		#print length

		if length == 0 :
			res = 0 
		else :
			res = res[length-1][0]

		print str(res)

		if (str(res) == "None")|(str(res) == "0") :

			os.environ['TZ'] = 'Asia/Calcutta'
			time.tzset()

			v_date = str(time.strftime("%d-%m-%Y"))
			v_time = str(time.strftime("%H:%M:%S"))

			sql = "INSERT INTO public.\"Votes\" (p_name,p_user,p_up_vote,p_down_vote,v_date,v_time) VALUES ('"+str(var2)+"','"+str(var1)+"',1,0,'"+v_date+"','"+v_time+"')"

			cur.execute(sql)

			conn.commit()

			sql = "SELECT p_up_votes,p_down_votes FROM public.\"Polls\" WHERE p_name='"+str(var2)+"'"

			cur.execute(sql)

			res = cur.fetchall()

			up_vote_count = res[0][0]
			down_vote_count = res[0][1]

			if down_vote_count == 0:
				down_vote_count = 1

			sql = "UPDATE public.\"Polls\" SET p_up_votes="+str(up_vote_count+1)+",p_down_votes="+str(down_vote_count-1)+" WHERE p_name='"+str(var2)+"'"

			cur.execute(sql)

			conn.commit()
			cur.close()
			conn.close()

			return "1"

		else :
			return "0"



@app.route('/down_vote/<p_user>/<p_name>')
def up_vote(p_user,p_name):
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor()

	var1 = p_user
	var2 = p_name

	sql = "SELECT EXISTS(SELECT p_up_vote FROM public.\"Votes\" WHERE p_user='"+str(var1)+"' AND p_name='"+str(var2)+"')"

	cur.execute(sql)

	res = cur.fetchone()

	if(res == "false"):
		sql = "INSERT INTO public.\"Votes\" (p_name,p_user,p_up_vote,p_down_vote,v_date,v_time) VALUES ('"+str(var2)+"','"+str(var1)+"',0,1,'"+v_date+"','"+v_time+"')"
		
		cur.execute(sql)

		conn.commit()



		sql = "SELECT p_up_votes,p_down_votes FROM public.\"Polls\" WHERE p_name='"+str(var2)+"'"

		cur.execute(sql)

		res = cur.fetchall()

		up_vote_count = res[0][0]
		down_vote_count = res[0][1]

		if up_vote_count == 0:
			up_vote_count = 1

		sql = "UPDATE public.\"Polls\" SET p_up_votes="+str(up_vote_count-1)+",p_down_votes="+str(down_vote_count+1)+" WHERE p_name='"+str(var2)+"'"

		cur.execute(sql)

		conn.commit()
		cur.close()
		conn.close()

		return "1"

		

	else:

		sql = "SELECT p_down_vote FROM public.\"Votes\" WHERE p_user='"+str(var1)+"'AND p_name='"+str(var2)+"'"

		cur.execute(sql)

		res = cur.fetchall()

		length = len(res)

		#print length

		if length == 0 :
			res = 0 
		else :
			res = res[length-1][0]

		print str(res)

		if (str(res) == "None")|(str(res) == "0") :

			os.environ['TZ'] = 'Asia/Calcutta'
			time.tzset()

			v_date = str(time.strftime("%d-%m-%Y"))
			v_time = str(time.strftime("%H:%M:%S"))

			sql = "INSERT INTO public.\"Votes\" (p_name,p_user,p_up_vote,p_down_vote,v_date,v_time) VALUES ('"+str(var2)+"','"+str(var1)+"',0,1,'"+v_date+"','"+v_time+"')"

			cur.execute(sql)

			conn.commit()

			sql = "SELECT p_up_votes,p_down_votes FROM public.\"Polls\" WHERE p_name='"+str(var2)+"'"

			cur.execute(sql)

			res = cur.fetchall()

			up_vote_count = res[0][0]
			down_vote_count = res[0][1]

			if up_vote_count == 0:
				up_vote_count = 1

			sql = "UPDATE public.\"Polls\" SET p_up_votes="+str(up_vote_count-1)+",p_down_votes="+str(down_vote_count+1)+" WHERE p_name='"+str(var2)+"'"

			cur.execute(sql)

			conn.commit()
			cur.close()
			conn.close()

			return "1"

		else :
			return "0"



@app.route('/all_polls')
def all_polls():
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor(cursor_factory=RealDictCursor)

	sql = "SELECT * FROM public.\"Polls\" WHERE p_id='abc1_2' AND p_id='sonu_1'"

	cur.execute(sql)

	rows = cur.fetchall()

	 
	return json.dumps(rows, indent=10)

@app.route('/test')
def test():
	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)

	cur = conn.cursor(cursor_factory=RealDictCursor)
	#cur = conn.cursor()

	sql = "SELECT * FROM public.\"Polls\" WHERE p_id='abc1_2'"

	cur.execute(sql)

	rows = cur.fetchall()

	 
	return json.dumps(rows, indent=10)

@app.route('/login_new/<uname>/<pwd>')
def login_new(uname,pwd):

	conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
	)
	cur = conn.cursor()

	var1 = uname
	var2 = pwd

	#return ("Username : "+uname);

	sql = "SELECT pwd FROM public.\"auth_new\" WHERE uname='"+str(var1)+"'"

	cur.execute(sql)

	res = cur.fetchone()
	res = str(res[0])

	if pwd == res :
		return "1"
	else :
		return "0"