# -? "JAMMY"
def start ():
	return "l1ll111lllll111l111l",{}
def llll1lll111l1llll11l (*O0O00O0OO00OOOOO0 ):
	return tuple ([int (O0OO0O00O0OOOOO00 )for O0OO0O00O0OOOOO00 in O0O00O0OO00OOOOO0 ])
def l1l11l111ll1l1lll1ll (O0OOOO000O0O0000O ,O00OOO000OO000OOO ):
	return chr (int (O0OOOO000O0O0000O /3 )%256 )+chr (int (O00OOO000OO000OOO /3 )%256 )
def l11lll111ll111lllll1 (O00OOO00OO0000O0O ):
	return int (ord (O00OOO00OO0000O0O [0 ])*3 ),int (ord (O00OOO00OO0000O0O [1 ])*3 )
def l1l1ll1llll1111llll1 (OO00000O00O0O0O0O ,O00O0OO00OOO000O0 ):
	return chr (int ((OO00000O00O0O0O0O +50 )/100 *255 ))+chr (int ((O00O0OO00OOO000O0 +50 )/100 *255 ))
def lllllllll111ll1ll1l1 (O000O000OO0O000OO ):
	return ord (O000O000OO0O000OO [0 ])/255 *100 -50 ,ord (O000O000OO0O000OO [1 ])/255 *100 -50 
