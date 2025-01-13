from models import (
    Session,
    Results,
    MainCategory,
    SubCategory,
)
from datetime import datetime
import re
from sqlalchemy.sql import extract

WORD_BOUNDARY = r"\b([A-Za-z]+)"


def entry_exists_in_database(estmnt_file_path: str):
    try:
        result = (
            Session.query(Results).filter(Results.file_name == estmnt_file_path).first()
        )
        return result is not None
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.close()


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
    finally:
        Session.close()


def save_db_results(estmnt_file_path, output_json):
    try:
        results = Results(file_name=estmnt_file_path, output_json=output_json)
        Session.add(results)
        Session.commit()
        print("Data committed to DB successfully")
    except Exception as e:
        print(f"Error saving results to DB: {e}")
    finally:
        Session.close()


def get_all_main_categories():
    try:
        return Session.query(MainCategory).all()
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.close()


def get_main_category_name(main_category_id):
    try:
        return (
            Session.query(MainCategory)
            .filter(MainCategory.id == main_category_id)
            .first()
        )
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.close()


def delete_pdf_entry_from_db(file_name: str):
    try:
        entry = Session.query(Results).filter(Results.file_name == file_name).first()
        if entry:
            Session.delete(entry)
            Session.commit()
            return True
        return False
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.close()


def get_analyzed_pdf_from_db(file_name: str):
    session = Session()
    try:
        entry = session.query(Results).filter(Results.file_name == file_name).first()
        if entry:
            return entry.output_json
        return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_analyzed_pdfs_list_from_db(year: int = None):
    try:
        if year:
            pdf_list = [
                {item.file_name: item.output_json}
                for item in Session.query(Results).filter(
                    extract("year", Results.analyzed_at) == year
                )
            ]
        else:
            pdf_list = [
                {item.file_name: item.output_json}
                for item in Session.query(Results).all()
            ]
        return pdf_list
    except Exception as e:
        Session.rollback()
        raise e


def update_pdf_timestamp(file_name: str, new_timestamp: datetime):
    try:
        parsed_timestamp = datetime.strptime(new_timestamp, "%Y-%m-%d")
        entry = Session.query(Results).filter(Results.file_name == file_name).first()
        if entry:
            entry.analyzed_at = parsed_timestamp
            Session.commit()
            return True
        return False
    except Exception as e:
        Session.rollback()
        raise e
    finally:
        Session.close()
