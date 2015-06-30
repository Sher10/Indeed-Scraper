import requests
import multiprocessing
from multiprocessing import Pool
from threading import Thread
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib, cookielib, urllib2


url = 'https://secure.indeed.com/account/login'

the_queue = multiprocessing.Queue()

username = 'sam.t.massey@gmail.com'
password = 'Resumazing051814'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17'
headers = { 'User-Agent' : user_agent }
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'email': username, 'password': password})
req = urllib2.Request(url, login_data, headers)

opener.open(req, login_data)

BASE_URL = "http://www.indeed.com"


def get_resumes(section_url):
	# opener.open('https://secure.indeed.com/account/login', login_data)
	# print "top"
	# try:	
	print 'HI'
	html = opener.open(section_url).read()
	print html
	soup = BeautifulSoup(html, "lxml")
	resultsList = soup.find("ol", "resultsList")
	resume_links = [BASE_URL + li.a["href"] for li in resultsList.findAll("li")]
	# except Exception as e:
		# print section_url, "ERROR"
		# print Exception
		# resume_links = []
	# for link in resume_links:
	# 	output.put(link)
	print resume_links
	return resume_links

def next_page(page_url):
	# opener.open('https://secure.indeed.com/account/login', login_data)
	try:	
	# continuing_url = "http://www.indeed.com/resumes/microsoft"
		continuing_url = page_url
		html = opener.open(page_url).read()
		soup = BeautifulSoup(html, "lxml")
		if((soup.find("a", "instl confirm-nav next")==None)):
			page_link = "no next"
			return page_link
		next_page = soup.find("a", "instl confirm-nav next").get('href')
		page_link = continuing_url + next_page
	except urllib2.HTTPError:
		print page_url, "ERROR"
		page_link = "no next"
	# 	page_link = "no next"
	return page_link




def ResumeDownloader(company):
	# print "IN HERE"
	page_url = "http://www.indeed.com/resumes/"+str(company)+"?co=US&start="
	links = []
	resumeUrls = []
	# print page_url
	# while(page_url and page_url!="no next"):
	# 	links.append(get_resumes(page_url))
	# 	page_url = next_page(page_url)
	# return links
	pageValue = 0
	for value in range(0,99):
		pageValue = pageValue+50
		links.append(page_url+str(pageValue))

	for link in links:
		resumeUrls.append(get_resumes(link))
	return resumeUrls

def resume_parallel(fn, l):
	for i in l:
		Thread(target=fn, args=(i,)).start()


