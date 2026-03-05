from typing import List
import csv
from models import Bio


def get_bio_instances() -> List[Bio]:
    """
    Reads bio.csv and creates a list of Bio instances.
    
    Returns:
        List[Bio]: A list of all Bio instances from the CSV file.
    """
    bio_instances = []
    
    with open('bio.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert inducted to int if it exists and is not empty
            inducted = int(row['inducted']) if row['inducted'] else None
            
            bio = Bio(
                name=row['name'],
                inducted=inducted,
                category=row['category'] if row['category'] else None,
                inducted_by=row['inducted_by'] if row['inducted_by'] else None
            )
            bio_instances.append(bio)
    
    return bio_instances
