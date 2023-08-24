import os
from tabula_extractor import TabulaTableExtractor

def main():
    pdf_folder = "tmp/"
    total_pdf =os.listdir(pdf_folder).__len__()
    print(f"total {total_pdf} pdf is found")
    files = os.listdir(pdf_folder)
    for file in files:
        file_path = pdf_folder + file
        extractor = TabulaTableExtractor(file_path)
        
        extractor.process_pdf()
    
        # extractor.extract_header_details()        
        # extractor.extract_part1_details()        
        # extractor.extract_part2_details()
        # extractor.extract_part3_details()
    
    print("done")
    print(f"Processing of all ({total_pdf}) PDFS are completed")
main()