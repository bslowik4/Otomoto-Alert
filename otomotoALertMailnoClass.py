import json
import requests
from bs4 import BeautifulSoup
import smtplib

def load_config():
    with open('config.json') as f:
        return json.load(f)

config = load_config()
url = "https://www.otomoto.pl/osobowe/od-2006/tarnow?search%5Bdist%5D=100&search%5Bfilter_enum_fuel_type%5D=petrol-lpg&search%5Bfilter_float_price%3Afrom%5D=5000&search%5Bfilter_float_price%3Ato%5D=10500&search%5Border%5D=created_at_first%3Adesc"

def extract_number_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.find_all('p')
    
    for paragraph in paragraphs:
        if "Liczba ogłoszeń:" in paragraph.get_text(strip=True):
            bold_tag = paragraph.find('b')
            if bold_tag and bold_tag.text.strip().isdigit():
                return int(bold_tag.text.strip())
    
    return None

def send_email(subject, body, to_email):
    from_email = config["EMAIL_USER"]
    password = config["EMAIL_PASSWORD"]
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_email, to_email, message)

def ensure_file_exists(filename):
    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            file.write("")

ensure_file_exists("website_number.txt")

try:
    with open("website_number.txt", "r") as file:
        old_number = int(file.read().strip())
except FileNotFoundError:
    old_number = None

current_content = requests.get(url).text

new_number = extract_number_from_content(current_content)

if new_number is not None:
    print(f"Current number of offers: {new_number}")
    
    if new_number != old_number:
        with open("website_number.txt", "w") as file:
            file.write(str(new_number))

        subject = "Website Number Changed"
        body = f"The number in 'Liczba ogłoszeń:' has changed to {new_number} on {url}."
        send_email(subject, body, config["EMAIL_USER"])

        print(f"The number in 'Liczba ogłoszeń:' has changed to {new_number}. Email sent!")
    else:
        print("No changes detected.")
else:
    print("Failed to extract the number of offers.")
