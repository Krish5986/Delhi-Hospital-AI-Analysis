import time 
import pandas as pd 
import re 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

# Configuration 
TARGET_REVIEWS_PER_HOSPITAL = 50

#Map of hospital names to their google maps reviews URLS 
Hospitals = {
    #Govt. Hospital
    "Safdarjung_Gov": "https://www.google.com/maps/place/VMMC+%26+Safdarjung+Hospital/@28.5672666,77.2025172,17z/data=!4m12!1m2!2m1!1ssafdarjung+hospital!3m8!1s0x390ce27b1527eb57:0xf71af9b11f97c064!8m2!3d28.5680405!4d77.2058155!9m1!1b1!15sChNzYWZkYXJqdW5nIGhvc3BpdGFsWhUiE3NhZmRhcmp1bmcgaG9zcGl0YWySARNnb3Zlcm5tZW50X2hvc3BpdGFs4AEA!16zL20vMGNtbnB2?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",
    "AIIMS_Gov": "https://www.google.com/maps/place/All+India+Institute+Of+Medical+Sciences+Delhi/@28.5671937,77.2102608,17z/data=!3m1!5s0x390ce26f67cd27fb:0xb9a86927f863f7c5!4m8!3m7!1s0x390ce26f903969d7:0x8367180c6de2ecc2!8m2!3d28.5671937!4d77.2102608!9m1!1b1!16s%2Fm%2F0lq5p3v?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",
    "RML_Gov" :"https://www.google.com/maps/place/Dr.+Ram+Manohar+Lohia+Hospital/@28.625857,77.2005083,17z/data=!4m12!1m2!2m1!1srml+govt+hospital!3m8!1s0x390cfd54897b42ab:0xaba569ad339668ef!8m2!3d28.625857!4d77.202697!9m1!1b1!15sChFybWwgZ292dCBob3NwaXRhbFoTIhFybWwgZ292dCBob3NwaXRhbJIBE2dvdmVybm1lbnRfaG9zcGl0YWzgAQA!16s%2Fm%2F02qpsfy?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",

    #Pvt Hosptial
    "Max_Pvt": "https://www.google.com/maps/place/Max+Super+Speciality+Hospital,+Saket+(Max+Saket)/@28.527549,77.1944851,14z/data=!4m12!1m2!2m1!1smax+hospital!3m8!1s0x390ce1f427d4c5fb:0x582d47bbf4970bc1!8m2!3d28.527549!4d77.2119946!9m1!1b1!15sCgxtYXggaG9zcGl0YWwiA4gBAVoOIgxtYXggaG9zcGl0YWySAQhob3NwaXRhbOABAA!16s%2Fm%2F0nhgv9_?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",
    "Apollow_Pvt" : "https://www.google.com/maps/place/Indraprastha+Apollo+Hospital+%7C+Best+Hospital+in+Delhi/@28.5406218,77.2805208,17z/data=!4m8!3m7!1s0x390ce6ad13eaaa99:0x3bc07ad476bc6d77!8m2!3d28.5406218!4d77.2830957!9m1!1b1!16s%2Fg%2F1tnpjcxm?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",
    "Fortis_Okhla_vPt" : "https://www.google.com/maps/place/Fortis+Escorts+Heart+Institute+-+Heart+Hospital+Okhla/@28.5606267,77.2737176,17z/data=!4m8!3m7!1s0x390ce392b869bbaf:0x865db71ba6f271b2!8m2!3d28.5606267!4d77.2737176!9m1!1b1!16s%2Fg%2F1tyzxc62?entry=ttu&g_ep=EgoyMDI2MDIxMS4wIKXMDSoASAFQAw%3D%3D",
}

def setup_driver():
    options = Options()
    #options.add_argument("Headless") #Keep this commented to see the browser
    options.add_argument("--lang=en")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    return driver 

def scrape_hospital(driver,name,url):
    print(f"--- Starting {name} ---")
    driver.get(url)
    time.sleep(6) #wait for inital load

    try:
        reviews_tab = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Reviews')]")
        reviews_tab.click()
        print("  (Clicked 'Reviews' tab sucessfully)")
        time.sleep(4)
    except Exception as e:
        print(f" (Could not click 'Reviews' tab - assuming already open or failed. Error: {e})")

    reviews_data = []
    processed_texts = set()
    last_count = 0
    consecutive_no_new_reviews = 0

    

    while len(reviews_data) < TARGET_REVIEWS_PER_HOSPITAL:
        #Scroll logic
        try:
            #find all reviews blocks 
            elements = driver.find_elements(By.CLASS_NAME,'jftiEf')
            if elements:
            #scroll the last element into view 
                driver.execute_script("arguments[0].scrollIntoView(true);",elements[-1])
                time.sleep(2.5) 
                      
            else:
                #fall back if no reviews found yet
                scrollable_div = driver.find_element(By.XPATH,"//div[contains(@aria-label,'Reviews for')]")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",scrollable_div)
                time.sleep(2.5)
        except Exception:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        #Extract Data
        elements = driver.find_elements(By.CLASS_NAME,'jftiEf')
        for elem in elements:
            if len(reviews_data) >= TARGET_REVIEWS_PER_HOSPITAL:
                break

            try:
                #Extract Date
                date_elem = elem.find_element(By.CLASS_NAME,'rsqaWe').text

                #1. Extract Text
                try:
                    text_elem = elem.find_element(By.CLASS_NAME,'wiI7pd').text
                except:
                    text_elem = "" #star rating only no text

                #Use Date + Text as unique ID to avoid duplicates 
                unique_id = f"{date_elem}_{text_elem[:30]}"

                if unique_id not in processed_texts:
                    processed_texts.add(unique_id)
                    reviews_data.append({
                        "Hospital" :name,
                        "Type" : "Government" if "Gov" in name else "Private",
                        "Review_Date": date_elem,
                        "Review_Text" : text_elem,
                    })
            except (StaleElementReferenceException,Exception):
                continue
        
        #Stuck Check 
        if len(reviews_data) == last_count:
            consecutive_no_new_reviews +=1
            print(f"   ...waiting for more reviews ({len(reviews_data)} collected)")
            #if stuck try scrolling up a bith then down to "wake up" the loader
            driver.execute_script("window.scrollBy(0,-300);")
        else:
            consecutive_no_new_reviews = 0
            print(f"  Progress: {len(reviews_data)}/{TARGET_REVIEWS_PER_HOSPITAL}")
        last_count = len(reviews_data)

        if consecutive_no_new_reviews > 8:
            print(f"Reached end of available reviews for {name}.")
            break

    return reviews_data

# MAIN EXECUTION
if __name__ == "__main__":
    driver = setup_driver()
    all_data = []

    for name, url in Hospitals.items():
        if "PASTE" in url:
            print(f"Warning: Please replace placeholder URL for {name} with a real Google Maps Link.")
        try:
            data = scrape_hospital(driver,name,url)
            all_data.extend(data)
        except Exception as e:
             print(f"Error scrapping {name}: {e}")

    driver.quit()

    if all_data:
        df = pd.DataFrame(all_data)
        filename = "delhi_hospital_reviews.csv"
        df.to_csv(filename,index=False)
        print(f"SUCCESS! Data saved to '{filename}'")
        print(df["Hospital"].value_counts())

    else:
        print("No data collected.")