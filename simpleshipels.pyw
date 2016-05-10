##
# -*- coding: utf-8 -*-
from suds.client import Client
import logging, os, base64
from Tkinter import *
from PIL import ImageTk, Image


def raise_frame(frame):
    frame.tkraise()

def destroy_frame(frame):
	frame.destroy()
	
#Returns user to login frame after changing passphrase
def returnLogin():
	changePhraseFrame.forget()
	loginFrame.pack(side=LEFT, expand=True, fill=BOTH)
	
#Change passphrase frame
def changeppEntry():
	loginFrame.forget()
	mainFrame.forget()
	changePhraseFrame.pack(side=LEFT, expand=True, fill=BOTH)
	changeppEntry.acctNumber = StringVar()
	acctNumberLabel = Label(changePhraseFrame, text="Account Number:", bg='white').place(x=200, y=200)
	acctNumberEntry = Entry(changePhraseFrame, textvariable=changeppEntry.acctNumber, width=30, bd=2).place(x=320, y=200)
	changeppEntry.acctPassphrase = StringVar()
	acctPassphraseLabel = Label(changePhraseFrame, text="Cuurent Passphrase:", bg='white').place(x=200, y=230)
	acctPassphraseEntry = Entry(changePhraseFrame, textvariable=changeppEntry.acctPassphrase, width=30, bd=2, show="*").place(x=320, y=230)
	changeppEntry.acctNewPassphrase = StringVar()
	acctPassphraseLabel = Label(changePhraseFrame, text="New Passphrase:", bg='white').place(x=200, y=260)
	acctPassphraseEntry = Entry(changePhraseFrame, textvariable=changeppEntry.acctNewPassphrase, width=30, bd=2, show="*").place(x=320, y=260)
	loginButton = Button(changePhraseFrame, text="Submit", width=15, height=1, bg='black', fg='white', command=changePhrase).place(x=300, y=295)
	changePhraseLabel = Label(changePhraseFrame, text="Change Passphrase", bg='white', font='20')
	changePhraseLabel.place(x=290, y=100)
	changePhrase.successButton = Button(changePhraseFrame, text="Return To Login Page", bg="darkgray", fg='white', width="25", command=returnLogin).place(x=267, y=400)	
	
	
#Change passphrase XML request
def changePhrase():

	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
		<ChangePassPhraseRequest TokenRequested="false">
		<RequesterID>lxxx</RequesterID>
		<RequestID>1234</RequestID>
		<CertifiedIntermediary>
		  <AccountID>%s</AccountID>
		  <PassPhrase>%s</PassPhrase>
		  <Token></Token>
		</CertifiedIntermediary>
		<NewPassPhrase>%s</NewPassPhrase>
	  </ChangePassPhraseRequest>
	"""  % (changeppEntry.acctNumber.get(), changeppEntry.acctPassphrase.get(), changeppEntry.acctNewPassphrase.get())
	response = client.service.ChangePassPhraseXML(xml)
	changePhrase.successLabel = Label(changePhraseFrame, text="Passphrase Changed", bg='white', fg='darkgreen').place(x=300, y=322)
	
	
	
#Builds the GUI window
tk = Tk()
mainFrame = Frame(tk, bg='white')
loginFrame = Frame(tk, bg='white')
changePhraseFrame = Frame(tk, bg='white')
loginFrame.pack(side=LEFT, expand=True, fill=BOTH)
tk.title("SimpleShip")
tk.iconbitmap(default="ssicon.ico")
tk.configure(background='white')
tk.minsize(width=768, height=512)
tk.maxsize(width=768, height=512)
tk.geometry("768x512")



	
#Login frame
def loginEntry():
	loginEntry.acctNumber = StringVar()
	acctNumberLabel = Label(loginFrame, text="Account Number:", bg='white').place(x=200, y=200)
	acctNumberEntry = Entry(loginFrame, textvariable=loginEntry.acctNumber, width=30, bd=2).place(x=320, y=200)
	loginEntry.acctPassphrase = StringVar()
	acctPassphraseLabel = Label(loginFrame, text="Passphrase:", bg='white').place(x=200, y=230)
	acctPassphraseEntry = Entry(loginFrame, textvariable=loginEntry.acctPassphrase, width=30, bd=2, show="*").place(x=320, y=230)
	loginButton = Button(loginFrame, text="Login", width=15, height=1, bg='black', fg='white', command=login).place(x=300, y=265)	

#accountStatusRequestXML used to get account status and postage balance
def accountStatusRequest():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
		<AccountStatusRequest ResponseVersion="0">
		<RequesterID>lxxx</RequesterID>
		<RequestID>1234</RequestID>
		<CertifiedIntermediary>
		  <AccountID>%s</AccountID>
		  <PassPhrase>%s</PassPhrase>
		  <Token></Token>
		</CertifiedIntermediary>
	  </AccountStatusRequest>
	""" (accountStatusRequest.acctNumber, accountStatusRequest.acctPassphrase)
	response = client.service.GetAccountStatusXML(xml)
	accountStatusRequest.postageBalance = response.CertifiedIntermediary.PostageBalance
	accountStatusRequest.accountStatus = response.CertifiedIntermediary.AccountStatus
	accountStatusRequest.accountNumber = response.CertifiedIntermediary.AccountID

