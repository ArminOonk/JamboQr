from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import A4, landscape
import os

c = canvas.Canvas('teamleader.pdf', pagesize=landscape(A4))
max_team_nr = 65
for i in range(max_team_nr):
    c.setFont('Helvetica', 400)
    c.drawCentredString(400, 200, str(i+1))
    c.showPage()
c.save()

c2 = canvas.Canvas('teams.pdf', pagesize=landscape(A4))
max_team_nr = 65
for i in range(max_team_nr):
    c2.setFont('Helvetica', 100)
    c2.setLineWidth(1)
    for x in range(4):
        for y in range(4):
            c2.drawCentredString(x*200+100, y*120+100, str(i+1))

    c2.line(200, 50, 200, 550)
    c2.line(400, 50, 400, 550)
    c2.line(600, 50, 600, 550)
    c2.line(50, 190, 750, 190)
    c2.line(50, 310, 750, 310)
    c2.line(50, 430, 750, 430)
    c2.showPage()
c2.save()
