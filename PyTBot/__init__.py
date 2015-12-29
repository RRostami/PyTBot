import sqlite3
import requests
import json

BASE_ADDRES='https://api.telegram.org/bot'
DB_NAME="teleg.db"

def init_lib():
	con=sqlite3.connect(DB_NAME)
	curs=con.cursor()
	curs.execute("CREATE TABLE IF NOT EXISTS bots (bot_token CHAR(55) PRIMARY KEY NOT NULL, upid CHAR(12) )")
	con.commit()
	con.close()
init_lib()


class bot:
	def __init__(self,token,name='my_bot'):
		self._token=token
		self._update_id=0
		self.name=name
		self._db_insert_me()
	######################## INTERNAL METHODS ##########################
	def _command(self,cmd,para={},method='get',time_out=20):
		address=BASE_ADDRES+self._token+"/"+cmd
		
		if(method=='get'):
			
			try:
				req=requests.get(address,params=para,timeout=time_out)
			except requests.exceptions.Timeout:
				return None
			except:
				return None
				
		elif(method=='post'):
			try:
				req=requests.post(address,data=para,timeout=time_out)
			except requests.exceptions.Timeout:
				return None
			except:
				return None
		else:
			raise Exception("{} is not a valid method".format(method))
				
				
		if(req.status_code==200):
			return req.text
		elif(req.status_code==404):
			raise Exception("No such Command")
		else:
			raise Exception("HTTP ERROR "+str(req.status_code) +"\n" + req.text)
	
	def _command_upload(self,cmd,file_add,para=None,time_out=75):
		address=BASE_ADDRES+self._token+"/"+cmd
		try:
			req=requests.post(address,data=para,timeout=time_out,files={'document': open(file_add, 'rb')})
		except requests.exceptions.Timeout:
			return None
		except:
			return None
		
		if(req.status_code==200):
			return req.text
		elif(req.status_code==404):
			raise Exception("No such Command")
		else:
			raise Exception("HTTP ERROR "+str(req.status_code))
			
			
	def _db_set_update_id(self,upid):
		if(upid>self._update_id):
			con=sqlite3.connect(DB_NAME)
			curs=con.cursor()
			curs.execute("UPDATE bots SET upid=? WHERE bot_token=?",(upid,self._token))
			con.commit()
			con.close()
			
	def _db_get_update_id(self):
		con=sqlite3.connect(DB_NAME)
		curs=con.cursor()
		curs.execute("SELECT * FROM bots WHERE bot_token=?",(self._token,))
		row=curs.fetchone()
		self._update_id=int(row[1])
		con.close()
	
	def _db_insert_me(self):
		con=sqlite3.connect(DB_NAME)
		curs=con.cursor()
		curs.execute("INSERT OR IGNORE INTO bots VALUES (?,?)", (self._token,1))
		con.commit()
		con.close()
		
	######################### API METHODS ######################
	def getMe(self):
		''' returns User Object '''
		response_str = self._command('getMe')
		if(not response_str):
			return []
		response = json.loads(response_str)	
		return response
	
	def sendMessage(self,chat_id,text,parse_mode=None,disable_web=None,reply_msg_id=None,markup=None):
		payload={'chat_id' : chat_id, 'text' : text, 'parse_mode': parse_mode , 'disable_web_page_preview' : disable_web , 'reply_to_message_id' : reply_msg_id}
		
		if(markup!=None):
			payload['reply_markup']=json.dumps(markup)
			
		response_str = self._command('sendMessage',payload,method='post')
		if(not response_str):
			return False
		response = json.loads(response_str)
		if(not response['ok']):
			return False
		return message(response['result'])
	


	def getUpdates(self,limit=20):
		
		if(self._update_id==0):
			self._db_get_update_id()
		offset=self._update_id+1
		response_str = self._command('getUpdates',{'limit':limit,'offset':offset})
		
		if(not response_str):
			return []
		response = json.loads(response_str)
		if(not response['ok']):
			return []
		updates=[{'upid':update.get('update_id') , 'message': message(update.get('message'))}   for update in response['result'] ]
		return updates
		
	def getUpdates_raw(self,limit=20):
		
		if(self._update_id==0):
			self._db_get_update_id()
		offset=self._update_id+1
		response_str = self._command('getUpdates',{'limit':limit,'offset':offset})
		
		if(not response_str):
			return []
		response = json.loads(response_str)
		if(not response['ok']):
			return []
		updates=response['result']
		return updates

	def getUpdates_iter(self,limit=20):
		
		if(self._update_id==0):
			self._db_get_update_id()
		offset=self._update_id+1
		response_str = self._command('getUpdates',{'limit':limit,'offset':offset})
		
		if(not response_str):
			return None
		response = json.loads(response_str)
		if(not response['ok']):
			return None
		updates=response['result'] 
		for update in updates:
			upid=update.get('update_id')
			msg=update.get('message')
			set_upid(upid)
			if(msg):
				yield message(msg)
			else:
				return None
		
		
	def set_upid(self,upid=None):
		if(upid!=None):
			self._db_set_update_id(upid)
		else:
			self._db_set_update_id(self._update_id+1)

		
		
		
		