#login frame -- uses GetAccountStatusXML to verify correct credentials
def login():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
		<AccountStatusRequest ResponseVersion="0">
		<RequesterID>lxxx</RequesterID>
		<RequestID>1234</RequestID>
		<CertifiedIntermediary>
		  <AccountID>%s</AccountID>
		  <PassPhrase>%s</PassPhrase>
		  <Token></Token>
		</CertifiedIntermediary>
	  </AccountStatusRequest>
	"""  % (loginEntry.acctNumber.get(), loginEntry.acctPassphrase.get())
	response = client.service.GetAccountStatusXML(xml)
	
	postageBalance = response.CertifiedIntermediary.PostageBalance
	accountStatus = response.CertifiedIntermediary.AccountStatus
	accountNumber = response.CertifiedIntermediary.AccountID
	#Removes the login frame and displays the mainFrame
	loginFrame.forget()
	mainFrame.pack(side=LEFT, expand=True, fill=BOTH)
	status = Label(mainFrame, text='SimpleShip ELS 2016 Ver. 3.5 build 1656 Alpha', bd=1, relief=SUNKEN, anchor=W, width=110)
	status.place(x=0, y=494)
	
#Clears all entries except return address
def cleartextbox():
	toAddressEntry.delete(0, END)
	toNameEntry.delete(0, END)
	toCityEntry.delete(0, END)
	toStateEntry.delete(0, END)
	ToPostalCodeEntry.delete(0, END)
	weightEntry.delete(0, END)
	weight.set('0')
	lengthEntry.delete(0, END)
	length.set('0')
	widthEntry.delete(0, END)
	width.set('0')
	heightEntry.delete(0, END)
	depth.set('0')
	

#Adds file menu and options
menu = Menu(tk)
tk.config(menu=menu)
filemenu = Menu(menu, tearoff='0')
optionsmenu = Menu(menu, tearoff='0')
accountmenu = Menu(menu, tearoff='0')
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Exit", command=mainFrame.quit)
menu.add_cascade(label="Options", menu=optionsmenu)
optionsmenu.add_command(label="Clear Fields", command=cleartextbox)
menu.add_cascade(label="Account", menu=accountmenu)
accountmenu.add_command(label="Change Passphrase (Relogin Required)", command=changeppEntry)

status = Label(loginFrame, text='SimpleShip ELS 2016 Ver. 3.5 build 1656 Alpha', bd=1, relief=SUNKEN, anchor=W, width=110)
status.place(x=0, y=494)
status = Label(changePhraseFrame, text='SimpleShip ELS 2016 Ver. 3.5 build 1656 Alpha', bd=1, relief=SUNKEN, anchor=W, width=110)
status.place(x=0, y=494)



headerLogo = PhotoImage(file="SSLogo.gif")
headerImage = Label(loginFrame, image=headerLogo, borderwidth=0)
headerImage.place(x=190, y=10)

headerImage.image = headerLogo

headerLogo = PhotoImage(file="SSLogo.gif")
headerImage = Label(mainFrame, image=headerLogo, borderwidth=0)
headerImage.place(x=190, y=10)

#Label information entries
fromLabel = Label(mainFrame, text="From: ", bg='white').place(x=25, y=100)
enterFromName = Label(mainFrame, text="Full Name: ", bg='white').place(x=25, y=120)
fromName = StringVar()
fromNameEntry = Entry(mainFrame, textvariable=fromName, width=20, bd=2).place(x=98, y=120)

enterFromAddress = Label(mainFrame, text="Address: ", bg='white').place(x=25, y=140)
fromAddress = StringVar()
fromAddressEntry = Entry(mainFrame, textvariable=fromAddress, width=20, bd=2).place(x=98, y=140)

enterFromCity = Label(mainFrame, text="City: ", bg='white').place(x=25, y=160)
fromCity = StringVar()
FromCityEntry = Entry(mainFrame, textvariable=fromCity, width=20, bd=2).place(x=98, y=160)

enterFromState = Label(mainFrame, text="State: ", bg='white').place(x=25, y=180)
fromState = StringVar()
fromStateEntry = Entry(mainFrame, textvariable=fromState, width=20, bd=2).place(x=98, y=180)

enterFromPostalCode = Label(mainFrame, text="Zip Code: ", bg='white').place(x=25, y=200)
fromPostalCode = StringVar()
fromPostalCodeEntry = Entry(mainFrame, textvariable=fromPostalCode, width=20, bd=2).place(x=98, y=200)


toLabel = Label(mainFrame, text="To: ", bg='white').place(x=265, y=100)
enterToName = Label(mainFrame, text="Full Name: ", bg='white').place(x=265, y=120)
toName = StringVar()
toNameEntry = Entry(mainFrame, textvariable=toName, width=20, bd=2)
toNameEntry.place(x=335, y=120)
enterToAddress = Label(mainFrame, text="Address: ", bg='white').place(x=265, y=140)
toAddress = StringVar()
toAddressEntry = Entry(mainFrame, textvariable=toAddress, width=20, bd=2)
toAddressEntry.place(x=335, y=140)

enterToCity = Label(mainFrame, text="City: ", bg='white').place(x=265, y=160)
toCity = StringVar()
toCityEntry = Entry(mainFrame, textvariable=toCity, width=20, bd=2)
toCityEntry.place(x=335, y=160)

enterToState = Label(mainFrame, text="State: ", bg='white').place(x=265, y=180)
toState = StringVar()
toStateEntry = Entry(mainFrame, textvariable=toState, width=20, bd=2)
toStateEntry.place(x=335, y=180)

enterToPostalCode = Label(mainFrame, text="Zip Code: ", bg='white').place(x=265, y=200)
toPostalCode = StringVar()
ToPostalCodeEntry = Entry(mainFrame, textvariable=toPostalCode, width=20, bd=2)
ToPostalCodeEntry.place(x=335, y=200)

chooseMailClass = Label(mainFrame, text="Mail Class: ", bg='white')
chooseMailClass.place(x=25, y=240)
mailClassOptions = ['First', 'Priority', 'PriorityExpress', 'ParcelSelect', 'MediaMail', 'LibraryMail']
mClass = StringVar()
mClass.set(mailClassOptions[0])
drop = OptionMenu(mainFrame, mClass, *mailClassOptions)
drop.config(bg='darkgray', fg='white')
drop.place(x=110, y=235)

choosePackageType = Label(mainFrame, text="Package Type: ", bg='white')
choosePackageType.place(x=25, y=285)
packageTypes = ['Flat', 'Parcel', 'FlatRateEnvelope', 'SmallFlatRateEnvelope',
 'MediumFlatRateBox', 'LargeFlatRateBox', 'SmallFlatRateBox', 'FlatRatePaddedEnvelope', 'FlatRateLegalEnvelope']
packagetype = StringVar()
packagetype.set(packageTypes[1])
drop2 = OptionMenu(mainFrame, packagetype, *packageTypes)
drop2.config(bg='darkgray', fg='white')
drop2.place(x=110, y=280)

chooseWeightOz = Label(mainFrame, text="Weight in Oz: ", bg='white').place(x=25, y=330)
weight = StringVar()
weight.set(0)
weightEntry = Entry(mainFrame, textvariable=weight, width=5, bd=2)
weightEntry.place(x=112, y=330)

enterWidth = Label(mainFrame, text="Width: ", bg='white').place(x=230, y=240)
width = StringVar()
width.set(0)
widthEntry = Entry(mainFrame, textvariable=width, width=4, bd=2)
widthEntry.place(x=280, y=240)

enterHeight = Label(mainFrame, text="Height: ", bg='white').place(x=317, y=240)
depth = StringVar()
depth.set(0)
heightEntry = Entry(mainFrame, textvariable=depth, width=4, bd=2)
heightEntry.place(x=365, y=240)

enterLength = Label(mainFrame, text="Length: ", bg='white').place(x=400, y=240)
length = StringVar()
length.set(0)
lengthEntry = Entry(mainFrame, textvariable=length, width=4, bd=2)
lengthEntry.place(x=450, y=240)


specServices = Label(mainFrame, text="Special Services: ", bg='white').place(x=230, y=280)
hidePostage = StringVar()
insurance = StringVar()
enableSample = StringVar()

C1 = Checkbutton(mainFrame, text="Hide Postage", variable=hidePostage, onvalue='TRUE', offvalue='FALSE', bg='white')
C1.place(x=230, y=300)
C1.deselect()
C2 = Checkbutton(mainFrame, text='Insurance', variable=insurance, onvalue=YES, offvalue=NO, bg='white')
C2.place(x=230, y=320)
C2.deselect()
C3 = Checkbutton(mainFrame, text="Sample Label", variable=enableSample, onvalue='YES', offvalue='NO', bg='white')
C3.place(x=267, y=459)
C3.deselect()

#CalculatePostageRateXML request
def postageRateRequest():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
	   <PostageRateRequest>
		<RequesterID>lxxx</RequesterID>
		<CertifiedIntermediary>
		  <AccountID>%s</AccountID>
		  <PassPhrase>%s</PassPhrase>
		  <Token></Token>
		</CertifiedIntermediary>
		<MailClass>%s</MailClass>
		<WeightOz>%s</WeightOz>
		<MailpieceShape>%s</MailpieceShape>
		<Services DeliveryConfirmation="OFF" SignatureConfirmation="OFF"/>
		<FromPostalCode>%s</FromPostalCode>
		<ToPostalCode>%s</ToPostalCode>
		<ResponseOptions PostagePrice=""/>
	   </PostageRateRequest>
	""" % (loginEntry.acctNumber.get(), loginEntry.acctPassphrase.get(), mClass.get(), weight.get(), packagetype.get(), fromPostalCode.get(), toPostalCode.get())
	response = client.service.CalculatePostageRateXML(xml)
	postageRateRequest.postageRate = response.Postage[0].Rate
	postageRateRequest.labelPrice = Label(mainFrame, text="${}".format(postageRateRequest.postageRate), bg='white', relief=GROOVE, width=8).place(x=420, y=280)