def l1l1ll111l1ll11l1ll1 (O0OO00O0O00000OO0 ):
	return chr (int (O0OO00O0O00000OO0 )//256 )+chr (int (O0OO00O0O00000OO0 )%256 )
def l1l11111l11l11lll111 (O000000O00000OOO0 ):
	return ord (O000000O00000OOO0 [0 ])*256 +ord (O000000O00000OOO0 [1 ])
def l1l11lllll111l1lll1l (O0O000OO00O00O0O0 ,O00O000O0OO0OOOO0 ,O0000O0OOO00O00OO ,OOOOO00O00OOO00O0 ,O00OOOO0O0O00O00O ):
	O0OO0O0OO0OO0O0O0 =O0000O0OOO00O00OO -O0O000OO00O00O0O0 
	O0O0O00OO00OO00OO =OOOOO00O00OOO00O0 -O00O000O0OO0OOOO0 
	OO000000000O0OO0O =sqrt (O0OO0O0OO0OO0O0O0 **2 +O0O0O00OO00OO00OO **2 )
	OO0O00OO0OOO00OO0 =degrees (atan2 (O0O0O00OO00OO00OO ,O0OO0O0OO0OO0O0O0 ))
	O0000O0OOO00O00OO =O0O000OO00O00O0O0 +cos (radians (OO0O00OO0OOO00OO0 ))*OO000000000O0OO0O 
	OOOOO00O00OOO00O0 =O00O000O0OO0OOOO0 +sin (radians (OO0O00OO0OOO00OO0 ))*OO000000000O0OO0O 
	O0OO0O0OO0OO0O0O0 =O0000O0OOO00O00OO -O0O000OO00O00O0O0 
	O0O0O00OO00OO00OO =OOOOO00O00OOO00O0 -O00O000O0OO0OOOO0 
	OO000000000O0OO0O =sqrt (O0OO0O0OO0OO0O0O0 **2 +O0O0O00OO00OO00OO **2 )
	OO0O00OO0OOO00OO0 =degrees (atan2 (O0O0O00OO00OO00OO ,O0OO0O0OO0OO0O0O0 ))
	if OO000000000O0OO0O >0 :
		OO0OO0OO000OOOO00 =O0OO0O0OO0OO0O0O0 /OO000000000O0OO0O *(O00OOOO0O0O00O00O *5 )
		OO0O0OO000O000OOO =O0O0O00OO00OO00OO /OO000000000O0OO0O *(O00OOOO0O0O00O00O *5 )
	else :
		OO0OO0OO000OOOO00 =O0OO0O0OO0OO0O0O0 
		OO0O0OO000O000OOO =O0O0O00OO00OO00OO 
	OOOO000O0O00OO000 ,O0O0OO00OO0O0000O =get_velocity_tuple ()
	O00OOO00O0000O0O0 =(OO0OO0OO000OOOO00 -OOOO000O0O00OO000 )*5 
	OOOO0OOOO0O0O0000 =(OO0O0OO000O000OOO -O0O0OO00OO0O0000O )*5 
	O0O0O000OOO0O0O00 =sqrt (O00OOO00O0000O0O0 **2 +OOOO0OOOO0O0O0000 **2 )
	if O0O0O000OOO0O0O00 ==0 :
		return 0 ,0 
	else :
		return O00OOO00O0000O0O0 /O0O0O000OOO0O0O00 ,OOOO0OOOO0O0O0000 /O0O0O000OOO0O0O00 
def ll1lll1l11l111ll1l1l (OO0O00OO0OOOO0000 ):
	OOOOO0O000OO00OOO =[OO0O00OO0OOOO0000 ]
	for O000O0OO00O0O0000 in range (1 ,180 ):
		OOOOO0O000OO00OOO .append ((OO0O00OO0OOOO0000 +O000O0OO00O0O0000 )%360 )
		OOOOO0O000OO00OOO .append ((OO0O00OO0OOOO0000 -O000O0OO00O0O0000 )%360 )
	OOOOO0O000OO00OOO .append ((OO0O00OO0OOOO0000 +180 )%360 )
	return OOOOO0O000OO00OOO 
def l1l1l1l111l111l1l1l1 (O0OOOOO0O0OO0OOO0 ,O0000OOO0O0OOO0OO ):
	OOO0OO0O0000O0O00 =0 
	OO0000O00O0O000OO =0 
	OO0000O000OO0OOO0 =False 
	OOO000O00OOOOO0OO =((O0OOOOO0O0OO0OOO0 -O0000OOO0O0OOO0OO )+360 )%360 
	if OOO000O00OOOOO0OO <1 or OOO000O00OOOOO0OO >359 :
		OO0000O000OO0OOO0 =True 
	elif OOO000O00OOOOO0OO >180 :
		OO0000O00O0O000OO =1 
	else :
		OOO0OO0O0000O0O00 =1 
	return OOO0OO0O0000O0O00 ,OO0000O00O0O000OO ,OO0000O000OO0OOO0 
def ll11l1l1l1l1ll1l111l (OOOO0000OO0OOOO0O ,OOO0O0O000O0O0000 ,OO0O000OO0OOOOO00 ,O0OO0OOO0O0O00OO0 ):
	OO00O0O000OOOO0O0 =degrees (atan2 ((O0OO0OOO0O0O00OO0 -OOO0O0O000O0O0000 ),(OO0O000OO0OOOOO00 -OOOO0000OO0OOOO0O )))%360 
	OO0O0OO000OOO0O0O =[]
	O0OO0O00O000OO0OO =0 
	O0OOO0O000OO00OO0 =False 
	OO0O00O0OO00O0O0O =None 
	O0OO0000OO0O0OOO0 =None 
	O0000O0OOOO0OOO0O =(None ,None ,None )
	OO0OO0OOOOOO0O0O0 =ll1lll1l11l111ll1l1l (OO00O0O000OOOO0O0 )
	for OOO0OOO000O00000O in range (len (OO0OO0OOOOOO0O0O0 )):
			O0OO0OOO0OOO0OOOO =OO0OO0OOOOOO0O0O0 [OOO0OOO000O00000O ]
			(O00OO000O0O00O0O0 ,OO00000OO000OO0OO ,O0000O0OOOO0OOO0O )=get_the_radar_data (O0OO0OOO0OOO0OOOO )
			if O00OO000O0O00O0O0 =="player":
				while O00OO000O0O00O0O0 =="player":
					O0OO0O00O000OO0OO +=OO00000OO000OO0OO 
					OO0O0OO000OOO0O0O .append (O0OO0OOO0OOO0OOOO )
					OOO0OOO000O00000O =((OOO0OOO000O00000O +2 )%len (OO0OO0OOOOOO0O0O0 ))
					O0OO0OOO0OOO0OOOO =OO0OO0OOOOOO0O0O0 [OOO0OOO000O00000O ]
					(O00OO000O0O00O0O0 ,OO00000OO000OO0OO ,_O00000O000OO0OO0O )=get_the_radar_data (O0OO0OOO0OOO0OOOO )
				O0OOO0O000OO00OO0 =True 
				O0OO0000OO0O0OOO0 =O0OO0O00O000OO0OO /len (OO0O0OO000OOO0O0O )
				OO0O00O0OO00O0O0O =OO0O0OO000OOO0O0O [len (OO0O0OO000OOO0O0O )//2 ]
				break 
	return O0OOO0O000OO00OO0 ,OO0O00O0OO00O0O0O ,O0OO0000OO0O0OOO0 ,O0000O0OOOO0OOO0O 
def l1ll111lllll111l111l ():
	(OOO00O0O0O0O00000 ,O0OOOOO0OO0000O00 )=get_position_tuple ()
	O00000OOOO0O0O0OO =radians (get_throwing_angle ()+180 )
	OO0000000OOOOOO00 =int (OOO00O0O0O0O00000 +cos (O00000OOOO0O0O0OO )*525 )
	OO0O000O0O0OOO00O =int (O0OOOOO0OO0000O00 +sin (O00000OOOO0O0O0OO )*525 )
	return "llll1ll1l11l1l1l1l11",{"SAVE_B":l1l1ll111l1ll11l1ll1 (OO0000000OOOOOO00 ),"SAVE_C":l1l1ll111l1ll11l1ll1 (OO0O000O0O0OOO00O ),"WEAPON":True }
def llll1ll1l11l1l1l1l11 ():
	(OO00000OOO0OO0000 ,OOOO000OO0OOO0000 )=get_position_tuple ()
	OO00OOO00OOO0OOO0 =get_throwing_angle ()
	O0OO00O0OO00O0O00 =(OO00OOO00OOO0OOO0 -235 )%360 
	OOO0000OO00OO0000 =(OO00OOO00OOO0OOO0 -125 )%360 
	if ((O0OO00O0OO00O0O00 -OOO0000OO00OO0000 )+360 )%360 >180 :
		O0O00OO0OO0000000 =-1 
	else :
		O0O00OO0OO0000000 =+1 
	O0OOO0OOOO000OOOO =OOO0000OO00OO0000 
	O000O0000OO00OOO0 =[]
	while not (O0OOO0OOOO000OOOO ==O0OO00O0OO00O0O00 ):
		(O00O0O000OO0OOOO0 ,O000OO0O0OOOOOO00 ,_O0OOOOO0OOO0O000O )=get_the_radar_data (O0OOO0OOOO000OOOO )
		if O00O0O000OO0OOOO0 =="column":
			O000O0000OO00OOO0 .append (O000OO0O0OOOOOO00 )
		else :
			O000O0000OO00OOO0 .append (-1 )
		if O0OOO0OOOO000OOOO >=360 :
			O0OOO0OOOO000OOOO -=360 
		elif O0OOO0OOOO000OOOO <0 :
			O0OOO0OOOO000OOOO +=360 
		O0OOO0OOOO000OOOO +=O0O00OO0OO0000000 
	O00OOOOO0OO0O0OO0 =0 
	OOO00OO00OOO00OOO =[]
	OO000OOOO0O0000O0 =0 
	O00OO00OO0O0OO0OO =[]
	O0OOO0OOOO000OOOO =OOO0000OO00OO0000 
	for OO00O0O0OOO0OO000 in range (len (O000O0000OO00OOO0 )):
		if O000O0000OO00OOO0 [OO00O0O0OOO0OO000 ]>0 :
			if O000O0000OO00OOO0 [OO00O0O0OOO0OO000 ]-O000O0000OO00OOO0 [OO00O0O0OOO0OO000 -1 ]<5 or O00OOOOO0OO0O0OO0 ==0 :
				OOO00OO00OOO00OOO .append (OO00O0O0OOO0OO000 )
				O00OOOOO0OO0O0OO0 +=1 
			else :
				if O00OOOOO0OO0O0OO0 >OO000OOOO0O0000O0 :
					O00OO00OO0O0OO0OO =OOO00OO00OOO00OOO [:]
					OO000OOOO0O0000O0 =O00OOOOO0OO0O0OO0 
				O00OOOOO0OO0O0OO0 =0 
				OOO00OO00OOO00OOO =[]
		else :
			if O00OOOOO0OO0O0OO0 >OO000OOOO0O0000O0 :
				O00OO00OO0O0OO0OO =OOO00OO00OOO00OOO [:]
				OO000OOOO0O0000O0 =O00OOOOO0OO0O0OO0 
			O00OOOOO0OO0O0OO0 =0 
			OOO00OO00OOO00OOO =[]
		O0OOO0OOOO000OOOO +=O0O00OO0OO0000000 
	O0O00OO0OOOOOOO0O =OOO0000OO00OO0000 +O0O00OO0OO0000000 *O00OO00OO0O0OO0OO [int (OO000OOOO0O0000O0 //2 )]
	(_O0OOOOO0OOO0O000O ,O000OO0O0OOOOOO00 ,_O0OOOOO0OOO0O000O )=get_the_radar_data (O0O00OO0OOOOOOO0O )
	OO0O0OO0O0OO00O00 =OO00000OOO0OO0000 +cos (radians (O0O00OO0OOOOOOO0O ))*O000OO0O0OOOOOO00 
	O00O000OO0OOOOOO0 =OOOO000OO0OOO0000 +sin (radians (O0O00OO0OOOOOOO0O ))*O000OO0O0OOOOOO00 
	return "l1ll111ll111ll1l11ll",{"SAVE_X":l1l1ll111l1ll11l1ll1 (OO0O0OO0O0OO00O00 ),"SAVE_Y":l1l1ll111l1ll11l1ll1 (O00O000OO0OOOOOO0 ),"WEAPON":True }
def l1ll111ll111ll1l11ll ():
	(O0OOO00O0OOO0000O ,OO0OOOO00OO00OO00 )=get_position_tuple ()
	(OO0O000O00O000OOO ,OOO0000000OO0O000 )=get_velocity_tuple ()
	OOO0O0O0000OOO00O =degrees (atan2 (OO0O000O00O000OOO ,OOO0000000OO0O000 ))
	(OO0O000OO0OO0OO00 ,OO00O000OOOOO0O00 ,_O0O00OOO000O00OO0 )=get_the_radar_data (OOO0O0O0000OOO00O )
	if (OO0O000OO0OO0OO00 =="column"and OO00O000OOOOO0O00 <100 ):
		return "lllll1l1l1l1111lllll",{}
	O000OOO00O000OO0O =get_my_stored_data ()
	OO00O0OO0000O0O0O =l1l11111l11l11lll111 (O000OOO00O000OO0O [1 ])
	O0000O00OO00OOO0O =l1l11111l11l11lll111 (O000OOO00O000OO0O [2 ])
	OO0000000OO00O00O =l1l11111l11l11lll111 (O000OOO00O000OO0O [6 ])
	OOOO0OOO00O00O0O0 =l1l11111l11l11lll111 (O000OOO00O000OO0O [7 ])
	O000OO0OO00O0O0OO =get_throwing_angle ()
	O00OOO000O0O0OO00 =degrees (atan2 (O0000O00OO00OOO0O -OO0OOOO00OO00OO00 ,OO00O0OO0000O0O0O -O0OOO00O0OOO0000O ))
	OO00OO00OO000O000 ,OOO0O00OO0OOO0OO0 ,OO00OOO0O0000000O =l1l1l1l111l111l1l1l1 (O00OOO000O0O0OO00 ,O000OO0OO00O0O0OO )
	O0O000O0000OO000O ,OO0O0OOO0O0O000OO =l1l11lllll111l1lll1l (O0OOO00O0OOO0000O ,OO0OOOO00OO00OO00 ,OO0000000OO00O00O ,OOOO0OOO00O00O0O0 ,1 )
	OO0O0000OO00OOO00 =sqrt ((OO0000000OO00O00O -O0OOO00O0OOO0000O )**2 +(OOOO0OOO00O00O0O0 -OO0OOOO00OO00OO00 )**2 )
	OOOOOO00O0OOOOOOO =[]
	OOOOOO00O0OOOOOOO .append (llll1lll111l1llll11l (OO0000000OO00O00O ,OOOO0OOO00O00O0O0 ,50 ))
	if OO0O0000OO00OOO00 <100 :
		OO0000O0O00O0OOOO =O0OOO00O0OOO0000O -OO0000000OO00O00O 
		O0OOO000O0OOOOOOO =OO0OOOO00OO00OO00 -OOOO0OOO00O00O0O0 
		O0O0OO0O00OO0O0O0 =int (round (degrees (atan2 (O0OOO000O0OOOOOOO ,OO0000O0O00O0OOOO )),-1 ))
		return "l1111ll1l1ll11l11l11",{"SAVE_A":l1l1ll111l1ll11l1ll1 (O0O0OO0O00OO0O0O0 %360 ),"SAVE_X":O000OOO00O000OO0O [6 ],"SAVE_Y":O000OOO00O000OO0O [7 ],"ACLT_X":O0O000O0000OO000O ,"ACLT_Y":OO0O0OOO0O0O000OO ,"WEAPON":True }
	else :
		return "l1ll111ll111ll1l11ll",{"SAVE_X":O000OOO00O000OO0O [6 ],"SAVE_Y":O000OOO00O000OO0O [7 ],"ACLT_X":O0O000O0000OO000O ,"ACLT_Y":OO0O0OOO0O0O000OO ,"WEAPON":True }
def l1111ll1l1ll11l11l11 ():
	(OOOOO00O00O0OOOO0 ,OOOO0OOO000OOO0O0 )=get_position_tuple ()
	(OO0000O00O0000O0O ,O00OO0000O0O00000 )=get_velocity_tuple ()
	O0OO00OO00OOO0O00 =degrees (atan2 (OO0000O00O0000O0O ,O00OO0000O0O00000 ))
	(O00OOO0OO0O0OOO0O ,OOOOOO0O0OOO0O000 ,_O0OO0O0000O000OOO )=get_the_radar_data (O0OO00OO00OOO0O00 )
	if (O00OOO0OO0O0OOO0O =="column"and OOOOOO0O0OOO0O000 <100 ):
		return "lllll1l1l1l1111lllll",{}
	OO00O0O00OOO0OO0O =get_my_stored_data ()
	OOOOOO0OO0OOOO00O =l1l11111l11l11lll111 (OO00O0O00OOO0OO0O [0 ])
	O0OO000OOOO0OO0O0 =l1l11111l11l11lll111 (OO00O0O00OOO0OO0O [1 ])
	O00000OO00OO00000 =l1l11111l11l11lll111 (OO00O0O00OOO0OO0O [2 ])
	OO00O00O0O0O0O00O =l1l11111l11l11lll111 (OO00O0O00OOO0OO0O [6 ])
	O000O0OOOOO0O00O0 =l1l11111l11l11lll111 (OO00O0O00OOO0OO0O [7 ])
	O0O00000OO0000OO0 =get_throwing_angle ()
	O0OO0O00000O00O0O =degrees (atan2 (O00000OO00OO00000 -OOOO0OOO000OOO0O0 ,O0OO000OOOO0OO0O0 -OOOOO00O00O0OOOO0 ))
	OO0OOO00OOOO00O0O ,OOO0000OOO000OO0O ,O000O00OOOOOO00OO =l1l1l1l111l111l1l1l1 (O0OO0O00000O00O0O ,O0O00000OO0000OO0 )
	if sqrt ((OO00O00O0O0O0O00O -OOOOO00O00O0OOOO0 )**2 +(O000O0OOOOO0O00O0 -OOOO0OOO000OOO0O0 )**2 )>150 :
		return "lllll1l1l1l1111lllll",{}
	O00OOOOO0OOOO00O0 =O0OO000OOOO0OO0O0 
	OO0OO000OOO00000O =O00000OO00OO00000 
	O00OOOO0000O00OOO =OO00O00O0O0O0O00O +cos (radians (OOOOOO0OO0OOOO00O ))*80 
	O0O0OOOO0O0000O00 =O000O0OOOOO0O00O0 +sin (radians (OOOOOO0OO0OOOO00O ))*80 
	OOOO00OOOO0O000OO =[]
	if sqrt ((O00OOOO0000O00OOO -OOOOO00O00O0OOOO0 )**2 +(O0O0OOOO0O0000O00 -OOOO0OOO000OOO0O0 )**2 )<30 :
		OO0000O00O0000O0O ,O00OO0000O0O00000 =get_velocity_tuple ()
		O00000OOO00OO000O =sqrt (OO0000O00O0000O0O **2 +O00OO0000O0O00000 **2 )
		if O00000OOO00OO000O >0 :
			OO00OO00O0OOOO0OO =-1 *OO0000O00O0000O0O /O00000OOO00OO000O 
			OO0O00000OO000O0O =-1 *O00OO0000O0O00000 /O00000OOO00OO000O 
		else :
			OO00OO00O0OOOO0OO =0 
			OO0O00000OO000O0O =0 
		O0000000O00OO0O0O ,O00OO0OO00000OOO0 ,O0O0O0O0OO00000OO ,OOO00O0OO0O0OO00O =ll11l1l1l1l1ll1l111l (OOOOO00O00O0OOOO0 ,OOOO0OOO000OOO0O0 ,O0OO000OOOO0OO0O0 ,O00000OO00OO00000 )
		if O0000000O00OO0O0O :
			O00OOOOO0OOOO00O0 =OOOOO00O00O0OOOO0 +cos (radians (O00OO0OO00000OOO0 ))*O0O0O0O0OO00000OO 
			OO0OO000OOO00000O =OOOO0OOO000OOO0O0 +sin (radians (O00OO0OO00000OOO0 ))*O0O0O0O0OO00000OO 
			O0O00000OO0000OO0 =get_throwing_angle ()
			O0OO0O00000O00O0O =degrees (atan2 (OO0OO000OOO00000O -OOOO0OOO000OOO0O0 ,O00OOOOO0OOOO00O0 -OOOOO00O00O0OOOO0 ))
			OO0OOO00OOOO00O0O ,OOO0000OOO000OO0O ,O000O00OOOOOO00OO =l1l1l1l111l111l1l1l1 (O0OO0O00000O00O0O ,O0O00000OO0000OO0 )
			O0000OOO000O0O000 =OOOOO00O00O0OOOO0 -OO00O00O0O0O0O00O 
			O0O0OOO0OO0000OOO =OOOO0OOO000OOO0O0 -O000O0OOOOO0O00O0 
			O0O000OO0OOO00OO0 =OO00O00O0O0O0O00O +cos (radians (OOOOOO0OO0OOOO00O +45 ))*70 
			OOOO0O00O000OOO0O =O000O0OOOOO0O00O0 +sin (radians (OOOOOO0OO0OOOO00O +45 ))*70 
			O0000OO0OOO000000 =OO00O00O0O0O0O00O +cos (radians (OOOOOO0OO0OOOO00O -45 ))*70 
			OOOO00OO0OO00O000 =O000O0OOOOO0O00O0 +sin (radians (OOOOOO0OO0OOOO00O -45 ))*70 
			OOOOOO00O00O0OOO0 =sqrt ((O0O000OO0OOO00OO0 -O00OOOOO0OOOO00O0 )**2 +(OOOO0O00O000OOO0O -OO0OO000OOO00000O )**2 )
			O0O00O0OO00O00000 =sqrt ((O0000OO0OOO000000 -O00OOOOO0OOOO00O0 )**2 +(OOOO00OO0OO00O000 -OO0OO000OOO00000O )**2 )
			OOOO00OOOO0O000OO .append (llll1lll111l1llll11l (OOOOO00O00O0OOOO0 ,OOOO0OOO000OOO0O0 ,O0O000OO0OOO00OO0 ,OOOO0O00O000OOO0O ))
			OOOO00OOOO0O000OO .append (llll1lll111l1llll11l (OOOOO00O00O0OOOO0 ,OOOO0OOO000OOO0O0 ,O0000OO0OOO000000 ,OOOO00OO0OO00O000 ))
			if OOOOOO00O00O0OOO0 >O0O00O0OO00O00000 :
				OOOOOO0OO0OOOO00O +=45 
			else :
				OOOOOO0OO0OOOO00O -=45 
			O00OOOO0000O00OOO =OO00O00O0O0O0O00O +cos (radians (OOOOOO0OO0OOOO00O ))*70 
			O0O0OOOO0O0000O00 =O000O0OOOOO0O00O0 +sin (radians (OOOOOO0OO0OOOO00O ))*70 
		else :
			pass 
	else :
		OO00OO00O0OOOO0OO ,OO0O00000OO000O0O =l1l11lllll111l1lll1l (OOOOO00O00O0OOOO0 ,OOOO0OOO000OOO0O0 ,O00OOOO0000O00OOO ,O0O0OOOO0O0000O00 ,1 )
	OOOO00OOOO0O000OO .append (llll1lll111l1llll11l (O00OOOO0000O00OOO ,O0O0OOOO0O0000O00 ,20 ))
	return "l1111ll1l1ll11l11l11",{"SAVE_A":l1l1ll111l1ll11l1ll1 (OOOOOO0OO0OOOO00O %360 ),"SAVE_B":l1l1ll111l1ll11l1ll1 (O00OOOOO0OOOO00O0 ),"SAVE_C":l1l1ll111l1ll11l1ll1 (OO0OO000OOO00000O ),"SAVE_X":OO00O0O00OOO0OO0O [6 ],"SAVE_Y":OO00O0O00OOO0OO0O [7 ],"ACLT_X":OO00OO00O0OOOO0OO ,"ACLT_Y":OO0O00000OO000O0O ,"ROT_CC":OO0OOO00OOOO00O0O ,"ROT_CW":OOO0000OOO000OO0O ,"WEAPON":not (O000O00OOOOOO00OO and get_if_have_weapon ())}
def lll1lll11lllllll1111 ():
	(OO0OOOOOOO0OOO0O0 ,OOO00O00O0000O000 )=get_position_tuple ()
	O00O000O0OOOOOO0O ,OO0OO0000000OO0O0 =l1l11lllll111l1lll1l (OO0OOOOOOO0OOO0O0 ,OOO00O00O0000O000 ,375 ,375 ,1 )
	if sqrt ((OO0OOOOOOO0OOO0O0 -375 )**2 +(OO0OOOOOOO0OOO0O0 -375 )**2 )<50 :
		return "llll1ll1l11l1l1l1l11",{"WEAPON":True }
	else :
		return "lll1lll11lllllll1111",{"WEAPON":True }
def lllll1l1l1l1111lllll ():
	(O000OO000OO000OOO ,OOOO0O0000OO00O0O )=get_position_tuple ()
	O0OO000OOOOOO0000 =get_throwing_angle ()
	OO0O0000OO0O0O00O =360 
	O000O00O0OO000OOO =0 
	O0OOOO0OO000OO000 =+1 
	OOO0O0000O0O0O00O =O000O00O0OO000OOO 
	OOO0O0OOO0O0OO0O0 =[]
	while not (OOO0O0000O0O0O00O ==OO0O0000OO0O0O00O ):
		(OOO0O00OO0OOO0OOO ,O000OO0O0O0O00OOO ,_OO0000OO000000000 )=get_the_radar_data (OOO0O0000O0O0O00O )
		if OOO0O00OO0OOO0OOO =="column":
			OOO0O0OOO0O0OO0O0 .append (O000OO0O0O0O00OOO )
		else :
			OOO0O0OOO0O0OO0O0 .append (-1 )
		if OOO0O0000O0O0O00O >=360 :
			OOO0O0000O0O0O00O -=360 
		elif OOO0O0000O0O0O00O <0 :
			OOO0O0000O0O0O00O +=360 
		OOO0O0000O0O0O00O +=O0OOOO0OO000OO000 
	O00O00OO00O000O00 =0 
	O0000OO0OO0O0000O =[]
	OOOO00O00OOOOO000 =0 
	O00O0O0OOO0O0OOOO =[]
	OOO0O0000O0O0O00O =O000O00O0OO000OOO 
	for O00O0OOOO0O0OO00O in range (len (OOO0O0OOO0O0OO0O0 )):
		if OOO0O0OOO0O0OO0O0 [O00O0OOOO0O0OO00O ]>0 :
			if OOO0O0OOO0O0OO0O0 [O00O0OOOO0O0OO00O ]-OOO0O0OOO0O0OO0O0 [O00O0OOOO0O0OO00O -1 ]<5 or O00O00OO00O000O00 ==0 :
				O0000OO0OO0O0000O .append (O00O0OOOO0O0OO00O )
				O00O00OO00O000O00 +=1 
			else :
				if O00O00OO00O000O00 >OOOO00O00OOOOO000 :
					O00O0O0OOO0O0OOOO =O0000OO0OO0O0000O [:]
					OOOO00O00OOOOO000 =O00O00OO00O000O00 
				O00O00OO00O000O00 =0 
				O0000OO0OO0O0000O =[]
		else :
			if O00O00OO00O000O00 >OOOO00O00OOOOO000 :
				O00O0O0OOO0O0OOOO =O0000OO0OO0O0000O [:]
				OOOO00O00OOOOO000 =O00O00OO00O000O00 
			O00O00OO00O000O00 =0 
			O0000OO0OO0O0000O =[]
		OOO0O0000O0O0O00O +=O0OOOO0OO000OO000 
	OO00O00O00OO0OOO0 =O000O00O0OO000OOO +O0OOOO0OO000OO000 *O00O0O0OOO0O0OOOO [int (OOOO00O00OOOOO000 //2 )]
	(_OO0000OO000000000 ,O000OO0O0O0O00OOO ,_OO0000OO000000000 )=get_the_radar_data (OO00O00O00OO0OOO0 )
	O0O00O0OOOO000000 =O000OO000OO000OOO +cos (radians (OO00O00O00OO0OOO0 ))*O000OO0O0O0O00OOO 
	OO00O0OOOOOO0OO00 =OOOO0O0000OO00O0O +sin (radians (OO00O00O00OO0OOO0 ))*O000OO0O0O0O00OOO 
	return "l1ll111ll111ll1l11ll",{"SAVE_X":l1l1ll111l1ll11l1ll1 (O0O00O0OOOO000000 ),"SAVE_Y":l1l1ll111l1ll11l1ll1 (OO00O0OOOOOO0OO00 ),"WEAPON":True }