######################## MISC API DEFINITIONS   ######################################


		
class replyMarkup:
	def __init__(self,keys=None,one_time=None,resize=None,selective=None):
		self.keyboard=None
		self.resize_keyboard=resize
		self.one_time_keyboard=one_time
		self.selective=selective
		if(keys):
			self.set_keys(keys)
		
		
	def get_dict(self):
		if(self.keyboard==None):
			return None
		ans={'keyboard': self.keyboard}
		if(self.resize_keyboard ==True):
			ans['resize_keyboard']=True
		if(self.one_time_keyboard ==True):
			ans['one_time_keyboard']=True
		if(self.selective ==True):
			ans['selective']=True
			
		return ans
		
	def set_keys(self,keys,force_row=None):
		lin=len(keys)
		if(lin==0 or force_row==0):
			self.keyboard=None
			return
			
		if(force_row==None):
			if(lin<=3):
				row=1
			elif(lin<=8):
				row=2
			else:
				row=3
		else:
			row=force_row
		
		self.keyboard=[]
		for i in range(row):
			self.keyboard.append( [] )
		k=0
		if(lin%row==0):
			step=lin//row
		else:
			step=lin//row+1
		while(k<lin):
			self.keyboard[k//step].append(keys[k])
			k+=1
		return True



###################    TELEGRAM TYPE DEFINITIONS   ##########################

class user:
	def __init__(self,para):
		self.id = para.get('id')
		self.first_name = para.get('first_name')
		self.last_name = para.get('last_name')
		self.username = para.get('username')
		
class chat:
	def __init__(self,para):
		self.id = para.get('id')
		self.type = para.get('type')
		self.title = para.get('title')
		self.username = para.get('username')
		self.first_name = para.get('first_name')
		self.last_name = para.get('last_name')
		
class message:
	def __init__(self,para):
		if(not para):
			return None
			
		self.id = para.get('message_id')
		self.date = int(para.get('date'))
		self.chat=chat(para.get('chat'))
		self.caption=para.get('caption')
		self.type=None	
		
		# Sender Handling
		self.sender=None
		tmp_sender=para.get('from')
		if(tmp_sender):
			self.sender=user(tmp_sender)
		
		# Handle TEXT MSG
		self.text=para.get('text')
		if 'text' in para:	
			self.type='text'
			self.content=self.__text2byte()
		# Handle AUDIO MSG
		if 'audio' in para:
			self.type='audio'
			self.content=t_audio(para.get('audio'))
		# Handle FILE MSG
		if 'document' in para:
			self.type='file'
			self.content=t_file(para.get('documet'))
		# Handle PHOTO MSG	
		if 'photo' in para:
			self.type='photo'
			self.content=[t_photo(w) for w in para.get('photo')]
		# Handle STICKER MSG
		if 'sticker' in para:
			self.type='sticker'
			self.content=t_sticker(para.get('sticker'))
		# Handle VIDEO MSG
		if 'video' in para:
			self.type='video'
			self.content=t_video(para.get('video'))	
		# Handle VOICE MSG
		if 'voice' in para:
			self.type='voice'
			self.content=t_voice(para.get('voice'))	
		# Handle CONTACT MSG
		if 'contact' in para:
			self.type='contact'
			self.content=t_contact(para.get('contact'))
		# Handle LOCATION MSG
		if 'location' in para:
			self.type='location'
			self.content=t_location(para.get('location'))
		# Handle SERVICE MSG
		# TODO
		
	def __text2byte(self):
		if(self.text):
			return str(self.text).encode('utf8')
		else:
			return None
			
class t_photo:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.width=para.get('width')
		self.height=para.get('height')
		self.file_size=para.get('file_size')
		
class t_audio:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.duration=para.get('duration')
		self.performer = para.get('performer')
		self.title=para.get('title')
		self.mime_type=para.get('mime_type')
		self.file_size=para.get('file_size')
	
class t_file:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.name=para.get('file_name')
		self.mime_type=para.get('mime_type')
		self.file_size=para.get('file_size')
		
		self.thumb=None
		tmp_thumb=para.get('thumb')
		if(tmp_thumb):
			self.thumb=t_photo(tmp_thumb)
		
class t_sticker:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.width=para.get('width')
		self.height=para.get('height')
		self.file_size=para.get('file_size')
		
		self.thumb=None
		tmp_thumb=para.get('thumb')
		if(tmp_thumb):
			self.thumb=t_photo(tmp_thumb)
			
class t_video:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.width=para.get('width')
		self.height=para.get('height')
		self.duration=para.get('duration')
		self.mime_type=para.get('mime_type')
		self.file_size=para.get('file_size')
		
		self.thumb=None
		tmp_thumb=para.get('thumb')
		if(tmp_thumb):
			self.thumb=t_photo(tmp_thumb)
			
			
class t_voice:
	def __init__(self,para):
		self.id=para.get('file_id')
		self.duration=para.get('duration')
		self.mime_type=para.get('mime_type')
		self.file_size=para.get('file_size')
		
class t_contact:
	def __init__(self,para):
		self.phone_number=para.get('phone_number')
		self.first_name=para.get('first_name')
		self.last_name = para.get('last_name')
		self.user_id=para.get('user_id')

class t_location:
	def __init__(self,para):
		self.longitude=para.get('longitude')
		self.latitude=para.get('latitude')
		
