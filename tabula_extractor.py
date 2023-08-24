import tabula
from tabula.io import read_pdf
import time
import PyPDF2
import json 
import pandas as pd
from header import *
# from part_1_extractor import *
# from part_2_extractor import *

class TabulaTableExtractor:

    def __init__(self, pdf_file_path) -> None:
        self.header = None
        self.part_1_tables = None
        self.part_2_tables = None
        self.part_3_tables = None
        self.part_4_tables = None
        self.part_5_tables = None
        self.part_6_tables = None
        self.pdf_file_path = pdf_file_path
        self.pdf_tables = []
        self.output_json = {}
        self.output_file_name = "output_json/" + pdf_file_path.replace("tmp/","").split(".")[0] + ".json"
        with open("boe_edi_template.json", "r") as f:
            self.output_json = json.load(f)
    
    def extract_encoding(pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            info = pdf_reader.getDocumentInfo()
            encoding = info.get('/Encoding')

            if encoding is not None:
                print(f"The PDF encoding is: {encoding}")
                return encoding
            else:
                print("No encoding information found in the PDF.")
                return 'Latin-1'

    def search_text_in_dataframes(self, search_text):
        matching_tables = []
        for index, table in enumerate(self.pdf_tables):
            dataframe = pd.DataFrame(table)
            # Convert all columns to string type for easier searching
            dataframe = dataframe.astype(str)
            
            # Check if search_text exists in any column of the dataframe
            if dataframe.apply(lambda x: x.str.contains(search_text, case=False)).any().any():
                matching_tables.append(table)
        
        return matching_tables

    
    def process_pdf(self):
        t1 = time.time()
        self.pdf_tables = tabula.read_pdf (self.pdf_file_path, pages='all', lattice=True, 
                                encoding="Latin-1",
                                guess=False,
                                pandas_options={"header":False})
        t2 = time.time()
        print(f"{self.pdf_file_path} Time taken: {round(t2 - t1, 2)} Sec.")
        
        
                          
    
        extract_file(self.pdf_file_path, self.output_json, self.output_file_name)
      

