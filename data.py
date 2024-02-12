from csv import DictReader, DictWriter

FILENAME = "Data_BMI_Calculator.csv"
FIELDS = ("name", "age", "gender", "height", "weight", "bmi", "category")
KEY = "name"

#Reads the data from CSV and returns it as a tuple of dict. Each dict represensts a row in the CSV file
def read():
    with open(FILENAME, "r", newline='') as file:
        return tuple(DictReader(file))



def insert(row):
    rows = read()#Red existing rows

    with open(FILENAME, "w", newline='') as file:
        writer = DictWriter(file, fieldnames=FIELDS) #Creates the DictWriter object
        writer.writeheader() #Writes the header of the CSV file

        for existing_row in rows:
            if existing_row[KEY] == row[KEY]: #Finds a row with the same name as the new row
                writer.writerow(row) #Overwrites the new row
            else:
                writer.writerow(existing_row) #Write the existing row


def find(value): #search specific value (input) and compare with the existent value (KEY = "name") 
    for row in read():
        if row[KEY] == value:
            return row