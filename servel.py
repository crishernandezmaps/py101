import wget
import pandas as pd
from tabula import read_pdf

def servel():     # Generating list of codes
    df = pd.read_html('https://zeus.sii.cl/avalu_cgi/br/brch10.sh')
    table_codes = df[-1][0][1:].values
    for i in table_codes:
        try:
            pdf_url = f"https://www.servel.cl/wp-content/uploads/2020/01/A{i}.pdf"
            print(f'Downloading {i}')
            wget.download(pdf_url)
        except:
            pass

def read_pds(a_pdf):
    df = tabula.read_pdf(a_pdf, pages='all')
    return df


if __name__ == "__main__":
    # servel()
    read_pds('A15102.pdf')
    pass