def main():

	# pool = Pool(10)
	# company_list = ["21Vianet Group", "2U", "3D Systems", "51job", "58.com", "A10 Networks", "Aaron's", "ACI Worldwide", "Actions Semiconductor", "Activision Blizzard", "Actua", "Actuant", "Acxiom", "Adept Technology", "Adobe Systems", "Advanced Micro Devices", "Advanced Semiconductor Engineering", "Advantest (Kabushiki Kaisha Advantest) ADS", "Advent Software", "Aercap Holdings", "AeroCentury", "Aerohive Networks", "AG&E Holdings", "Agilysys", "Air Lease", "Aircastle", "AirMedia Group", "Aixtron SE", "Alliance Fiber Optic Products", "Allot Communications", "Allscripts Healthcare Solutions", "Alpha and Omega Semiconductor", "Altera", "Amaya", "Ambarella", "Amber Road", "Amdocs", "American Software", "Amkor Technology", "AMN Healthcare Services", "Amtech Systems", "ANADIGICS", "Analog Devices", "ANSYS", "AOL", "API Technologies", "Apigee", "Apple", "Applied Materials", "Applied Micro Circuits", "Applied Optoelectronics", "ARI Network Services", "Arista Networks", "ARM Holdings plc", "ARRIS Group", "Ascent Solar Technologies", "ASM International", "ASML Holding", "Aspen Technology", "Astro-Med", "Asure Software", "Atmel", "Attunity", "AU Optronics", "Audience", "Authentidate Holding", "Autobytel", "Autodesk", "Autohome", "Automatic Data Processing", "Avago Technologies", "AVG Technologies", "Aviat Networks", "Avolon Holdings", "Aware", "Axcelis Technologies", "AXT", "B.O.S. Better Online Solutions", "Baidu", "Barracuda Networks", "Barrett Business Services", "Bazaarvoice", "Benchmark Electronics", "Benefitfocus", "BG Staffing", "Bitauto Holdings", "Black Box", "Black Knight Financial Services", "Blackbaud", "Blonder Tongue Laboratories", "Blucora", "Bottomline Technologies", "Box", "Bridgeline Digital", "Brightcove", "Broadcom", "BroadSoft", "BroadVision", "Brocade Communications Systems", "Brooks Automation", "CA", "Cabot Microelectronics", "CACI International", "Cadence Design Systems", "Cai International", "CalAmp", "Callidus Software", "Canadian Solar", "Carbonite", "Castlight Health", "Cavium", "CDI", "Celestica", "Ceragon Networks", "Cerner", "CEVA", "Changyou.com", "ChannelAdvisor", "Check Point Software Technologies", "Cheetah Mobile", "Chicago Rivet & Machine", "China Digital TV Holding", "China Information Technology", "China Mobile Games and Entertainment Group", "China Sunergy", "ChinaCache International Holdings", "ChinaNet Online Holdings", "ChipMOS TECHNOLOGIES (Bermuda)", "Ciber", "Cirrus Logic", "Cisco Systems", "Citrix Systems", "Cleantech Solutions International", "ClickSoftware Technologies", "Code Rebel", "Cogent Communications Holdings", "Cognizant Technology Solutions", "CollabRx", "CommScope Holding Company", "CommVault Systems", "Computer Programs and Systems", "Computer Sciences", "Computer Task Group", "Comtech Telecommunications", "Concurrent Computer", "Connecture", "Constant Contact", "Convergys", "CoreLogic", "Cornerstone OnDemand", "CounterPath", "Cover-All Technologies", "Covisint", "Cray", "Cree", "Criteo", "Cross Country Healthcare", "Crossroads Systems", "CSG Systems International", "CSP", "CSR plc", "CTPartners Executive Search", "CTS", "Curtiss-Wright", "CVD Equipment", "CVENT", "Cyan", "CyberArk Software", "Cypress Semiconductor", "CYREN", "Daegis", "DAQO New Energy", "Datalink", "Dataram", "Datawatch", "Dealertrack Technologies", "Demand Media", "DEMANDWARE", "Digi International", "Digimarc", "Digital Ally", "Diodes", "DLH Holdings", "Document Security Systems", "Dolby Laboratories", "Dot Hill Systems", "Dover", "DSP Group", "DST Systems", "EarthLink Holdings", "Eaton", "Ebix", "Echelon", "EchoStar", "Edgewater Technology", "eFuture Information Technology", "eGain", "Electro Rent", "Electronic Arts", "Electronics for Imaging", "Ellie Mae", "Eltek", "eMagin", "EMC", "EMCORE", "Endurance International Group Holdings", "Energous", "Energy Recovery", "EnerNOC", "Enphase Energy", "Envivio", "EPAM Systems", "EPIQ Systems", "ePlus", "Ericsson", "Evertec", "Evolving Systems", "Exa", "Exar", "Exterran Holdings", "Extreme Networks", "EZchip Semiconductor", "F5 Networks", "Facebook", "FactSet Research Systems", "Fairchild Semiconductor International", "FalconStor Software", "Finisar", "FireEye", "First Solar", "Fiserv", "Five9", "Fleetmatics Group", "Flextronics International", "FormFactor", "Formula Systems (1985)", "Fortinet", "Freescale Semiconductor", "General Employment Enterprises", "GigaMedia", "Gigamon", "GigOptix", "Gilat Satellite Networks", "GlobalSCAPE", "Globant S.A.", "Glu Mobile", "GoDaddy", "Google", "Graham", "Groupon", "GSE Systems", "GSI Technology", "Guidance Software", "Guidewire Software", "Hanwha Q CELLS", "Harmonic", "Harte-Hanks", "HealthStream", "Heidrick & Struggles International", "Hewlett-Packard", "Himax Technologies", "HomeAway", "Hortonworks", "HubSpot", "Hudson Global", "Identiv", "iDreamSky Technology", "IEC Electronics", "iGATE", "IHS", "Illinois Tool Works", "Imation", "Immersion", "Imperva", "Imprivata", "IMS Health Holdings", "inContact", "Infoblox", "Informatica", "Infosys", "Ingram Micro", "Innodata", "Innovative Solutions and Support", "Inovalon Holdings", "Inphi", "Insperity", "Integrated Device Technology", "Integrated Silicon Solution", "Intel", "Intellicheck Mobilisa", "Interactive Intelligence Group", "Intermolecular", "Internap", "International Business Machines", "Internet Initiative Japan", "Interphase", "Interpublic Group of Companies (The)", "Intersections", "Intersil", "InterXion Holding", "Intevac", "IntraLinks Holdings", "Intuit", "InvenSense", "iPass", "IPG Photonics", "IXYS", "j2 Global", "JA Solar Holdings", "Jabil Circuit", "Jack Henry & Associates", "JDS Uniphase", "Jiayuan.com International", "JinkoSolar Holding Company", "Jive Software", "John Bean Technologies", "Juniper Networks", "Kadant", "Kelly Services", "Key Technology", "Key Tronic", "Kforce", "Kimball Electronics", "King Digital Entertainment", "Kingtone Wirelessinfo Solution Holding", "KongZhong", "Kopin", "Kulicke and Soffa Industries", "KVH Industries", "Kyocera", "L-3 Communications Holdings", "Lam Research", "Lantronix", "Lattice Semiconductor", "Leidos Holdings", "Lexmark International", "Liberty TripAdvisor Holdings", "LifeLock", "LightPath Technologies", "Lincoln Electric Holdings", "Linear Technology", "LinkedIn", "LiqTech International", "Liquid Holdings Group", "LiveDeal", "LivePerson", "Logitech International S.A.", "LogMein", "LookSmart", "Loral Space and Communications", "Luxoft Holding", "Magic Software Enterprises", "MagnaChip Semiconductor", "MagneGas", "Majesco Entertainment", "MAM Software Group", "Manhattan Associates", "Manitex International", "ManpowerGroup", "Marin Software", "Marketo", "Marvell Technology Group", "Materialise", "Mattson Technology", "Maxim Integrated Products", "MaxLinear", "McGrath RentCorp", "MDC Partners", "MedAssets", "Medical Transcription Billing", "Medidata Solutions", "Mellanox Technologies", "Mentor Graphics", "Merge Healthcare", "Meru Networks", "Micrel", "Microchip Technology", "Micron Technology", "Microsemi", "Microsoft", "MicroStrategy", "Millennial Media", "MIND C.T.I.", "Mitcham Industries", "Mitek Systems", "Mitel Networks", "MiX Telematics", "MobileIron", "Mobileye", "Model N", "ModSys International", "Moko Social Media", "Momo", "Monolithic Power Systems", "Monotype Imaging Holdings", "Monster Worldwide", "Moog", "MoSys", "Motorola Solutions", "MRV Communications", "Multi-Fineline Electronix", "National Instruments", "NCI", "Neff", "NeoPhotonics", "Net Element", "NetApp", "Netlist", "NetScout Systems", "NetSol Technologies", "Netsuite", "Network-1 Technologies", "New Relic", "NICE-Systems", "Nimble Storage", "Nokia", "NQ Mobile", "NTT DOCOMO", "Nuance Communications", "NVE", "NVIDIA", "NXP Semiconductors", "O2Micro International", "Oclaro", "Omnicell", "Omnicom Group", "OmniVision Technologies", "On Assignment", "ON Semiconductor", "On Track Innovations", "Open Text", "Opower", "Oracle", "OSI Systems", "P & F Industries", "Palo Alto Networks", "Park City Group", "Park Electrochemical", "ParkerVision", "Paycom Software", "Paylocity Holding", "PC-Tel", "PDF Solutions", "Pegasystems", "Pentair", "Perficient", "Pericom Semiconductor", "Perion Network", "Photronics", "Pixelworks", "Plexus", "PMC - Sierra", "Pointer Telocation", "Power Integrations", "Professional Diversity Network", "Progress Software", "Proofpoint", "PROS Holdings", "PTC", "Q2 Holdings", "QAD", "Qihoo 360 Technology", "Qlik Technologies", "QLogic", "Qorvo", "QUALCOMM", "Quality Systems", "Qualstar", "Qualys", "Quantum", "Quest Resource Holding", "QuickLogic", "Qumu", "Rackspace Hosting", "Radcom", "RadiSys", "Rally Software Development", "Rambus", "RCM Technologies", "ReachLocal", "RealD", "RealNetworks", "RealPage", "Red Hat", "RELM Wireless", "Renesola", "Renren", "Rent-A-Center", "Resonant", "Rexnord", "Ringcentral", "Robert Half International", "Rocket Fuel", "Rosetta Stone", "Rubicon Technology", "Ruckus Wireless", "Sabre", "Salesforce.com", "SanDisk", "Sanmina", "SAP SE", "Sapiens International N.V.", "ScanSource", "SCIENCE APPLICATIONS INTERNATIONAL", "Scientific Games", "SciQuest", "SeaChange International", "Seagate", "Selectica", "Semiconductor  Manufacturing International", "SemiLEDS", "Semtech", "Sequans Communications S.A.", "ServiceNow", "SGOCO Group", "Shopify", "Shutterstock", "Sierra Wireless", "Sify Technologies", "Sigma Designs", "SigmaTron International", "Silicom", "Silicon Graphics International", "Silicon Laboratories", "Silicon Motion Technology", "Siliconware Precision Industries Company", "Silver Spring Networks", "Simulations Plus", "Sina", "Sky-mobi", "Skyworks Solutions", "SMART Technologies", "Smith Micro Software", "SMTC", "SMTP", "Sohu.com", "SolarEdge Technologies", "Solarwinds", "Solera Holdings", "Sonic Foundry", "Sonus Networks", "SouFun Holdings", "Sparton", "Speed Commerce", "Sphere 3D", "Splunk", "SPS Commerce", "SPX", "SS&C Technologies Holdings", "Standex International", "StarTek", "STMicroelectronics", "Stratasys", "Streamline Health Solutions", "SunEdison Semiconductor", "SunEdison", "Sungy Mobile", "SunPower", "Super Micro Computer", "SuperCom", "Superconductor Technologies", "support.com", "Sykes Enterprises", "Symantec", "Synacor", "Synaptics", "Synchronoss Technologies", "Synnex", "Synopsys", "Syntel", "Sysorex Global Holding", "Tableau Software", "Taiwan Semiconductor Manufacturing Company", "Take-Two Interactive Software", "TAL International Group", "Tangoe", "Team Health Holdings", "Tech Data", "Technical Communications", "TeleCommunication Systems", "TeleTech Holdings", "Tennant Company", "Teradata", "Tessera Technologies", "Texas Instruments", "Textainer Group Holdings", "Textura", "The Descartes Systems Group", "The KEYW Holding", "The Middleby", "The Rubicon Project", "The Ultimate Software Group", "TigerLogic", "Top Image Systems", "Tower Semiconductor", "TransAct Technologies", "Travelzoo", "Tremor Video", "Trina Solar", "Trio-Tech International", "TripAdvisor", "TrueBlue", "TrueCar", "TSR", "TTM Technologies", "TubeMogul", "Tucows", "Twin", "Twitter", "Tyler Technologies", "UBIC", "Ubiquiti Networks", "Ultra Clean Holdings", "Ultratech", "Unisys", "United Microelectronics", "United Online", "United Rentals", "Unwired Planet", "Upland Software", "Varonis Systems", "VASCO Data Security International", "Veeco Instruments", "Veeva Systems", "Verint Systems", "VeriSign", "Verisk Analytics", "ViaSat", "Viggle", "Vimicro International", "Violin Memory", "Virtusa", "VisionChina Media", "Vmware", "Volt Information Sciences", "Vuzix", "Wave Systems", "Wayside Technology Group", "Web.com Group", "Weibo", "Western Digital", "WidePoint", "Wipro", "Wix.com", "Workday", "Workiva", "Wowo", "WPP", "WSI Industries", "Xilinx", "Xplore Technologies", "Xunlei", "Yahoo", "Yandex", "Yingli Green Energy Holding Company", "Yodlee", "Youku Tudou", "YuMe", "YY", "Zebra Technologies", "Zendesk", "Zhaopin", "Zix", "Zynga"]
	company_list_2 = ["Jabil Circuit", "Jack Henry & Associates", "JDS Uniphase", "Jiayuan.com International", "JinkoSolar Holding Company", "Jive Software", "John Bean Technologies", "Juniper Networks", "Kadant", "Kelly Services", "Key Technology", "Key Tronic", "Kforce", "Kimball Electronics", "King Digital Entertainment", "Kingtone Wirelessinfo Solution Holding", "KongZhong", "Kopin", "Kulicke and Soffa Industries", "KVH Industries", "Kyocera", "L-3 Communications Holdings", "Lam Research", "Lantronix", "Lattice Semiconductor", "Leidos Holdings", "Lexmark International", "Liberty TripAdvisor Holdings", "LifeLock", "LightPath Technologies", "Lincoln Electric Holdings", "Linear Technology", "LinkedIn", "LiqTech International", "Liquid Holdings Group", "LiveDeal", "LivePerson", "Logitech International S.A.", "LogMein", "LookSmart", "Loral Space and Communications", "Luxoft Holding", "Magic Software Enterprises", "MagnaChip Semiconductor", "MagneGas", "Majesco Entertainment", "MAM Software Group", "Manhattan Associates", "Manitex International", "ManpowerGroup", "Marin Software", "Marketo", "Marvell Technology Group", "Materialise", "Mattson Technology", "Maxim Integrated Products", "MaxLinear", "McGrath RentCorp", "MDC Partners", "MedAssets", "Medical Transcription Billing", "Medidata Solutions", "Mellanox Technologies", "Mentor Graphics", "Merge Healthcare", "Meru Networks", "Micrel", "Microchip Technology", "Micron Technology", "Microsemi", "Microsoft", "MicroStrategy", "Millennial Media", "MIND C.T.I.", "Mitcham Industries", "Mitek Systems", "Mitel Networks", "MiX Telematics", "MobileIron", "Mobileye", "Model N", "ModSys International", "Moko Social Media", "Momo", "Monolithic Power Systems", "Monotype Imaging Holdings", "Monster Worldwide", "Moog", "MoSys", "Motorola Solutions", "MRV Communications", "Multi-Fineline Electronix", "National Instruments", "NCI", "Neff", "NeoPhotonics", "Net Element", "NetApp", "Netlist", "NetScout Systems", "NetSol Technologies", "Netsuite", "Network-1 Technologies", "New Relic", "NICE-Systems", "Nimble Storage", "Nokia", "NQ Mobile", "NTT DOCOMO", "Nuance Communications", "NVE", "NVIDIA", "NXP Semiconductors", "O2Micro International", "Oclaro", "Omnicell", "Omnicom Group", "OmniVision Technologies", "On Assignment", "ON Semiconductor", "On Track Innovations", "Open Text", "Opower", "Oracle", "OSI Systems", "P & F Industries", "Palo Alto Networks", "Park City Group", "Park Electrochemical", "ParkerVision", "Paycom Software", "Paylocity Holding", "PC-Tel", "PDF Solutions", "Pegasystems", "Pentair", "Perficient", "Pericom Semiconductor", "Perion Network", "Photronics", "Pixelworks", "Plexus", "PMC - Sierra", "Pointer Telocation", "Power Integrations", "Professional Diversity Network", "Progress Software", "Proofpoint", "PROS Holdings", "PTC", "Q2 Holdings", "QAD", "Qihoo 360 Technology", "Qlik Technologies", "QLogic", "Qorvo", "QUALCOMM", "Quality Systems", "Qualstar", "Qualys", "Quantum", "Quest Resource Holding", "QuickLogic", "Qumu", "Rackspace Hosting", "Radcom", "RadiSys", "Rally Software Development", "Rambus", "RCM Technologies", "ReachLocal", "RealD", "RealNetworks", "RealPage", "Red Hat", "RELM Wireless", "Renesola", "Renren", "Rent-A-Center", "Resonant", "Rexnord", "Ringcentral", "Robert Half International", "Rocket Fuel", "Rosetta Stone", "Rubicon Technology", "Ruckus Wireless", "Sabre", "Salesforce.com", "SanDisk", "Sanmina", "SAP SE", "Sapiens International N.V.", "ScanSource", "SCIENCE APPLICATIONS INTERNATIONAL", "Scientific Games", "SciQuest", "SeaChange International", "Seagate", "Selectica", "Semiconductor  Manufacturing International", "SemiLEDS", "Semtech", "Sequans Communications S.A.", "ServiceNow", "SGOCO Group", "Shopify", "Shutterstock", "Sierra Wireless", "Sify Technologies", "Sigma Designs", "SigmaTron International", "Silicom", "Silicon Graphics International", "Silicon Laboratories", "Silicon Motion Technology", "Siliconware Precision Industries Company", "Silver Spring Networks", "Simulations Plus", "Sina", "Sky-mobi", "Skyworks Solutions", "SMART Technologies", "Smith Micro Software", "SMTC", "SMTP", "Sohu.com", "SolarEdge Technologies", "Solarwinds", "Solera Holdings", "Sonic Foundry", "Sonus Networks", "SouFun Holdings", "Sparton", "Speed Commerce", "Sphere 3D", "Splunk", "SPS Commerce", "SPX", "SS&C Technologies Holdings", "Standex International", "StarTek", "STMicroelectronics", "Stratasys", "Streamline Health Solutions", "SunEdison Semiconductor", "SunEdison", "Sungy Mobile", "SunPower", "Super Micro Computer", "SuperCom", "Superconductor Technologies", "support.com", "Sykes Enterprises", "Symantec", "Synacor", "Synaptics", "Synchronoss Technologies", "Synnex", "Synopsys", "Syntel", "Sysorex Global Holding", "Tableau Software", "Taiwan Semiconductor Manufacturing Company", "Take-Two Interactive Software", "TAL International Group", "Tangoe", "Team Health Holdings", "Tech Data", "Technical Communications", "TeleCommunication Systems", "TeleTech Holdings", "Tennant Company", "Teradata", "Tessera Technologies", "Texas Instruments", "Textainer Group Holdings", "Textura", "The Descartes Systems Group", "The KEYW Holding", "The Middleby", "The Rubicon Project", "The Ultimate Software Group", "TigerLogic", "Top Image Systems", "Tower Semiconductor", "TransAct Technologies", "Travelzoo", "Tremor Video", "Trina Solar", "Trio-Tech International", "TripAdvisor", "TrueBlue", "TrueCar", "TSR", "TTM Technologies", "TubeMogul", "Tucows", "Twin", "Twitter", "Tyler Technologies", "UBIC", "Ubiquiti Networks", "Ultra Clean Holdings", "Ultratech", "Unisys", "United Microelectronics", "United Online", "United Rentals", "Unwired Planet", "Upland Software", "Varonis Systems", "VASCO Data Security International", "Veeco Instruments", "Veeva Systems", "Verint Systems", "VeriSign", "Verisk Analytics", "ViaSat", "Viggle", "Vimicro International", "Violin Memory", "Virtusa", "VisionChina Media", "Vmware", "Volt Information Sciences", "Vuzix", "Wave Systems", "Wayside Technology Group", "Web.com Group", "Weibo", "Western Digital", "WidePoint", "Wipro", "Wix.com", "Workday", "Workiva", "Wowo", "WPP", "WSI Industries", "Xilinx", "Xplore Technologies", "Xunlei", "Yahoo", "Yandex", "Yingli Green Energy Holding Company", "Yodlee", "Youku Tudou", "YuMe", "YY", "Zebra Technologies", "Zendesk", "Zhaopin", "Zix", "Zynga"]
	resume_list = []
	masterListUrls = set()
	# rs = (grequests.get)
	# results = pool.map(ResumeDownloader, company_list_2)
	for company_name in company_list_2:
		resume_list.append(ResumeDownloader(company_name))

	for stuff in resume_list:
		for individual in stuff:
			masterListUrls.update(individual)

	f = open('ResumeList6.txt', 'w')
	for resume in masterListUrls:
		f.write(resume)
		f.write('\n')
	f.close()
	# print len(results)
	# print len(results)
	# for link in results:
	# 	for values in link:
	# 		for cv in values:
	# 			print cv
	# f = open('resumes.txt', 'w')
	# for stuff in resumes:
	# 	f.write(stuff)
	# 	f.write('\n')
	# f.close()



# main()
get_resumes('http://www.indeed.com/resumes/21vianetgroup?co=US&start=50')



