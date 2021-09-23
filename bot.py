import slack
from fpdf import FPDF
import os


pdf = FPDF(orientation='landscape')
pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.set_margin(0)
pdf.image(x = -0.5, y = 12, w = pdf.w + 1, name='RIFLogo(B&W).png')

pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.set_fill_color(0, 0, 0)
pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')

pdf.add_page()
pdf.set_fill_color(128, 0, 0)
pdf.rect(x = 0, y = 0, w = pdf.w, h = 12, style = 'F')
pdf.rect(x = 0, y = 198, w = pdf.w, h = 12, style = 'F')
pdf.set_fill_color(0, 0, 0)
pdf.rect(x = 0, y = 12, w = pdf.w, h = 186, style = 'F')


#pdf.set_text_color(r=128, g=0, b=0)
#pdf.set_font(family='Times', style='B', size=26)
#pdf.cell(w=295, h=210, txt='The Rambler Investment Fund', align='C', center=True)







pdf.output('pdf_1.pdf')



#### Call Bot and Send Portfolio
# client = slack.WebClient(token = '####')
# client.chat_postMessage(channel = '#sector-materials', text='Hello World!')