labelCost = Label(mainFrame, text="Label Price:", bg='white').place(x=345, y=280)
#Starts the mainFrame with 0.00 label price
labelPriceStart = Label(mainFrame, text="0.00", bg='white', relief=GROOVE, width=8).place(x=420, y=280)
getRateButton = Button(mainFrame, text="Get Rate", width=8, height=1, bg='black', fg='white', command=postageRateRequest).place(x=344, y=310)

#BuyPostageXML request 
def buyPostageRequest():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
	   <RecreditRequest>
	     <RequesterID>lxxx</RequesterID>
		 <RequestID>1234214234</RequestID>
		 <CertifiedIntermediary>
		   <AccountID>%s</AccountID>
		   <PassPhrase>%s</PassPhrase>
		 </CertifiedIntermediary>
	     <RecreditAmount>%s</RecreditAmount>
	   </RecreditRequest>
	""" %(loginEntry.acctNumber.get(), loginEntry.acctPassphrase.get(), postageamount.get())
	response = client.service.BuyPostageXML(xml)
	accountStatusRequest()
	status = Label(mainFrame, text='SimpleShip ELS 2016 Ver. 3.1 build 1655 Alpha', bd=1, relief=SUNKEN, anchor=W, width=110)
	status.place(x=0, y=494)


buyPostagelabel = Label(mainFrame, text="Buy Postage:", bg='white').place(x=25, y=375)
choosePostageAmount = Label(mainFrame, text="Postage Amount: ", bg='white')
choosePostageAmount.place(x=25, y=400)
postageAmounts = ['10', '25', '50', '100', '250', '500']
postageamount = StringVar()
#Sets default postage amount option
postageamount.set('10')
drop4 = OptionMenu(mainFrame, postageamount, *postageAmounts)
drop4.config(bg='darkgray', fg='white')
drop4.place(x=125, y=395)
buyPostageButton = Button(mainFrame, text="Buy Now", width=8, height=1, bg='black', fg='white', command=buyPostageRequest).place(x=27, y=428)


chooseImageFormat = Label(mainFrame, text="Save Label As:", bg='white')
chooseImageFormat.place(x=293, y=400)
imageTypes = ['EPL2', 'ZPLII', 'GIF', 'JPEG', 'PNG', 'PDF']
imagetype = StringVar()
imagetype.set('JPEG')
drop3 = OptionMenu(mainFrame, imagetype, *imageTypes)
drop3.config(bg='darkgray', fg='white')
drop3.place(x=377, y=395)

#Starts mainFrame with blank label preview
image = Image.open("Labelsample_blank.jpg")
image = image.resize((251, 377), Image.ANTIALIAS) #The (250, 250) is (height, width)
samplePic1 = ImageTk.PhotoImage(image)
sampleLabel = Label(mainFrame, image=samplePic1)
sampleLabel.place(x=493, y=100)


#Gets a sample label from label server, converts it from base64 to image type and displays it
def previewLabel():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
	<LabelRequest Test="YES" LabelType="Default" LabelSize="4x6"
	ImageFormat="%s">
	  <RequesterID>lxxx</RequesterID>
	  <AccountID>%s</AccountID>
	  <PassPhrase>%s</PassPhrase>
      <Token></Token>
      <MailClass>%s</MailClass>
      <DateAdvance>0</DateAdvance>
      <WeightOz>%s</WeightOz>
      <MailpieceShape>%s</MailpieceShape>
      <Stealth>%s</Stealth>
      <Services InsuredMail="OFF" SignatureConfirmation="OFF" />
      <Value>0</Value>
      <PartnerCustomerID></PartnerCustomerID>
      <PartnerTransactionID>1234</PartnerTransactionID>
      <ToName>%s</ToName>
      <ToCompany></ToCompany>
      <ToAddress1>%s</ToAddress1>
      <ToCity>%s</ToCity>
      <ToState>%s</ToState>
      <ToPostalCode>%s</ToPostalCode>
      <ToZIP4></ToZIP4>
      <ToDeliveryPoint></ToDeliveryPoint>
      <ToPhone></ToPhone>
      <FromName>%s</FromName>
      <FromCompany></FromCompany> 
      <ReturnAddress1>%s</ReturnAddress1>
      <FromCity>%s</FromCity>
      <FromState>%s</FromState>
      <FromPostalCode>%s</FromPostalCode>
      <FromZIP4></FromZIP4>
      <FromPhone></FromPhone>
      <ResponseOptions PostagePrice=""/>
	</LabelRequest>
	""" % (imagetype.get(), loginEntry.acctNumber.get(), loginEntry.acctPassphrase.get(), mClass.get(), weight.get(), packagetype.get(), hidePostage.get(), toName.get(), toAddress.get(), toCity.get(), toState.get(), toPostalCode.get(), fromName.get(), fromAddress.get(), fromCity.get(), fromState.get(), fromPostalCode.get())
	response = client.service.GetPostageLabelXML(xml)

	#Conversion base64 to label type chosen. Does not work with PDF, EPL and ZPL
	code = response.Base64LabelImage
	with open(os.path.expanduser('~/Desktop//simpleship/Labelpreview.%s') % (imagetype.get()), 'wb') as fout:
	  fout.write(base64.decodestring(code))
	print response
	image = Image.open("Labelpreview" + "." + "{}".format(imagetype.get()))
	image = image.resize((251, 377), Image.ANTIALIAS)  # The (250, 250) is (height, width) 240, 360
	samplePic2 = ImageTk.PhotoImage(image)
	sampleLabel.config(image=samplePic2)
	sampleLabel.image = samplePic2
	mainFrame.update_idletasks()

