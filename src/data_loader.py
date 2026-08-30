import pandas as pd
from pathlib import Path
 

def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, encoding='utf-8')


    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        raise    
    except UnicodeDecodeError:
        df= pd.read_csv(path, encoding='latin1')

    except pd.errors.ParserError:
        print(f"Error: The file at {path} could not be parsed. Please check the file format.")
        raise
    except OSError as e:
        print(f"Error: An OS error occurred while trying to read the file at {path}: {e}")
        raise    

    return df

