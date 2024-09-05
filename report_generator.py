from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet#, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
import datetime
import platform
import uuid
#import os
from getmac import get_mac_address


def data_processing(raw_data):
    data=[["S.NO","Section","Description","PASS/FAIL"],]
    for i,j in enumerate(raw_data):
        temp=[i,]
        temp.append(j["title"])
        temp.append(j["desc"])
        temp.append(j["pof"][2])
        data.append(temp)
    return data

def create_pdf(data):
    #print(data)
    # Get the MAC address of the default network interface
    mac_address = get_mac_address()

    # Get current date and time
    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get system info
    username = platform.uname().node
    # Replace this with actual MAC address retrieval if needed

    # Generate a unique report ID
    report_id = str(uuid.uuid4())

    # Create PDF
    pdf_filename = "output/report.pdf"
    document = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch, bottomMargin=inch)

    # Set up styles
    styles = getSampleStyleSheet()
    
    # Use Paragraphs to enable word wrapping within the cells
    data_wrapped = [
        [Paragraph(cell, styles['Normal']) if isinstance(cell, str) else cell for cell in row] 
        for row in data
    ]
    
    title_style = styles['Title']
    title_style.alignment = 1  # Center alignment for the title

    normal_style = styles['Normal']
    normal_style.alignment = 0  # Left alignment for normal text

    # Create PDF content
    content = []

    # Create a table with logo and title
    logo_path = "pdf.png"
    logo_width = 60
    logo_height = 60

    # Prepare content for the table with logo and title
    logo_title_table_data = [
        [
            Paragraph(f'<img src="{logo_path}" width="{logo_width}" height="{logo_height}"/>', normal_style),
            Paragraph('CIS BENCHMARKS FOR UBUNTU 22.04', title_style),
        ]       
    ]

    # Create a table for logo and title with spacing adjustment
    logo_title_table = Table(logo_title_table_data, colWidths=[logo_width, 6*inch])

    # Set TableStyle for the logo and title table
    logo_title_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # Center logo vertically
        ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),  # Center title vertically
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Center logo horizontally
        ('ALIGN', (1, 1), (1, 0), 'CENTER'),  # Center title horizontally
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # White background
    ]))

    content.append(logo_title_table)
    content.append(Spacer(1, 0.5*inch))  # Space between title and other content

    # Add Date and Time
    content.append(Paragraph(f'Date and Time: {date_time_str}', normal_style))
    content.append(Spacer(1, 0.1*inch))

    # Add Report ID
    content.append(Paragraph(f'Report ID: {report_id}', normal_style))
    content.append(Spacer(1, 0.5*inch))  # Space before the table


    # Create and add table
    table = Table(data_wrapped, colWidths=[0.5*inch, 2.5*inch, 3.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to the top of each cell
        ('WORDWRAP', (0, 0), (-1, -1), None),  # Enable word wrapping
    ]))

    content.append(table)
    content.append(Spacer(1, 0.5*inch))  # Space before system info

    # Add username and MAC address at the bottom left corner
    content.append(Paragraph(f'Username: {username}', normal_style))
    content.append(Paragraph(f'MAC Address: {mac_address}', normal_style))

    # Add page number at the bottom right corner
    def add_page_number(canvas, doc):
        canvas.drawRightString(7.5*inch, 0.5*inch, f'Page {doc.page}')

    # Build PDF
    document.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)

    print(f"PDF generated: {pdf_filename}")
      
#if data is not processed then use 
# d1=data_processing(data)  
# create_pdf(d1)


#already processed data is d1