previewLabelButton = Button(mainFrame, text="Preview Label", width=13, height=1, bg='black', fg='white', command=previewLabel).place(x=360, y=435)


#Label request function
def elsRequest():
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)

	url = 'https://elstestserver.endicia.com/LabelService/EwsLabelService.asmx?wsdl'
	client = Client(url)

	xml = \
	"""<?xml version="1.0" encoding="utf-8"?>
	<LabelRequest Test="%s" LabelType="Default" LabelSize="4x6"
	ImageFormat="%s">
	  <RequesterID>lxxx</RequesterID>
	  <AccountID>%s</AccountID>
	  <PassPhrase>%s</PassPhrase>
      <Token></Token>
      <MailClass>%s</MailClass>
      <DateAdvance>0</DateAdvance>
      <WeightOz>%s</WeightOz>
      <MailpieceShape>%s</MailpieceShape>
      <Stealth>%s</Stealth>
      <Services InsuredMail="OFF" SignatureConfirmation="OFF" />
      <Value>0</Value>
      <PartnerCustomerID></PartnerCustomerID>
      <PartnerTransactionID>1234</PartnerTransactionID>
      <ToName>%s</ToName>
      <ToCompany></ToCompany>
      <ToAddress1>%s</ToAddress1>
      <ToCity>%s</ToCity>
      <ToState>%s</ToState>
      <ToPostalCode>%s</ToPostalCode>
      <ToZIP4></ToZIP4>
      <ToDeliveryPoint></ToDeliveryPoint>
      <ToPhone></ToPhone>
      <FromName>%s</FromName>
      <FromCompany></FromCompany> 
      <ReturnAddress1>%s</ReturnAddress1>
      <FromCity>%s</FromCity>
      <FromState>%s</FromState>
      <FromPostalCode>%s</FromPostalCode>
      <FromZIP4></FromZIP4>
      <FromPhone></FromPhone>
      <ResponseOptions PostagePrice=""/>
	</LabelRequest>
	""" % (enableSample.get(), imagetype.get(),loginEntry.acctNumber.get(), loginEntry.acctPassphrase.get(), mClass.get(), weight.get(), packagetype.get(), hidePostage.get(), toName.get(), toAddress.get(), toCity.get(), toState.get(), toPostalCode.get(), fromName.get(), fromAddress.get(), fromCity.get(), fromState.get(), fromPostalCode.get())
	response = client.service.GetPostageLabelXML(xml)

	code = response.Base64LabelImage
	with open(os.path.expanduser('~/Desktop//simpleship/Label.%s') % (imagetype.get()), 'wb') as fout:
	  fout.write(base64.decodestring(code))
	print response
	accountStatusRequest()
	status = Label(mainFrame, text='SimpleShip ELS 2016 Ver. 3.5 build 1656 Alpha', bd=1, relief=SUNKEN, anchor=W, width=110)
	status.place(x=0, y=494)

	image = Image.open("Label" + "." + "{}".format(imagetype.get()))
	image = image.resize((251, 377), Image.ANTIALIAS)  # The (250, 250) is (height, width) 240, 360
	samplePic2 = ImageTk.PhotoImage(image)
	sampleLabel.config(image=samplePic2)
	sampleLabel.image = samplePic2
	mainFrame.update_idletasks()

printLabel = Button(mainFrame, text="Print Label", width=10, height=1, bg='black', fg='white', command=elsRequest).place(x=270, y=435)



#Starts program with login frame first	
loginEntry()
raise_frame(loginFrame)
tk.mainloop()