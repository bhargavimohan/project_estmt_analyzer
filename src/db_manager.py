from models import Session, Results, MainCategory, SubCategory
import re

WORD_BOUNDARY = r"\b([A-Za-z]+)"


def entry_exists_in_database(estmnt_file_path: str) -> bool:
    result = (
        Session.query(Results).filter(Results.file_name == estmnt_file_path).first()
    )
    return result is not None


def get_sub_category(sub_category_str):
    try:
        sub_category = (
            Session.query(SubCategory)
            .filter(
                SubCategory.sub_category.like(f'%{sub_category_str.split(" ")[1]}%')
            )
            .first()
        )
        if not sub_category:
            category_string = " ".join(sub_category_str.split(" ")[1:-1])
            processed_sub_category = re.search(WORD_BOUNDARY, category_string).group()
            sub_category = (
                Session.query(SubCategory)
                .filter(SubCategory.sub_category == processed_sub_category)
                .first()
            )
        return sub_category
    except Exception as e:
        print(f"Error getting sub category for {sub_category_str}: {e}")
        return None


def save_db_results(estmnt_file_path, output_json):
    try:
        results = Results(file_name=estmnt_file_path, output_json=output_json)
        Session.add(results)
        Session.commit()
        print("Data committed to DB successfully")
    except Exception as e:
        print(f"Error saving results to DB: {e}")


def get_all_main_categories():
    return Session.query(MainCategory).all()


def get_main_category_name(main_category_id):
    return (
        Session.query(MainCategory).filter(MainCategory.id == main_category_id).first()
    )
