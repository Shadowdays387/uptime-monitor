import requests
import time
import json
from datetime import datetime
from colorama import init,Fore,Style
init()

#логирруем
def write_log(line):
    with open("monitor.log", "a") as f:
        f.write(line + "\n")

#формат для логов:
def format_status(site, ok, code=None, ms=None, error=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ok:
        return f"{timestamp} | [OK] {site} | {code} | {ms:.0f}ms"
    else:
        return f"{timestamp} | [FAIL] {site} | {error}"
#Вывод цвета в консоли
def colorize(line):
    if "[OK]" in line:
        return line.replace(
            "[OK]",
            f"{Fore.GREEN}[OK]{Style.RESET_ALL}"
        )

    if "[FAIL]" in line:
        return line.replace(
            "[FAIL]",
            f"{Fore.RED}[FAIL]{Style.RESET_ALL}"
        )

    return line
def colorize_ms(ms):
    if ms < 500:
        return Fore.GREEN
    elif ms < 1000:
        return Fore.YELLOW
    else:
        return Fore.RED
#даём список сайтов
with open("sites.json","r") as f:
	sites = json.load(f)
#Старый способ, сайты не в конфиге:
#sites = [
#    "https://google.com",
#    "https://github.com",
#    "https://abrakadabra-super-site-123456.com"
#]

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
        #       duration = end - start
        #переводим мс в с
        #       ms = duration * 1000
                        ms = (end-start) * 1000

#Вывод в одну строку и логирруем
                        log_line = format_status(
                                site,
                                ok=response.ok,
                                code=response.status_code,
                                ms=ms
                        )
                        console_line = colorize(log_line)
                        ms_color = colorize_ms(ms)
                        console_line = console_line.replace(
                            f"{ms:.0f}ms",
                            f"{ms_color}{ms:.0f}ms{Style.RESET_ALL}"
                            )
                        print(console_line)
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
