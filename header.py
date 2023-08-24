import pdfplumber
import json
from mis_function import *
import copy 
import csv
import os
import datetime

# this code for take current date and time with file created
# download_path = f"csv_download_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
# os.makedirs(download_path)
cdt=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
sno=0
def extract_file(pdf_file_path, output_json, output_file_name):
    """
    """
    global sno
    global cdt
    combined_data = []
    with pdfplumber.open(pdf_file_path) as pdf:
        combined_table = []
        sno+=1
        for page in pdf.pages[0:]:# Modify the page range as needed
            text = page.extract_text()
            if text:
                table = text.split("\n")
                combined_table.extend(table)
        items = [line.split("\n") for line in combined_table]
    

        if "Invoice No SC" in text:
            
            extract_gardiner(pdf_file_path, output_json, output_file_name,items, combined_data)
            
        elif "INVOICE INVOICE" in text:
            
            extract_new_gardiner(pdf_file_path, output_json, output_file_name,items, combined_data)
            
            
        elif "Harneys Corporate Services Limited" in combined_table:
            
            extract_harneys(pdf_file_path, output_json, output_file_name,items, combined_data)
            
        elif "Invoice Number" in combined_table:
            
            extract_savills(pdf_file_path, output_json, output_file_name,items, combined_data)
            
        elif "Olayan Europe Ltd" in text:
            
            extract_olaya(pdf_file_path, output_json, output_file_name,items, combined_data)
            
        elif "BW Interiors Ltd"in text:
            
            extract_BW(pdf_file_path, output_json, output_file_name,items, combined_data)
        
def create_csv(data):
  if len(data):
       
        header_keys = data[0].keys()

        output_folder = r"output_csv_file"
        output_file = os.path.join(output_folder, f"outputfile{cdt}.csv")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"New folder created: {output_folder}")

        if not os.path.exists(output_file):
            with open(output_file, "w", newline="", encoding="utf-8") as file:
                csv_writer = csv.DictWriter(file, fieldnames=header_keys)
                csv_writer.writeheader()
                print(f"New CSV file created: {output_file}")

        with open(output_file, "a", newline="", encoding="utf-8") as file:
            csv_writer = csv.DictWriter(file, fieldnames=header_keys)
            csv_writer.writerows(data)
            print("Data appended to CSV file") 
            
                   
def extract_gardiner(pdf_file_path, output_json, output_file_name,items, combined_data):
    for key, value in output_json.get("header", {}).items():
        # temp_invoice = copy.deepcopy()
       
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno 
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "Gardiner & Theobald LLP"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            text = ""
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "Invoice No")
            text = items[start_idx[0]][0].split("Invoice No")[1].strip() 
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "Job Ref")
            text = items[start_idx[0]][0].split("Job Ref")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Date & Tax Point")
            text = items[start_idx[0]][0].split("Date & Tax Point")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Sub-Total exclusive of VAT")
            text = items[start_idx[0]][0].split("Sub-Total exclusive of VAT")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            start_idx = find_row_index(items, "Plus Value Added Tax")
            text = items[start_idx[0]][0].split(" ")[6]
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "TOTAL AMOUNT DUE")
            text = items[start_idx[0]][0].split(" ")[3]
            output_json["header"][key] =  text if text else ""
    # return output_json["header"]
    combined_data.append(output_json["header"])
    create_csv(combined_data)
    return combined_data

def extract_new_gardiner(pdf_file_path, output_json, output_file_name,items, combined_data):
    for key, value in output_json.get("header", {}).items():
        # temp_invoice = copy.deepcopy()
       
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno 
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "Gardiner & Theobald LLP"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            text = ""
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "INVOICE INVOICE")
            text = items[start_idx[0]][0].split("INVOICE INVOICE")[1].strip() 
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "Job Ref")
            text = items[start_idx[0]][0].split("Job Ref")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Date & Tax Point")
            text = items[start_idx[0]][0].split("Date & Tax Point")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Sub-Total exclusive of VAT")
            text = items[start_idx[0]][0].split("Sub-Total exclusive of VAT")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            start_idx = find_row_index(items, "Plus Value Added Tax")
            text = items[start_idx[0]][0].split(" ")[6]
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "TOTAL AMOUNT DUE")
            text = items[start_idx[0]][0].split(" ")[3]
            output_json["header"][key] =  text if text else ""
    # return output_json["header"]
    combined_data.append(output_json["header"])
    create_csv(combined_data)
    return combined_data
    
