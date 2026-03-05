from typing import List
import csv
from models import Non_Performers


def get_non_performers_instances() -> List[Non_Performers]:
    """
    Reads non_performers.csv and creates a list of Non_Performers instances.
    
    Returns:
        List[Non_Performers]: A list of all Non_Performers instances from the CSV file.
    """
    non_performers_instances = []
    
    with open('non_performers.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert class_year to int if it exists and is not empty
            class_year = int(row['class_year']) if row['class_year'] else None
            
            non_performer = Non_Performers(
                name=row['name'],
                class_year=class_year,
                category=row['category'] if row['category'] else None
            )
            non_performers_instances.append(non_performer)
    
    return non_performers_instances
