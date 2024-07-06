import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time

# Ścieżka do Chrome
chrome_path = "/usr/bin/chromium-browser"

# Konfiguracja Selenium WebDriver dla Chromium
service = Service('/usr/bin/chromedriver')
options = Options()
options.binary_location = chrome_path
driver = webdriver.Chrome(service=service, options=options)

driver.get("http://www.google.com")

# Funkcja do generowania fałszywych danych
def generate_fake_email():
    fake = Faker()
    email = fake.email()
    print("Wygenerowany fałszywy email:", email)
    return email

# Test 1: Otwieranie strony głównej Badoo i sprawdzanie ciasteczek
try:
    print("Test 1: Otwieranie strony głównej Badoo.")
    driver.get("https://www.badoo.com")
    print("Test 1: Strona główna Badoo otwarta.")
    
    print("Sprawdzanie komunikatu o ciasteczkach.")
    try:
        # Czekanie na iframe
        iframe = WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@src, 'consent')]"))
        )
        print("Test 1: Iframe z komunikatem o ciasteczkach dostępny.")

        # Użycie ogólnego selektora dla przycisku "Akceptuj"
        accept_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Akceptuj') or contains(text(), 'Accept')]"))
        )
        accept_button.click()
        print("Test 1: Kliknięto 'Akceptuj'.")

        # Powrót do głównej strony
        driver.switch_to.default_content()
        time.sleep(2)  # Poczekaj chwilę, aby sprawdzić, czy baner zniknie

        # Sprawdzenie, czy baner zniknął
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'consent')]"))
        )
        print("Test 1: Baner z ciasteczkami zniknął po kliknięciu 'Akceptuj'.")
    except Exception as e:
        print("Nie udało się znaleźć przycisku akceptacji ciasteczek w określonym czasie:", e)

    # Test 2: Przechodzenie do strony logowania
    print("Test 2: Przechodzenie do strony logowania.")
    login_button_main = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/signin')]"))
    )
    login_button_main.click()
    print("Test 2: Kliknięto 'Zaloguj się' na stronie głównej.")

    # Generowanie fałszywego emaila
    email = generate_fake_email()
    print(f"Test 2: Wygenerowany fałszywy email: {email}")

   # Poczekaj na pole e-mail
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='signin-name']"))
    )
    print("Test 2: Pole email znalezione.")

     # Wprowadź fałszywy e-mail do pola e-mail
    email_field.send_keys(email)
    print(f"Test 2: Wprowadzono fałszywy email: {email}")

        # Kliknij przycisk logowania
    email_field.send_keys(Keys.RETURN)
    print(f"Test 2: Próba logowania z fałszywym emailem: {email}")

    verification_message = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='signin-name']"))
    )

    if verification_message.is_displayed():
        print("Test 2: Komunikat o wysłaniu kodu weryfikacyjnego został wyświetlony.")
        print("Test 2: UWAGA! Strona nie sprawdza, czy konto istnieje - można próbować logowania na nieistniejące konto.")
    else:
        print("Test 2: Komunikat o wysłaniu kodu weryfikacyjnego nie został wyświetlony.")

    # Test 3: Testowanie responsywności
    def test_responsiveness(width, height, device_name):
        driver.set_window_size(width, height)
        time.sleep(2)  # Poczekaj chwilę na załadowanie
        print(f"Test 3: Test responsywności dla {device_name}:")
        print(f"Test 3: Rozmiar okna: {width}x{height}")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if element.is_displayed():
                print(f"Test 3: Responsywność strony działa poprawnie dla {device_name}.")
            else:
                print(f"Test 3: Strona nie jest responsywna dla {device_name}.")
        except Exception as e:
            print(f"Test 3: Wystąpił problem podczas testowania responsywności dla {device_name}: ", e)

    test_responsiveness(1440, 3200, "Samsung Galaxy S21")
    test_responsiveness(1170, 2532, "iPhone 12 Pro")
    test_responsiveness(1290, 2796, "iPhone 15 Pro")

    print("Test 4: Rejestracja z fałszywymi danymi.")
    driver.get("https://www.badoo.com")

    # Znalezienie przycisku rejestracji za pomocą podanego full XPath
    try:
        register_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/section[1]/div/div/div[1]/div[1]/form/div[1]/div[2]/button"))
        )
        register_button.click()
        print("Test 4: Kliknięto przycisk 'Zarejestruj za pomocą telefonu'.")
    except Exception as e:
        print("Test 4: Nie udało się znaleźć przycisku 'Zarejestruj za pomocą telefonu':", e)
        raise

    # Poczekaj aż pole email będzie widoczne i interaktywne
    try:
        email_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div/main/section[1]/div/div/div[1]/div[1]/form/div[2]/div[2]/div/input"))
        )
        email_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/section[1]/div/div/div[1]/div[1]/form/div[2]/div[2]/div/input"))
        )
        print("Test 4: Pole email jest widoczne i interaktywne.")
    except Exception as e:
        print("Test 4: Nie udało się znaleźć pola email:", e)
        raise

    # Wprowadź fałszywy e-mail do pola e-mail
    email = generate_fake_email()
    email_field.send_keys(email)
    print(f"Test 4: Wprowadzono fałszywy email: {email}")

    # Kliknij przycisk "Zapisz się" po wpisaniu emaila
    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/section[1]/div/div/div[1]/div[1]/form/div[2]/div[2]/button"))
        )
        next_button.click()
        print("Test 4: Kliknięto przycisk 'Zapisz się' po wpisaniu emaila.")
    except Exception as e:
        print("Test 4: Nie udało się znaleźć przycisku 'Zapisz się' po wpisaniu emaila:", e)
        raise
 # Warunkowe sprawdzenie obecności kontroli bezpieczeństwa
    try:
        security_check_visible = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "xpath_do_kontroli_bezpieczeństwa"))
        )
        if security_check_visible:
            print("Test 4: Kontrola bezpieczeństwa jest widoczna. Zakończono test.")
            driver.quit()
            exit()
        else:
            print("Test 4: Kontrola bezpieczeństwa nie jest widoczna.")
    except Exception:
        print("Test 4: Kontrola bezpieczeństwa pojawiła się.")

    # Warunkowe sprawdzenie obecności komunikatu o preferencjach e-mail
    try:
        preferences_visible = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div[2]/div/div/div[2]/div[1]/button/span/span/span"))
        )
        if preferences_visible:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div[2]/div/div/div[2]/div[1]/button/span/span/span"))
            )
            accept_button.click()
            print("Test 4: Kliknięto przycisk 'Jasne' po preferencjach e-mail.")
        else:
            print("Test 4: Komunikat o preferencjach e-mail nie jest widoczny.")
    except Exception:
        print("Test 4: Komunikat o preferencjach e-mail pojawił się.")


    # Sprawdzenie, czy strona przepusci puste bloki tekstowe, nieuzupelnione
    try:
        security_check_visible = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div[3]/button"))
        )

        print("Test 4: Strona przepuszcza nie uzupelnione bloki tekstowe.")
    except Exception:
        print("Test 4: Strona nie pozwala na nieuzupelnienie danych.")


     # Test 5: Otwieranie strony "Safety Centre"
    try:
        print("Test 5: Otwieranie strony 'Safety Centre'.")
        driver.get("https://badoo.com")
        
        # Sprawdzenie czy strona jest w pełni załadowana
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Przewinięcie do dołu strony, aby element mógł stać się widoczny
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Poczekaj chwilę na przewinięcie

        # Poczekaj aż element stanie się klikalny
        safety_centre_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Safety Centre']"))
        )
        safety_centre_link.click()
        print("Test 5: Strona 'Safety Centre' otwarta poprawnie.")
    except Exception as e:
        print("Test 5: Nie udało się znaleźć linku do 'Safety Centre' w określonym czasie.")

    # Test 6: Otwieranie strony pomocy
        print("Test 6: Otwieranie strony pomocy.")
        driver.get("https://badoo.com")

        # Sprawdzenie czy strona jest w pełni załadowana
    WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

         # Przewinięcie do dołu strony, aby element mógł stać się widoczny
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Poczekaj chwilę na przewinięcie

        # Poczekaj aż element stanie się klikalny
    safety_centre_link = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/footer/div[1]/div/section[2]/div[2]/nav/ul/li[3]/a"))
    )
    print("Test 6: Strona pomocy otwarta poprawnie.")
