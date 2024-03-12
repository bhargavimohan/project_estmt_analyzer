import pdfplumber
import re
import json
import os
from sqlalchemy import func
import requests
from render_results import entry_exists_in_database
from models import Session, MainCategory, SubCategory, Results


WORD_BOUNDARY = r'\b([A-Za-z]+)'


def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_desired_costs(pdf_text):
    # alter_saldo_index = None
    # neuer_saldo_index = None
    cost_list = pdf_text.split('\n')
    for i, string in enumerate(cost_list):
        if 'ALTER SALDO' in string: 
            alter_saldo_index = i
        elif 'NEUER SALDO' in string:
            neuer_saldo_index = i
            break
    # Extract the sublist between 'ALTER SALDO' and 'NEUER SALDO'
    if alter_saldo_index is not None and neuer_saldo_index is not None:
        filtered_cost_list = cost_list[alter_saldo_index : neuer_saldo_index + 1]
    else:
        filtered_cost_list = []
    
    return filtered_cost_list

def get_sub_category(sub_category_str):
    sub_category = Session.query(SubCategory).filter(SubCategory.sub_category.like(f'%{sub_category_str.split(" ")[1]}%')).first()
    if not sub_category:
        category_string = ' '.join(sub_category_str.split(" ")[1:-1])
        processed_sub_category = re.search(WORD_BOUNDARY,category_string).group()
        sub_category = Session.query(SubCategory).filter(SubCategory.sub_category == processed_sub_category).first()
    return sub_category

def classify_costs(desired_cost_list):
    main_categories = Session.query(MainCategory).all()
    deposits = []
    classified_costs_dict = {main_category.main_category: [] for main_category in main_categories}
    for sub_category_str in desired_cost_list:
        sub_category = get_sub_category(sub_category_str)
        if 'ALTER SALDO' in sub_category_str: # record the old balance
            classified_costs_dict.update({'Old Balance' : sub_category_str})
        elif 'EINZAHLUNG' in sub_category_str: # record the deposits
            deposits.append(sub_category_str)
        elif 'NEUER SALDO' in sub_category_str: # record the new balance
            classified_costs_dict.update({'New Balance' : sub_category_str})
        elif 'SOLLZINSEN' in sub_category_str: # record the new balance
            classified_costs_dict.update({'Debit Interest' : sub_category_str})
        elif 'Gesetzliche Vertreter' in sub_category_str: # skip the page footer
            continue
        elif sub_category:
            # If a matching sub category is found, get the associated main category name
            main_category_id = sub_category.main_category_id
            main_category_name = Session.query(MainCategory).filter(MainCategory.id == main_category_id).first()
            main_category_name = main_category_name.main_category
    
            # If main category doesn't exist in the dictionary, add it with an empty list
            if main_category_name not in classified_costs_dict:
                classified_costs_dict[main_category_name] = []
            # Append the sub category to the list of sub categories for its main category
            classified_costs_dict[main_category_name].append(sub_category_str)
        
        else:
            classified_costs_dict["Others"].append(sub_category_str)
            print("No subcategory for  " + sub_category_str)

    classified_costs_dict.update({'Deposit' : deposits})
    return classified_costs_dict

def compute_category_costs(classified_cost_dict):
    final_costs_dict = {}
    for key, value in classified_cost_dict.items():
        total_cost = 0
        if isinstance(value, list):
            for list_item in value:
                decimal_part = float(list_item.split(" ")[-1].replace(".","").replace(",", "."))
                total_cost += decimal_part
            final_costs_dict[key] = round(total_cost,2)
        else:
            spl_decimal_part = float(value.split(" ")[-1].replace(".","").replace(",", "."))
            total_cost = spl_decimal_part
            final_costs_dict[key] = round(total_cost,2)
    return final_costs_dict


def verify_category_total_costs(final_cost_dict):
    RHS = 0
    for key, value in final_cost_dict.items():
        if key == 'New Balance':
            LHS = value # from e-stmnt
        else:
            RHS += value # analyzer calculated
    RHS = round(RHS,2)
    final_cost_dict.update({"Cost of ALL categories" : RHS})
    if LHS == RHS:
        success_message = "TADAAAA!!Individual costs combined match the New Balance 😊"
        final_cost_dict.update({"E-stmnt Analyzer Status" : success_message})
    else:
        warning_message = "Uh Oh!!We've encountered an issue 😬 Individual costs put together does not align with the New Balance in your "  
        "e-statement"
        final_cost_dict.update({"E-stmnt Analyzer Status" : warning_message})
    return final_cost_dict
    
def main (estmnt_file_path):
    is_pdf_reviewed = entry_exists_in_database(estmnt_file_path)
    if is_pdf_reviewed is False:
        estmnt_full_file_path = os.path.join("./pdfs/", estmnt_file_path)
        # read pdf
        pdf_extraction = read_pdf(estmnt_full_file_path)
        # extract the categories from pdf
        desired_cost_list = extract_desired_costs(pdf_extraction)
        # categorize items under their main category
        classified_cost_dict = classify_costs(desired_cost_list) 
        # calculate individual category's costs
        final_cost_dict= compute_category_costs(classified_cost_dict)
        # Final tally
        output_dict = verify_category_total_costs(final_cost_dict)
        # jsonify
        output_json = json.dumps(output_dict) 
        results = Results(file_name=estmnt_file_path, output_json=output_json)
        Session.add(results)
        Session.commit()
        print("Data commited to DB successfully")

if __name__ == "__main__":
    estmnt_file_path = "October 2023.pdf"
    main(estmnt_file_path)
    # commit results to db:
    

