import requests
from bs4 import BeautifulSoup

url = "https://www.otomoto.pl/osobowe/od-2006/tarnow?search%5Bdist%5D=100&search%5Bfilter_enum_fuel_type%5D=petrol-lpg&search%5Bfilter_float_price%3Afrom%5D=5000&search%5Bfilter_float_price%3Ato%5D=10500&search%5Border%5D=created_at_first%3Adesc"  # Replace with the actual URL

def extract_number_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all('div', class_="ooa-wgahvq e17gkxda0")
    
    for div in divs:
        paragraph = div.find('p', class_="e17gkxda2 ooa-17owgto er34gjf0")
        
        if paragraph and "Liczba ogłoszeń:" in paragraph.get_text():    
            bold_tag = paragraph.find('b')
            if bold_tag and bold_tag.text.isdigit():
                return int(bold_tag.text)
    
    return None

try:
    with open("website_number.txt", "r") as file:
        old_number = int(file.read().strip())
except FileNotFoundError:
    old_number = None

current_content = requests.get(url). 

new_number = extract_number_from_content(current_content)

if new_number is not None:
    print(f"Current number of offers: {new_number}")
    
    if new_number != old_number:
        with open("website_number.txt", "w") as file:
            file.write(str(new_number))

        print(f"The number in 'Liczba ogłoszeń:' has changed to {new_number}.")
    else:
        print("No changes detected.")
else:
    print("Failed to extract the number of offers.")
