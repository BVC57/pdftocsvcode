import csv
import os

output_csv = []
curr_list = [
    "INR", "USD", ".ﺇ.ﺩ", "$", "฿", "AED",
    "EUR", "₹", "SGD", "CNY", "AUD",
    "PHP", "£", "CAD", "JPY", "IDR",
    "VND", "MYR", "QAR", "THB", "Rp",
    "RM", "£", "₹", "₫", "GBP"
]
curr_prefix_list = [".ﺇ.ﺩ", "$", "AED", "Rp", "RM", "£", "₹", "₫", "฿"]

def is_float(n):
    try:
        if type(float(n.replace(',',''))).__name__ == 'float' or type(int(n).replace(',','')).__name__=='int':
            return True
    except:
        return False

def find_desc(line, index, file_list):
    temp_index = index
    no_of_items = 2
    description = ""
    if "Campaigns" in line:
        temp_index += 1
        while no_of_items > 0 and temp_index < len(file_list):
            if file_list[temp_index].lower().startswith("from") and "to" in file_list[temp_index].lower():
                description += file_list[temp_index - 2] + "\n"
                no_of_items -= 1
            temp_index += 1
        return description
    if "Description" in line:
        temp_index+=3
        if is_float(file_list[temp_index]):
            description+=file_list[temp_index]+" "
            return description
        while not is_float(file_list[temp_index]):
            description+=file_list[temp_index]+" "
            temp_index+=1
        return description

    return ""


def find_trans_amount(line, index, file_list):
    amount = ""
    if line == "Transaction ID":
        temp = index
        amount = file_list[temp - 1]
        for cur in curr_prefix_list:
            amount = amount.replace(cur, "")
            if len(amount.split(" ")) > 1:
                if amount.split(" ")[0] == "AED":
                    amount = amount.split(" ")[1]
                else:
                    amount = amount.split(" ")[0]
        amount = amount.strip()
    if "Invoice Total:" in line or 'Total Credit:' in line:
        amount = file_list[index+1].strip()
    return amount


supplier_address = [
    "Facebook Ireland Limited",
    "4 Grand Canal Square, Grand Canal Harbour",
    "Dublin 2, Ireland",
    "VAT Reg. No. IE9692928F"
]

supplier_address2 = [
    "Facebook, Inc.",
    "1601 Willow Road",
    "Menlo Park, CA 94025-1452"
]


def find_supplier_address(line, index, file_list):
    address = ""
    if "Facebook Ireland Limited" in line:
        temp = index
        address = ""
        while temp < len(file_list) and ("VAT Reg. No. IE9692928F" not in file_list[temp] or "GST:" not in file_list[temp]):
            if file_list[temp] in supplier_address:
                address += file_list[temp] + '\n'
            temp += 1
        if temp < len(file_list):
            address += (file_list[temp] +
                        '\n') if file_list[temp] in supplier_address else ""
    elif "Facebook, Inc." in line:
        temp = index
        address = ""
        while temp < len(file_list):
            if file_list[temp] in supplier_address2 or "GST/HST:" in file_list[temp]:
                address += file_list[temp] + '\n'
            elif temp < len(file_list)-1:
                if file_list[temp] == file_list[temp + 1]:
                    address += file_list[temp]
            temp += 1
    elif "Please refer to actual invoice for final charges." in line:
        address += line
    address = address.strip()
    return address


def find_customer_address(line, index, file_list):
    temp = index
    address = ""
    if "BILL TO:" in line:
        temp+=1
        while "ATTN:" not in file_list[temp]:
            if "Page:" in file_list[temp]:
                temp += 2
            address += file_list[temp]
            temp+=1
        return address
    if "Facebook Ireland Limited" in line or "Facebook, Inc." in line or "Please refer to actual invoice for final charges." in line:
        while temp:
            if len(file_list[temp].split(" ")) > 1:
                if file_list[temp].split(" ")[1] in curr_list:
                    break
            else:
                if [x for x in curr_list if x in file_list[temp]]:
                    break
            temp -= 1
        temp += 1
        if "Campaigns" not in file_list:
            while temp < len(file_list):
                if file_list[temp] == "Product Type":
                    temp += 2
                    break
                temp += 1

    if "Facebook Ireland Limited" in line:
        while temp < len(file_list):
            if file_list[temp] in supplier_address:
                temp += 1
                continue
            address += (file_list[temp] + "\n")
            temp += 1

    elif "Facebook, Inc." in line:
        while temp < len(file_list):
            if file_list[temp] in supplier_address2 or "GST/HST:" in file_list[temp]:
                temp += 1
                continue
            elif temp < len(file_list)-1:
                if file_list[temp] == file_list[temp + 1] or "GST/HST:" in file_list[temp]:
                    temp += 1
                    continue
            address += (file_list[temp] + "\n")
            temp += 1
    elif "Please refer to actual invoice for final charges." in line:
        while temp < len(file_list):
            address += (file_list[temp] + "\n")
            temp += 1

    address = address.strip()
    return address