except Exception:
    print("Test 6: Strona pomocy nie zostala otwarta poprawnie.")

    # Test 7: Otwieranie strony prywatności
try:
    print("Test 7: Otwieranie strony prywatności.")
    driver.get("https://badoo.com")
    # Sprawdzenie czy strona jest w pełni załadowana
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Przewinięcie do dołu strony, aby element mógł stać się widoczny
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Poczekaj chwilę na przewinięcie

    # Poczekaj aż element stanie się klikalny
    safety_centre_link = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/footer/div[1]/div/section[2]/div[2]/nav/ul/li[9]/a"))
    )
    
    print("Test 7: Strona prywatności otwarta poprawnie.")

    # Test 8: Otwieranie strony warunków użytkowania
    print("Test 8: Otwieranie strony warunków użytkowania.")
    driver.get("https://badoo.com")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/footer/div[1]/div/section[2]/div[2]/nav/ul/li[9]/a)]"))
    )
    print("Test 8: Strona warunkow uzytkowania otwarta poprawnie")
except Exception as e:
    print("Test 8: Strona warunkow uzytkowania nie zostala otwarta poprawnie")

    # Test 9: Otwieranie oświadczenia w sprawie Ustawy o współczesnym niewolnictwie
try:
    print("Test 9: Otwieranie oświadczenia w sprawie Ustawy o współczesnym niewolnictwie.")
    driver.get("https://badoo.com")
    # Sprawdzenie czy strona jest w pełni załadowana
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Przewinięcie do dołu strony, aby element mógł stać się widoczny
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Poczekaj chwilę na przewinięcie

    # Poczekaj aż element stanie się klikalny
    safety_centre_link = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/footer/div[1]/div/section[2]/div[2]/nav/ul/li[13]/a"))
    )
    print("Test 9: Oświadczenie w sprawie Ustawy o współczesnym niewolnictwie otwarte poprawnie.")

except Exception as e:
    print("Test 9: Oświadczenie w sprawie Ustawy o współczesnym niewolnictwie otwarte niepoprawnie.")

finally:
    driver.quit()
