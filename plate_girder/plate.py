#
##Plate Girder Designer
##Author-Yajnavalkya Bandyopadhyay
##B.Tech Project Part 2
##Supervisor - Mr. Somnath Majumder
##email-yajnab@gmail.com
#

print("Plate Girder Designer")
print("Author- Yajnavalkya Bandyopadhyay")
print("email- yajnab@gmail.com")

import numpy as np
from colorama import init, Fore, Style, Back
from PIL import Image, ImageFont, ImageDraw
import math

#Constants
FOS = 1.5 #Factor of Safety
udl = 30 #UDL Superimposed Load in KN
c_load_n=2 #NUmber of Concentrated Loads
c_load = 150 #Concentrated Load at 6m from either ends
c_load_dist = 6 #Distance of loads from either of the ends
span= 20 #Span of the Girder
k=180#Value of d/tw
f_y=250#Value of Fy


class plate_girder:
	init() #Initialize Colorama
	
	w_udl = udl*span#UDL Load on Girder
	F_w_udl = w_udl*FOS	#Factored w_udl
	print("Superimposed Uniformaly Distributed Load on the Girder Span is", w_udl)
	print("Factored Superimposed Uniformaly Distributed Load on the Girder Span is", F_w_udl)
	w_c= c_load #Superimposed Concentrated Load
	F_w_c= FOS*w_c #Superimposed Concentrated Load
	print("Concentrated Load on the Span", w_c)
	print("Factored Concentrated Load on the Span", F_w_c)
	w_self = (w_udl+w_c*c_load_n)/300
	F_w_self = FOS*w_self
	print("Self Load on the Girder Span is", w_self)
	print("Factored Self Load on the Girder Span is", F_w_self)
	w_total_udl = (w_self+udl)*FOS
	print("Total UDL Load on the Girder Span is w_total_udl=", w_total_udl)
	w_total = w_total_udl*span + c_load_n*c_load*FOS
	print("Total Load on the Girder w_total=", w_total)

	#Calculation of Reactions
	#Let two reactions be at the supports. Reaction at the one end be Ra and the other end be Rb
	#Moment on one side(Lets say its B) have the moment as 0. So the reaction will play like
	Ra = (w_total_udl*0.5*(span**2)+F_w_c*(span-c_load_dist)+F_w_c*(c_load_dist))/span
	print("The Reaction at Reaction point a be Ra=", Ra)
	Rb = w_total - Ra
	print("The Reaction at Reaction point a be Rb=", Rb)

	#Bending Moments
	BM_cnc = Ra*c_load_dist - w_total_udl*(c_load_dist**2)/2
	print("Bending moment at the concentrated load points BM_cnc=",BM_cnc)
	BM_ctr = Ra*(span/2) - F_w_c*((span/2)-c_load_dist) - w_total_udl*0.5*(span/2)**2
	print("Bending moment at the center of the span BM_ctr=",BM_ctr)

	#Dimension of the Flange and the Web
	M_k = BM_cnc if (BM_cnc>BM_ctr) else BM_ctr #Consider the greater moment
	d = (M_k*(10**6)*k/f_y)**(0.33) #optimum depth of the plate girder
	d_r=round(d,-2)+100
	print(Fore.CYAN+"Depth of the Web is d=",d_r,""+Style.RESET_ALL)

	#Optimum thickness of the web
	tw = (M_k*10**6/(f_y*k**2))**0.33
	#Too small so increasing it
	tw = 1.8*tw
	print(Fore.CYAN+"Thickness of the Web is tw=",tw,""+Style.RESET_ALL)

	print(Fore.MAGENTA+"The Dimension of the web is", d_r, "x", tw,""+Style.RESET_ALL);

	#Design of Flange
	Af = (M_k*10**6*1.1)/(250*d_r)
	print(Fore.CYAN+"Area of the Flange Af=",Af,""+Style.RESET_ALL)

	#WIdth of the Flange
	bf= 0.3*d_r
	print(Fore.CYAN+"Width of the Flange = bf= ",bf,""+Style.RESET_ALL)
	tf=Af/bf
	print(Fore.CYAN+"Thickness of the flange is tf=",tf,""+Style.RESET_ALL)

	print(Fore.MAGENTA+"The Dimension of the flange plate is", bf, "x", tf,""+Style.RESET_ALL);

	#Classification
	b = (bf-tw)/2
	flag = b/tf
	if (flag>8.4):
		print(Fore.RED+"Section is not plastic as d/tw ratio =",flag,""+Style.RESET_ALL)
		exit()
	else:
		print(Fore.GREEN+"Section is plastic as d/tw ratio =",flag,""+Style.RESET_ALL)

	#Check for Bending Strength
	Zpz = 2*(bf*tf)*((d_r/2 + tf))
	print("Plastic Section modulus Zpz=",Zpz)
	Md = 0.92*Zpz*f_y/1.1
	print(Md)
	print(M_k)
	if(Md<(M_k*10**6)):
		print("safe")
	else:
		print("unsafe")

	#Check for Shear Capacity
	tow_cr = (5.35*3.14*3.14*2*10**5)/(12*(1-0.3)*(d/tw)**2)
	print("Value of T_cr = ", tow_cr)
	lmb_w = (f_y/(1.73*tow_cr))**0.5
	print("Value of lambda_W = ",lmb_w)
	tow_b = lmb_w/1.73
	if(lmb_w>0.8):
		tow_b = (1-0.8*(lmb_w-0.8))*f_y/1.73
	if(lmb_w>1.2):
		tow_b=(f_y/(1.73*lmb_w**2))
	print("The value of tow_b is = ",tow_b)
	Vcr = Af * tow_b/1000;
	if(Vcr > Ra):
		print(Fore.GREEN+"Safe in Shear Failure as Shear Force", Ra, " is smaller than", Vcr,""+Style.RESET_ALL);
	if(Vcr < Ra):
		print(Fore.RED+"Unsafe in Shear Failure Passed as Shear Force", Ra, " is greater than", Vcr,""+Style.RESET_ALL);

	#Flange to Web Connection
	#Let us provide the weld of Size = 6mm
	weld=6 #mm
	#Effective throat thickness
	t_e = 0.707*weld
	p_d=1*t_e*f_y/(1.1*1.73*1000)
	print("Weld Size = ",t_e)
	print(p_d)
	Izz = (bf*(d+tw)**3)/12 - ((bf-tw)*d**3)/12
	print(Izz)
	qw = (Ra*(Af)*(d+tf)/4)/Izz

	if(qw>p_d):
		print(Fore.GREEN+"Safe load on unit length of weld"+Style.RESET_ALL);
	else:
		print(Fore.RED+"Unsafe load on unit length of weld "+Style.RESET_ALL)

	#End Bearing Stiffner
	F_w = (125+2.5*(tf))*tw*250/1.1

	if(F_w<Ra):
		print(Fore.GREEN+"Safe, No stiffner is required"+Style.RESET_ALL);
		exit()
	else:
		print(Fore.RED+"Unsafe... Designing the End Bearing Stiffner "+Style.RESET_ALL)
		#Dimension of the end bearing stiffner
		eb_thk = 16 #Assuming
		eb_stf = 14*eb_thk
		print(Fore.MAGENTA+"The Dimesion of End bearing stiffner are", eb_thk," x ",eb_stf,""+Style.RESET_ALL)

		#Bearing capacity on the stiffners
		sf_stf = F_w-Ra #Shear Force on the stiffners
		w_stf = eb_stf - 15
		Fs = 2*w_stf*f_y/1.1
		if(Fs>Ra):
			print(Fore.GREEN+"End Bearing is safe in bearing"+Style.RESET_ALL);
		else:
			print(Fore.RED+"End Bearing is unsafe in Bearing. Redesign the Frame "+Style.RESET_ALL)
			exit()

		# Torsional Check for End Bearing Stiffner
		Is = (eb_thk*(eb_stf*2)**3)/12
		Iyy = (tf*bf**3)/6 + (d*tw**3)/12
		A_s = tf*bf*2 + d*tw
		rry = (Iyy/A_s)**0.5
		alpha_s = 30/(((span*10**3)/rry)**2)

		Is2 = 0.34*alpha_s*((d+2*tw)**3)*tf

		if(Is>Is2):
			print(Fore.GREEN+"End Stiffners are safe in torsional Loading"+Style.RESET_ALL)
		else:
			print(Fore.RED+"End Stiffners are not safe in torsional Loading"+Style.RESET_ALL)

		#Connection of End Bearing Stiffners
		weld_eb = 6 #Assuming the size of end bearing stiffner to be 6mm
		t_e_eb= 0.707*weld_eb
		#Strength of Shop weld per unit length
		P_dw_eb = t_e_eb*f_y/(1.73*1.25)

		#Available width of the stiffner connected to flange
		l_n_eb = eb_stf- 15
		#Tension Capacity
		Tdn = 0.9*(l_n_eb*tw)*410/1.25
		print("Tension capacity of one stiffner Tdn=",Tdn)
		#Shear Force Subjected to the unit length of the weild is
		q1 = Tdn/(2*(d-2*15))
		print("Shear Force Subjected to the unit length of the weild is q1=", q1)


		#Generating Image
		img = Image.open("plate.jpg")
		draw = ImageDraw.Draw(img)

		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 14)

		draw.text((400, 320),("bf = "+str(bf)),(0,0,0), font=font)
		draw.text((400, 340),("tf = "+str(tf)),(0,0,0), font=font)
		draw.text((400, 360),("tw = "+str(tw)),(0,0,0), font=font)
		draw.text((400, 380),("d = "+str(d)),(0,0,0), font=font)
		img.save('output.jpg')
		img.show()
