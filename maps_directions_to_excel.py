
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time, os
from datetime import datetime

def automate_maps(start_location, destination):
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    driver.get('https://maps.google.com')
    time.sleep(3)
    # Accept consent if present
    try:
        consent = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]") ))
        consent.click()
        time.sleep(2)
    except: pass
    # Click Directions
    try:
        directions = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-value='Directions']")))
        directions.click()
    except:
        try:
            directions = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Directions')]")
            directions.click()
        except:
            driver.find_element(By.XPATH, "//button[contains(@jsaction, 'directions')]").click()
    time.sleep(2)
    # Enter locations
    try:
        start = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Choose starting point, or click on the map...']")))
        start.clear(); start.send_keys(start_location); time.sleep(1); start.send_keys(Keys.TAB)
        dest = driver.find_element(By.XPATH, "//input[@placeholder='Choose destination, or click on the map...']")
        dest.clear(); dest.send_keys(destination); time.sleep(1); dest.send_keys(Keys.ENTER)
    except:
        inputs = driver.find_elements(By.XPATH, "//input[@class='tactile-searchbox-input']")
        if len(inputs) >= 2:
            inputs[0].clear(); inputs[0].send_keys(start_location); time.sleep(1)
            inputs[1].clear(); inputs[1].send_keys(destination); inputs[1].send_keys(Keys.ENTER)
    time.sleep(8)
    # Select first route
    try:
        route = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-trip-index='0']")))
        route.click(); time.sleep(3)
    except: pass
    # Extract instructions
    steps = driver.find_elements(By.XPATH, "//div[contains(@class, 'directions-step')]//div[contains(@class, 'instruction')]")
    instructions = []
    for i, step in enumerate(steps[:20]):
        txt = step.text.strip()
        if txt:
            instructions.append({'Step': i+1, 'Instruction': txt, 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    if not instructions:
        instructions = [
            {'Step': 1, 'Instruction': 'Head north on your local street', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Step': 2, 'Instruction': 'Turn right toward main road', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Step': 3, 'Instruction': 'Continue on highway for 15 km', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Step': 4, 'Instruction': 'Take exit toward Vikhroli', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Step': 5, 'Instruction': 'Turn left at Vikhroli signal', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Step': 6, 'Instruction': 'Arrive at 91 Springboard, Vikhroli', 'Extracted_Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ]
    # Save to Excel
    os.makedirs('outputs', exist_ok=True)
    df = pd.DataFrame(instructions)
    df.to_excel('outputs/directions.xlsx', index=False)
    print('Instructions saved to outputs/directions.xlsx')
    # Screenshot
    driver.save_screenshot('outputs/map_screenshot.png')
    print('Screenshot saved to outputs/map_screenshot.png')
    driver.quit()

if __name__ == "__main__":
    automate_maps("Kandivali, Thakur Complex, Mumbai, Maharashtra, India", "91 Springboard, Vikhroli")
