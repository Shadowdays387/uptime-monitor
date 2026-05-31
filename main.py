import requests
import time
from datetime import datetime

#логирруем
def write_log(line):
    with open("monitor.log", "a") as f:
        f.write(line + "\n")

#формат приводим в норму:
def format_status(site, ok, code=None, ms=None, error=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ok:
        return f"{timestamp} | [OK] {site} | {code} | {ms:.0f}ms"
    else:
        return f"{timestamp} | [FAIL] {site} | {error}"
#даём список сайтов
sites = [
    "https://google.com",
    "https://github.com",
    "https://abrakadabra-super-site-123456.com"
]

ok_count = 0
fail_count = 0
total_count = 0
#цикл повтора
while True:
#говорим чего делаем с сайтами
	for site in sites:	
#исключаем падение из-за несуществущего хоста
		try:
	#таймер вкл
			total_count += 1
			start = time.time() 
			response = requests.get(site,timeout = 5)

			if response.status_code == 200:
				ok_count += 1
			else:
				 fail_count += 1
	#таймер выкл
			end = time.time()
	#считаем разницу 
	#	duration = end - start
	#переводим мс в с
	#	ms = duration * 1000
			ms = (end-start) * 1000
		
#Вывод в одну строку и логирруем
			log_line = format_status(
        			site,
        			ok=response.ok,
        			code=response.status_code,
        			ms=ms
			)

			print(log_line)
			write_log(log_line)
#status logic(не исползуется уже)
		#if response.status_code == 200:
			#status = "OK"
		#else: 
			#status = "FAIL"
#выводим статус код
		#print(response.status_code)
#проверяем ок ли?
		#print(response.ok)
#считаем время ответа
		#print(response.elapsed)
#выводим урл ответа
		#print(response.url)

#исключаем ошибку
		except requests.exceptions.Timeout:
			log_line = f"[FAIL] {site} | TIMEOUT"
			print(log_line)
			write_log(log_line)
			fail_count += 1
		except requests.exceptions.ConnectionError:
			log_line = f"[FAIL] {site} | CONNECTION"
			print(log_line)
			write_log(log_line)
			fail_count += 1
#Считаем уптиме
	if total_count == 0:
		uptime = 0
	else:
		uptime = (ok_count / total_count) * 100
#Саммари и спать
	print(f"SUMMARY | UPTIME: {uptime:.1f}% | OK={ok_count} | FAIL={fail_count}")
	
	time.sleep(10)	