def extract_harneys(pdf_file_path, output_json, output_file_name,items, combined_data):
    
    for key, value in output_json.get("header", {}).items():
        # temp_invoice = copy.deepcopy()
        #counter[0] += 2
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "Harneys Corporate Services Limited"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            text = ""
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "Invoice No.:")
            text = items[start_idx[0]][col].split("Invoice No.:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "Ref:")
            text = items[start_idx[0]][0].split("Ref:")[1].split(" ")[1]
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Invoice Date:")
            text = items[start_idx[0]][0].split("Invoice Date:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Subtotal")
            text = items[start_idx[0]][0].split(" ")[3]
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            text = "-"
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "Subtotal")
            text = items[start_idx[0]][0].split(" ")[3]
            output_json["header"][key] =  text if text else ""
            
     # return output_json["header"]       
    combined_data.append(output_json["header"])
    #append all result data into csv file        
    create_csv(combined_data)
    
    return combined_data


def extract_BW(pdf_file_path, output_json, output_file_name,items, combined_data):
    
    for key, value in output_json.get("header", {}).items():
        
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "BW Interiors Ltd"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            text = ""
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "Invoice Number")
            text = items[start_idx[0]][col].replace("Invoice Number", "").replace("Project Number 7720", "")
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "REF:")
            text = items[start_idx[0]][0].replace("11 Hamilton Place, London, ", "").replace("REF:", "")
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Invoice Date")
            text = items[start_idx[0]][0].split("Invoice Date")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Credit note against the invoice 16473 #12 ")
            text = items[start_idx[0]][0].split(" ")[7]
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            text = "-"
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "Gross certified")
            text = items[start_idx[0]][0].split(" ")[4]
            output_json["header"][key] =  text if text else ""
            
     # return output_json["header"]       
    combined_data.append(output_json["header"]) 
    #append all result data into csv file       
    create_csv(combined_data)
    return combined_data



def extract_savills(pdf_file_path, output_json, output_file_name,items, combined_data):
    
    for key, value in output_json.get("header", {}).items():
        # temp_invoice = copy.deepcopy()
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "Savills"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            text = ""
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "Invoice Number")
            text = items[start_idx[0]+1][0]
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "Our Ref:")
            text = items[start_idx[0]][0].split("Our Ref:")[1].split(" ")[1]
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Date:")
            text = items[start_idx[0]][0].split("Date:")[1].split(" ")[1]
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Interest may be charged on late payment")
            text = items[start_idx[0]+1][0].split("Interest may be charged on late payment")[0].split(" ")[0]
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            start_idx = find_row_index(items, "Interest may be charged on late payment")
            text = "-"
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "Interest may be charged on late payment")
            text = items[start_idx[0]+1][0].split("Interest may be charged on late payment")[0].split(" ")[0]
            output_json["header"][key] =  text if text else ""
    # return output_json["header"]
    combined_data.append(output_json["header"]) 
    #append all result data into csv file       
    create_csv(combined_data)
    return combined_data  

def extract_olaya(pdf_file_path, output_json, output_file_name,items, combined_data):
    
    for key, value in output_json.get("header", {}).items():
        # temp_invoice = copy.deepcopy()
        #counter[0] += 5
        row = value.get("row",0)            

        col = value.get("col",0)
        if key in ["S.no."]:
            text = sno 
            output_json["header"][key] = text
        elif key in ["Supplier Name"]:
            text = "H/m"
            output_json["header"][key] =  text if text else ""
        elif key in ["Supplier VAT registration number"]:
            start_idx = find_row_index(items, "VAT Number:")
            text = items[start_idx[0]][0].split("VAT Number:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice No."]:
            start_idx = find_row_index(items, "Invoice No:")
            text = items[start_idx[0]][0].split("Invoice No:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Reference No"]:
            start_idx = find_row_index(items, "Project No:")
            text =  items[start_idx[0]][0].split("Project No:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Invoice Date"]:
            start_idx = find_row_index(items, "Date:")
            text = items[start_idx[0]][0].split("Date:")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Tax base amount"]:
            start_idx = find_row_index(items, "Sub Total")
            text = items[start_idx[0]][0].split("Sub Total")[1].strip()
            output_json["header"][key] =  text if text else ""
        elif key in ["Input tax"]:
            start_idx = find_row_index(items, "Sub Total")
            text = items[start_idx[0]+1][0].split("VAT")[1].split(" ")[3]
            output_json["header"][key] =  text if text else ""
        elif key in ["Gross amount"]:
            start_idx = find_row_index(items, "TOTAL")
            text = items[start_idx[0]][0].split("TOTAL")[1].strip()
            output_json["header"][key] =  text if text else ""
    # return output_json["header"]
    combined_data.append(output_json["header"])
     #append all result data into csv file       
    create_csv(combined_data)
    return combined_data

    """
    Your existing code for writing data to a CSV file
    """
 
        