import gspread

gc = gspread.service_account(filename="client-api.json")

# Open a sheet from a spreadsheet in one go
wks = gc.open("Test Google Sheets API").sheet1

# Update a range of cells using the top left corner address
wks.update([["Привет", "это Навальный"], ["Я научу вас",
           "загружать данные в гугл-таблицы"]], 'A1')

# Or update a single cell
wks.update_acell('B42', "it's down there somewhere, let me take another look.")

# Format the header
wks.format('A1:B1', {'textFormat': {'bold': True}})