def cur(line, index, file_list):
    temp_currency = ""
    if "Transaction ID" in line:
        if ".ﺇ.ﺩ" in file_list[index - 1]:
            temp_currency = str(file_list[index - 1]).split(" ")[0]
        else:
            temp_currency = str(file_list[index - 1]).split(" ").pop()
    elif "Invoice Currency:" in line or 'Credit Memo Currency:' in line:
        temp_currency = file_list[index+1]
    return temp_currency


def remove_prefix(text, prefix):
    if text.lower().startswith(prefix.lower()):
        return text[len(prefix):]
    return text


def find_name(line):
    prefix = ["Invoice for ", "Receipt for "]
    for p in prefix:
        line = remove_prefix(line, p)
    return line


def find_inv_date(line, index, file_list):
    if "Invoice/Payment Date" in line:
        return list(file_list)[index + 1]
    elif 'Invoice Date:' in line or 'Credit Memo Date:' in line:
        return file_list[index+1]
    return ""


def find_accId(line,line_index,file_list):
    if "Account ID:" in line:
        temp_acc_id = line.split(":")[1].strip()
        return "\"" + temp_acc_id + "\""
    elif 'Account Id' in line:
        temp_acc_id = file_list[line_index+1].strip()
        return "\"" + temp_acc_id + "\""
    return ""

# ------------------------------ Start Execution Here -----------------------


folder_path = str(input("folder name : "))
# for i in range(1, 41):
#     folder_path = "D:\\Facebook-Converted-Files\\Facebook-Text-Files\\" + \
#         str(i)
#folder_path = "incoming-file/"
folder_path = "TXT/" + folder_path
list_of_files = []
for file in os.listdir(folder_path):
    if file.endswith(".txt"):
        obj = {
            "FileName": file,
            "FilePath": os.path.join(folder_path, file)
        }
        list_of_files.append(obj)
        print(os.path.join(folder_path, file))

for file_obj,file_name in zip(list_of_files,os.listdir(folder_path)):
    file_name = file_name.replace('.txt','')
    output_row = {
        "FileName": "",
        "AccountId": "",
        "Name": "",
        "InvoiceDate": "",
        "Currency": "",
        "Description": "",
        "SupplierAddress": "",
        "CustomerAddress": "",
        "TransactionAmount": "",
    }

    file_list = []
    with open(file_obj["FilePath"], "r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                file_list.append(line)
        file_list = list(map(str.strip, file_list))
    # file_list.remove("Powered by TCPDF (www.tcpdf.org)")

    print(f"Processing -> {file_obj['FilePath']}")
    output_row["FileName"] = file_obj["FileName"]
    line_index = 0
    for line in file_list:
        if line_index == 0:
            output_row["Name"] = find_name(line)

        AccountId = find_accId(
            line,line_index,file_list)
        if AccountId:
            output_row["AccountId"] = AccountId if AccountId!= "" else ""

        InvoiceDate = find_inv_date(
            line, line_index, file_list)
        if InvoiceDate:
            output_row["InvoiceDate"] = InvoiceDate if InvoiceDate != "" else ""

        currency = cur(line, line_index,
                        file_list)
        if currency:
            output_row["Currency"] = currency if currency!= "" else ""

        sup_addres = find_supplier_address(
            line, line_index, file_list)
        if sup_addres:
            output_row["SupplierAddress"] = sup_addres if sup_addres!="" else ""

        cust_address = find_customer_address(
            line, line_index, file_list)
        if cust_address:
            output_row["CustomerAddress"] = cust_address if cust_address!="" else ""

        trans_amount = find_trans_amount(
            line, line_index, file_list)
        if trans_amount:
            output_row["TransactionAmount"] = trans_amount if trans_amount!="" else ""

        find_description = find_desc(
            line, line_index, file_list)
        if find_description:
            output_row["Description"] = find_description if find_description!="" else ""

        line_index += 1

    output_csv.append(output_row)

if len(output_csv):
        keys = output_csv[0].keys()
        if os.path.exists('output-file/output.csv'):
            with open('output-file/output.csv', 'a', newline='', encoding="utf8") as out_file:
                dict_writer = csv.DictWriter(out_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(output_csv)
        else:
            with open('output-file/output.csv', 'w', newline='', encoding="utf8") as out_file:
                dict_writer = csv.DictWriter(out_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(output_csv)
