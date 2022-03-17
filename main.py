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

# Find descripción actividad field of today
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

# Print today
## TODO: Print all week
print("\n\n\nHoy es " + weekday + "\n")

pretty = PrettyTable()
pretty._max_width = {"Descripción Actividad":30}
pretty.field_names = ["Descripción Actividad", "Orientaciones", "Observaciones", "Horas"]

celda1 = driver.find_element(By.XPATH,'//div[@id="diario'+get_weekday_number()+'"]/table/tbody/tr[2]/td[1]').text
celda2 = driver.find_element(By.XPATH,'//div[@id="diario'+get_weekday_number()+'"]/table/tbody/tr[2]/td[2]').text
celda3 = driver.find_element(By.XPATH,'//div[@id="diario'+get_weekday_number()+'"]/table/tbody/tr[2]/td[3]').text
celda4 = driver.find_element(By.XPATH,'//div[@id="diario'+get_weekday_number()+'"]/table/tbody/tr[2]/td[4]').text

pretty.add_row([celda1,celda2,celda3,celda4])
print(pretty)

# Find today's modify button
today_p = driver.find_element(By.XPATH,'//span[text()="'+weekday+'"]/preceding-sibling::a/img')
today_p.click()

time.sleep(3)

# Send Descripción Actividad
descripcion_actividad = driver.find_element(By.XPATH,'//textarea[@id="descripcion' + get_weekday_number() + '"]')
eleccion = input("¿Quieres modificar el campo Descripción Actividad? (s/N): ").lower()
if eleccion == "s":
    descripcion_actividad.clear()
    descripcion_actividad_input = input("\n¿Qué has hecho hoy?: \n")
    descripcion_actividad.send_keys(descripcion_actividad_input)

# Send Horas
horas_object = driver.find_element(By.XPATH,'//input[@id="tiempo' + get_weekday_number() + '"]')
horas_object.clear()
horas_input = int(input("\n¿Cuántas horas has hecho hoy? - [Por defecto: 8] \n") or "8")
horas_object.send_keys(horas_input)

# Click send
send_button = driver.find_element(By.XPATH,'//img[@src="img/aceptar.png"]')
send_button.click()

# Show remaining hours
driver.refresh()
time.sleep(2)
horas = driver.find_element(By.XPATH,'//*[@id="contenedorDetallesFCT"]/table/tbody/tr[14]/td[4]').text
print("\n\nLlevas\t" + horas + " te quedan")

# Log out
logout_button = driver.find_element(By.CSS_SELECTOR,"input[name='logout']")
logout_button.click()

driver.close()
