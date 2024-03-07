import pdfplumber
import re
from sqlalchemy import func
from models import Session, MainCategory, SubCategory


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
            classified_costs_dict.update({'old_balance' : sub_category_str})
        elif 'EINZAHLUNG' in sub_category_str: # record the deposits
            deposits.append(sub_category_str)
        elif 'NEUER SALDO' in sub_category_str: # record the new balance
            classified_costs_dict.update({'new_balance' : sub_category_str})
        elif 'SOLLZINSEN' in sub_category_str: # record the new balance
            classified_costs_dict.update({'Debit_interest' : sub_category_str})
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

    classified_costs_dict.update({'deposit' : deposits})
    return classified_costs_dict

def aggregate_costs(classified_cost_dict):
    pass

if __name__ == "__main__":
    file_path = './src/pdfs/October 2023.pdf'
    # read pdf
    pdf_extraction = read_pdf(file_path)
    desired_cost_list = extract_desired_costs(pdf_extraction)
    classified_cost_dict = classify_costs(desired_cost_list) 
    final_cost_json = aggregate_costs(classified_cost_dict)
