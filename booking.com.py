from datetime import datetime, timedelta
import csv
import time
from playwright.sync_api import sync_playwright
import urllib.parse
import re
import tkinter as tk
from gui import MyApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

    # Retrieve the user inputs after the GUI has closed
    Url_of_hotel, Csv_name = app.get_user_inputs()
    print(f"Hotel Link: {Url_of_hotel}")
    print(f"Csv Name: {Csv_name}")
    def extract_and_convert_dates(url):
        parsed_url = urllib.parse.urlparse(url)# Parse the URL
        query_string = parsed_url.query
        checkin_date = None # Extract check-in and check-out dates using regex
        checkout_date = None

        checkin_match = re.search(r'checkin=([\d-]+)', query_string)
        checkout_match = re.search(r'checkout=([\d-]+)', query_string)
        if checkin_match:
            checkin_date = checkin_match.group(1)
        if checkout_match:
            checkout_date = checkout_match.group(1)
        if checkin_date and checkout_date:
            try:
                # Extract the year, month, and day parts of the dates
                checkin_year, checkin_month, checkin_day = checkin_date.split('-')
                checkout_year, checkout_month, checkout_day = checkout_date.split('-')

                month_name = {
                    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
                    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
                }
                formatted_dates = f"{checkin_day} to {checkout_day} {month_name.get(checkin_month, 'Month')} {checkin_year}"
                return formatted_dates
            except ValueError as e:
                print(f"Error extracting dates from URL: {e}")
                return "Invalid date format in URL"
        else:
            return "Check-in or check-out date not found in URL"


    def generate_future_dates(url, days_to_generate=365):
        checkin_match = re.search(r'checkin=(\d{4}-\d{2}-\d{2})', url)
        checkout_match = re.search(r'checkout=(\d{4}-\d{2}-\d{2})', url)
        if checkin_match and checkout_match:
            checkin_date_str = checkin_match.group(1)
            checkout_date_str = checkout_match.group(1)
            checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d')
            future_dates = []
            for i in range(days_to_generate):
                new_checkin_date = checkin_date + timedelta(days=i)
                new_checkout_date = checkout_date + timedelta(days=i)
                new_checkin_date_str = new_checkin_date.strftime('%Y-%m-%d')
                new_checkout_date_str = new_checkout_date.strftime('%Y-%m-%d')
                updated_url = url.replace(f'checkin={checkin_date_str}', f'checkin={new_checkin_date_str}')
                updated_url = updated_url.replace(f'checkout={checkout_date_str}', f'checkout={new_checkout_date_str}')
                future_dates.append(updated_url)
            return future_dates
        else:
            return "Checking or checkout dates not found in the URL"
    def clean_text(text):
        if text:
            return re.sub(r'\s+', ' ', text.strip())
        return "Not Found"

    # Input the url
    url = Url_of_hotel
    future_urls = generate_future_dates(url)
    # for future_url in future_urls:
    #     print(future_url)

    count = 1
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(headless=False, user_data_dir=r"C:\Users\HP\PycharmProjects\image-upload-bot\userDir")
        page = browser.new_page()
        for future_url in future_urls:
            print(f"Open Link for {count}/365 time")
            try: page.goto(future_url, timeout=0)
            except Exception as e:
                print(f"Error opening {future_url}: {e}")
                continue
            # ab ye date extract kr rha hai
            date_of_hotel = extract_and_convert_dates(future_url)
            try:
                firstroom_price = page.query_selector('(//div[@class="bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading "])[3]').text_content()
                firstroom_price = clean_text(firstroom_price)
            except:
                firstroom_price = "Not Found"
            try:
                tworooms_price = page.query_selector('(//div[@class="bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading "])[1]').text_content()
                tworooms_price = clean_text(tworooms_price)
            except:
                tworooms_price = "Not Found"
            try:
                third_rooms_price = page.query_selector('(//div[@class="bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading "])[2]').text_content()
                third_rooms_price = clean_text(third_rooms_price)
            except:
                third_rooms_price = "Not Found"
            try:
                forth_rooms_price = page.query_selector('(//div[@class="bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading "])[4]').text_content()
                forth_rooms_price = clean_text(forth_rooms_price)
            except:
                forth_rooms_price = "Not Found"
            try:
                fifth_rooms_price = page.query_selector('(//div[@class="bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading "])[5]').text_content()
                fifth_rooms_price = clean_text(fifth_rooms_price)
            except:
                fifth_rooms_price = "Not Found"
            print(f"First Room Price: {firstroom_price} - Date: {date_of_hotel} - Two Rooms Price: {tworooms_price} - Third Room Price: {third_rooms_price} - Forth Room Price: {forth_rooms_price} - Fifth Room Price: {fifth_rooms_price}")
            # save data to csv
            header = ["Date", "Room Price", "Room Price", "Room Price", "Room Price", "Room Price" "Url"]
            with open(f'{Csv_name}buh.csv', 'a+', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Check if file is empty
                    writer.writerow(header)
                writer.writerow([date_of_hotel, firstroom_price, tworooms_price, third_rooms_price, forth_rooms_price, fifth_rooms_price, future_url])
            count += 1
            time.sleep(1)


