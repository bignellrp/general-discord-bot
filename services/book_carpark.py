# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# import time
# from datetime import datetime, timedelta
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
# import os
# from selenium_stealth import stealth
# import base64
# import discord

# from dotenv import load_dotenv

# # Load values from .env
# load_dotenv()

# car = os.getenv("CAR")
# name = os.getenv("FIRSTNAME")
# surname = os.getenv("SURNAME")
# emailsan = os.getenv("WORKEMAIL")
# fromemail = os.getenv("FROMEMAIL")
# toemail = os.getenv("TOEMAIL")
# key = os.getenv("APIKEY")

# def discordmessage(status, spaces, booking):
#     try:
#         entry_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
#         ##Send Rerun message to discord
#         url = os.getenv("DISCORD_WEBHOOK")
#         webhook = discord.Webhook.from_url(url, 
#                                         adapter=discord.RequestsWebhookAdapter())
#         ##Embed Message
#         embed=discord.Embed(title="Unity place car park for {} - {}".format(entry_date, status),
#                             color=discord.Color.dark_green())
#         embed.set_author(name="general-bot")
#         embed.set_footer(text="{} \n {} \n Car: {}".format(booking, spaces, car))
#         webhook.send(embed = embed)
#     except Exception as e:
#         print(e.message)

# def sendmail(status, spaces, booking):
#     entry_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
#     sendgrid_api_key = key
#     sender_email = fromemail
#     receiver_email = toemail
#     subject = "Unity place car park for {} - {}".format(entry_date, status)
#     content = "{} \n {} \n Car: {}".format(booking, spaces, car)

#     # Create the email message
#     message = Mail(
#         from_email=sender_email,
#         to_emails=receiver_email,
#         subject=subject,
#         plain_text_content=content)

#     try:
#         # Check and attach any of the PNG files that exist
#         for png_file in ['ok.png', 'error.png', 'remaining.png']:
#             if os.path.exists(png_file) and os.path.getsize(png_file) > 0:
#                 with open(png_file, 'rb') as f:
#                     file_data = f.read()
#                     file_base64 = base64.b64encode(file_data).decode()
                
#                 attachment = Attachment(
#                     FileContent(file_base64),
#                     FileName(png_file),
#                     FileType('image/png'),
#                     Disposition('attachment')
#                 )
#                 message.attachment = attachment

#         # Send the email whether or not there were attachments
#         sg = SendGridAPIClient(sendgrid_api_key)
#         sg.send(message)

#         # After successful send, delete any of the PNG files that exist
#         for png_file in ['ok.png', 'error.png', 'remaining.png']:
#             if os.path.exists(png_file):
#                 os.remove(png_file)
#     except Exception as e:
#         print(e.message)

# def bookcarpark():
#     try:
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         # adding argument to disable the AutomationControlled flag
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         # exclude the collection of enable-automation switches
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         # turn-off userAutomationExtension
#         options.add_experimental_option("useAutomationExtension", False)
#         # disable pop-up blocking
#         options.add_argument('--disable-popup-blocking')
#         # start the browser window in maximized mode
#         options.add_argument('--start-maximized')
#         # disable extensions
#         options.add_argument('--disable-extensions')
#         browser = webdriver.Chrome(options=options)
#         # changing the property of the navigator value for webdriver to undefined
#         browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#         # enable stealth mode
#         stealth(browser,
#                 languages=["en-US", "en"],
#                 vendor="Google Inc.",
#                 platform="Win32",
#                 webgl_vendor="Intel Inc.",
#                 renderer="Intel Iris OpenGL Engine",
#                 fix_hairline=True,
#                 )
#         browser.get("https://unityplace.aeroparker.com/book/Santander/Parking?parkingCmd=collectParkingDetails")

#         today = datetime.now()
#         tomorrow = today + timedelta(days=1)
#         day_after_tomorrow = today + timedelta(days=2)
#         new_entry_date = tomorrow.strftime('%d/%m/%Y')
#         new_exit_date = day_after_tomorrow.strftime('%d/%m/%Y')

#         #### SELECT DATE
#         entry_date_input = browser.find_element(By.ID, "changeEntryDate")
#         exit_date_input = browser.find_element(By.ID, "changeExitDate")
#         entry_time_input = browser.find_element(By.ID, "changeEntryTime")
#         exit_time_input = browser.find_element(By.ID, "changeExitTime")

#         browser.execute_script("arguments[0].removeAttribute('readonly')", entry_date_input)
#         browser.execute_script("arguments[0].removeAttribute('readonly')", exit_date_input)
#         entry_date_input.clear()
#         exit_date_input.clear()
#         entry_date_input.send_keys(new_entry_date)
#         exit_date_input.send_keys(new_entry_date)
#         select_entry = Select(entry_time_input)
#         select_exit = Select(exit_time_input)
#         select_entry.select_by_value('06:00')
#         select_exit.select_by_value('19:00')

#         button = browser.find_elements(By.CLASS_NAME, "btn-desktop")[0]
#         button.click()

#         #### SELECT PARKING
#         browser.execute_script("document.body.style.zoom='50%'")
#         browser.save_screenshot('remaining.png')
#         browser.execute_script("document.body.style.zoom='100%'")
#         partial_href_value = "pid=413"
#         link = browser.find_element(By.XPATH, f"//a[contains(@href, '{partial_href_value}')]")
#         spaces_element = browser.find_element(By.CLASS_NAME, 'item__alert')
#         spaces_text = spaces_element.text
#         link.click()

#         # ### ENTER DETAILS
#         print ("Entering details")
#         input_field = browser.find_element(By.ID, "firstName")
#         input_field.send_keys(name)
#         input_field = browser.find_element(By.ID, "lastName")
#         input_field.send_keys(surname)
#         checkbox = browser.find_element(By.ID, "terms")
#         checkbox.send_keys(Keys.SPACE)
#         input_field = browser.find_element(By.ID, "email")
#         input_field.send_keys(emailsan)
#         input_field = browser.find_element(By.ID, "registration")
#         input_field.send_keys(car)
#         time.sleep(2)
#         input_field.send_keys(car)
#         buttonval = browser.find_element(By.ID, 'validationButton')
#         buttonval.click()
#         buttonval.click()
#         time.sleep(2)
#         button = browser.find_element(By.ID, "PaymentFormSubmit")
#         button.click()
#         button.click()
#         browser.save_screenshot('ok.png')
#         booking_element = browser.find_element(By.CLASS_NAME, 'confirmation__title')
#         booking_text = booking_element.text
#         discordmessage('Success', spaces_text, booking_text)
#         sendmail('Success', spaces_text, booking_text)
#     except:
#         try:
#             browser.find_element(By.CLASS_NAME, 'confirmation__title')
#             booking_element = browser.find_element(By.CLASS_NAME, 'confirmation__title')
#             booking_text = booking_element.text
#             discordmessage('Success', spaces_text, booking_text)
#             sendmail('Success', spaces_text, booking_text)
#         except:
#             browser.execute_script("document.body.style.zoom='50%'")
#             browser.save_screenshot('error.png')
#             discordmessage('Error', '', '')
#             sendmail('Error', '', '')
#     browser.close()