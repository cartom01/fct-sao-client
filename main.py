# selenium for web driving
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service

service_object = Service(binary_path)

# time for pausing between navigation
import time

# A simple Python library for easily displaying tabular 
# data in a visually appealing ASCII table format
from prettytable import PrettyTable

# what day is it today
import datetime
from babel.dates import format_date, format_datetime, format_time

d = datetime.datetime.now()
weekday = format_date(d, "EEEE", locale='es').capitalize()

# stealth options (low effort)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument("--headless")
driver = webdriver.Chrome(service=service_object, options=options)

# Open the website
driver.get('https://fct.edu.gva.es/')

# Read user from file
with open('user.txt', 'r') as f:
	user_id = f.read()

# Read password from file
with open('cp.txt', 'r') as f:
	cp = f.read()

# Locate id and password
id_box = driver.find_element(By.CSS_SELECTOR,"input[name='usuario']")
pass_box = driver.find_element(By.CSS_SELECTOR,"input[name='password']")

# Send login information
id_box.send_keys(user_id)
pass_box.send_keys(cp)

# Click login
login_button = driver.find_element(By.CSS_SELECTOR,"input[name='login']")
login_button.click()

# Go to FCTs page
fcts_button = driver.find_element(By.XPATH,'//a[@href="/index.php?op=2)"]')
fcts_button.click()

def get_weekday_number():
    if weekday == "Lunes":
        return "0"
    if weekday == "Martes":
        return "1"
    if weekday == "Miércoles":
        return "2"
    if weekday == "Jueves":
        return "3"
    if weekday == "Viernes":
        return "4"

def get_number_weekday(n):
    if n == 0:
        return "Lunes"
    if n == 1:
        return "Martes"
    if n == 2:
        return "Miércoles"
    if n == 3:
        return "Jueves"
    if n == 4:
        return "Viernes"

time.sleep(3)

# Welcome
student_name = driver.find_element(By.XPATH,'//*[@id="contenedorDetallesFCT"]/table/tbody/tr[2]/td[2]').text.lower().split(" ")
print("\nHola " + student_name[0].capitalize() + "\nHoy es " + weekday + "\n")

# Print this week
print(driver.find_element(By.XPATH,'//select[@id="semanaDiario"]/option[@selected="selected"]').text)

# Print table
for i in range(0,(int(get_weekday_number())+1)):
    print(get_number_weekday(i))
    pretty = PrettyTable()
    pretty._max_width = {"Descripción Actividad":30}
    pretty.field_names = ["Descripción Actividad", "Orientaciones", "Observaciones", "Horas"]

    celda_list = []
    celdas = driver.find_elements(By.XPATH,'//div[@id="diario' + str(i) + '"]/table/tbody/tr[2]/td')
    for i in range(0,len(celdas)):
        celda_list.append(celdas[i].get_attribute('innerHTML'))

    pretty.add_row(celda_list)
    print(pretty)

eleccion_dia = input("¿Quieres modificar el día de hoy o ayer? (HOY/ayer)").lower()
if eleccion_dia == "ayer":
    weekday = get_number_weekday(int(get_weekday_number())-1)

# Find today's modify button
today_p = driver.find_element(By.XPATH,'//span[text()="'+weekday+'"]/preceding-sibling::a/img')
today_p.click()

time.sleep(3)

# Send Descripción Actividad
descripcion_actividad = driver.find_element(By.XPATH,'//textarea[@id="descripcion' + get_weekday_number() + '"]')
eleccion = input("¿Quieres modificar el campo Descripción Actividad del " + weekday + "? (s/N): ").lower()
if eleccion == "s":
    descripcion_actividad.clear()
    descripcion_actividad_input = input("\n¿Qué has hecho?: \n")
    descripcion_actividad.send_keys(descripcion_actividad_input)

# Send Horas
horas_object = driver.find_element(By.XPATH,'//input[@id="tiempo' + get_weekday_number() + '"]')
horas_object.clear()
horas_input = int(input("\n¿Cuántas horas has hecho? - [Por defecto: 8] ") or "8")
horas_object.send_keys(horas_input)

# Click send
send_button = driver.find_element(By.XPATH,'//img[@src="img/aceptar.png"]')
send_button.click()

# Show remaining hours
driver.refresh()
time.sleep(2)
horas = driver.find_element(By.XPATH,'//*[@id="contenedorDetallesFCT"]/table/tbody/tr[14]/td[4]').text.replace(" ","").split('/')
horas_restantes = int(horas[1]) - int(horas[0])
print("\n\nLlevas " + horas[0] + " horas\nTe quedan " + str(horas_restantes) + " horas\nA razón de 8 horas diarias aún te quedan " + str(horas_restantes/8) + " días")
print("\nTe quedan " + str(4 - int(get_weekday_number())) + " días para acabar la semana")

# Log out
logout_button = driver.find_element(By.CSS_SELECTOR,"input[name='logout']")
logout_button.click()

driver.close()
