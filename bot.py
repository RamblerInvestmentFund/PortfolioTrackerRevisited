import slack
from fpdf import FPDF
import quandl
from yahoo_fin import stock_info as si
import datetime
import pandas as pd
import os

today = datetime.date.today()
lastMonday = today - datetime.timedelta(days=today.weekday())
df = pd.read_csv(filepath_or_buffer='portfolio.csv')
basis = []

for idx in df.index:
    price = si.get_live_price('{ticker}'.format(ticker = df['Ticker'][idx]))
    basisPrice = price * df['Shares'][idx]
    basis.append(basisPrice)

df['Basis'] = basis

benchmark = pd.DataFrame()


# # ---- Cover Page

# pdf = FPDF(orientation='landscape')
# pdf.set_margin(2)
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# # ---- Date
# pdf.set_font("Times", size=22)
# pdf.set_font(style='B')
# pdf.set_text_color(237, 232, 228)
# pdf.cell(txt=str(date_object), align='C')
# # ----
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.image(x = -0.5, y = 12, w = pdf.w + 1, name='RIFLogo(B&W).png')

# # ---- Second Page
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.set_fill_color(0, 0, 0)
# pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')

# # ---- Third Page
# pdf.add_page()
# pdf.set_fill_color(128, 0, 0)
# pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
# pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
# pdf.set_fill_color(0, 0, 0)
# pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')


















# # ---- PDF Output
# pdf.output('pdf_1.pdf')




#### Call Bot and Send Portfolio
# client = slack.WebClient(token = '####')
# client.chat_postMessage(channel = '#sector-materials', text='Hello World!')