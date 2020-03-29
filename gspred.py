import gspread
from oauth2client.service_account import ServiceAccountCredentials


def setsheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('arctic-signer-.json', scope)
    global worksheet    
    gc = gspread.authorize(credentials)
    gc = gc.open("mySheet")
    worksheet = gc.worksheet("oneday_kibutsu")#管理シートを指定


def search_last_row(num):
        row_count = 1
        while worksheet.cell(row_count, num).value:
            row_count += 1
        return row_count


def record_keyword(keyword):
    worksheet.update_cell(search_last_row(1), 1, keyword)


def record_error(keyword):
    worksheet.update_cell(search_last_row(2), 2, keyword)


def record_notExist(keyword):
    worksheet.update_cell(search_last_row(3), 3, keyword)


def record_userinfo(display_name, user_id, status_message, picture_url):
    worksheet.update_cell(search_last_row(5), 5, display_name)
    worksheet.update_cell(search_last_row(6), 6, user_id)
    worksheet.update_cell(search_last_row(7), 7, status_message)
    worksheet.update_cell(search_last_row(8), 8, picture_url)