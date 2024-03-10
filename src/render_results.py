import os 
from models import Session, Results

def entry_exists_in_database(estmnt_file_path: str) -> bool:
    result =  Session.query(Results).filter(Results.file_name == estmnt_file_path).first()
    if result:
        return True
    else:
        return False

if __name__ == "__main__":
    #estmnt_file_path = "October 2023.pdf"
    is_exist = entry_exists_in_database(estmnt_file_path)
    # commit results to db: