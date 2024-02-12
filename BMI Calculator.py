# BMI Calculator App

'''Create an application/program for a BMI Calculator. 

You can use the tkinter library for the interface, store a few users' data in a file and use matplotlib to display the BMI chart. 
You may choose to display it as a pie chart(percentage of people overweight/underweight/normal/obese)or bar chart.'''

from collections import Counter #
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox, Button, E, Entry, Frame, Label, LabelFrame, StringVar, Tk, W
from tkinter.ttk import Combobox, Spinbox

import data #code created to write the data and read the content of the file. 


def center(window, height=340, width=680): #Resizing and centralizing the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry("%dx%d+%d+%d" % (width, height, x, y))


main_window = Tk()
main_window.title("BMI Calculator")
center(main_window)

frame = Frame(main_window)
frame.pack()

patient_info_frame = LabelFrame(frame, text="Patient")
patient_info_frame.grid(row=1, column=0, padx=10, pady=5, sticky="news")

name_label = Label(patient_info_frame, text="Name: ")
name_label.grid(row=0, column=0)
name_var = StringVar()
name_txt = Entry(patient_info_frame, textvariable=name_var)
name_txt.grid(row=0, column=1, padx=10, pady=10)

gender_label = Label(patient_info_frame, text="Gender: ")
gender_label.grid(row=0, column=2)
gender_var = StringVar()
gender_combo = Combobox(patient_info_frame, values=[
                        "Male", "Female"], textvariable=gender_var)
gender_combo.grid(row=0, column=3, padx=10, pady=10)

age_label = Label(patient_info_frame, text="Age: ")
age_label.grid(row=0, column=4)
age_var = StringVar()
age_box = Spinbox(patient_info_frame, from_=2, to=100, textvariable=age_var)
age_box.grid(row=0, column=5, padx=10, pady=10)

height_label = Label(patient_info_frame, text="Height (cm): ")
height_label.grid(row=1, column=0)
height_var = StringVar()
height_txt = Entry(patient_info_frame, textvariable=height_var)
height_txt.grid(row=1, column=1, padx=10, pady=10)

weight_label = Label(patient_info_frame, text="Weight (kg): ")
weight_label.grid(row=1, column=2)
weight_var = StringVar()
weight_txt = Entry(patient_info_frame, textvariable=weight_var)
weight_txt.grid(row=1, column=3, padx=10, pady=10)

result_frame = LabelFrame(frame, text="Result")
result_frame.grid(row=2, column=0, padx=10, pady=5, sticky="news")

bmi_label = Label(result_frame, text="BMI: ")
bmi_label.grid(row=0, column=0)
bmi_var = StringVar()
bmi_txt = Entry(result_frame, state="readonly", textvariable=bmi_var)
bmi_txt.grid(row=0, column=1, padx=10, pady=10)

category_label = Label(result_frame, text="Category: ")
category_label.grid(row=1, column=0)
category_var = StringVar()
category_txt = Entry(result_frame, state="readonly", textvariable=category_var)
category_txt.grid(row=1, column=1, padx=10, pady=10)


ENTRIES = {
    "name": name_var,
    "age": age_var,
    "gender": gender_var,
    "weight": weight_var,
    "height": height_var,
    "bmi": bmi_var,
    "category": category_var,
}

FIELDS_TO_VALIDATE = ("weight", "height")

#To search for a existing patient in the CSV file and test the code easily:

search_frame = LabelFrame(frame, text="Search")
search_frame.grid(row=0, column=0, padx=10, pady=5, sticky="news")

search_name_label = Label(search_frame, text="Name: ")
search_name_label.grid(row=0, column=0)
search_name_var = StringVar()
search_name_txt = Entry(search_frame, textvariable=search_name_var)
search_name_txt.grid(row=0, column=1, padx=10, pady=10)


def set_value(entry, value): # Sets the entry to the specified value.
    entry.set(value)


def populate_fields(patient): #Auto-fill the entries with the specified patient dict value.
    for entry_name, entry in ENTRIES.items():
        set_value(entry, patient[entry_name])


def clear_fields(): #Clear the values setting the values to an empty string.
    for entry in ENTRIES.values():
        set_value(entry, "")


def search(): #Search the patient in the CVS file and populates the fields if the patient is found.
    clear_fields()
    name = search_name_var.get()
    patient = data.find(name)

    if patient:
        populate_fields(patient)
        search_name_var.set("")
        calculate_button.focus_set()


search_button = Button(search_frame, text="Search", command=search)
search_button.grid(row=0, column=2, padx=10, pady=10, sticky=E)

#Calculate and display BMI

def calculate_bmi(weight, height): #Calculate the BMI and return a error message box if the weight or height field is not a number.
    try:
        return round(float(weight) / float(height)**2, 2)
    except ValueError:
        messagebox.showwarning(
            title="Error", message="Weight and Height must be numbers.")


def categorize_bmi(bmi):#Categorize the BMI
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def read_patient(): #Reads the user's entries and creates a dict.
    return {
        "name": name_txt.get(),
        "age": age_box.get(),
        "gender": gender_combo.get(),
        "weight": weight_txt.get(),
        "height": height_txt.get(),
        "bmi": bmi_txt.get(),
        "category": category_txt.get(),
    }


def show_bmi(): #Retrieves the patient's info, calculate BMI, updates the BMI and the categoru fields ans save the data in the CSV file.
    patient = read_patient()
    bmi = calculate_bmi(patient["weight"], patient["height"])

    if bmi:
        category = categorize_bmi(bmi)
        patient |= {"bmi": bmi, "category": category}
        populate_fields(patient)
        data.insert(patient)


calculate_button = Button(frame, text="Calculate and Save", command=show_bmi)
calculate_button.grid(row=4, column=0, padx=10, pady=10, sticky=E)

# Display statistics using pie chart

def show_statistics():
    window = Tk()
    window.title("Statistics")
    center(window, height=400, width=500)

    frame = Frame(window)
    frame.pack()

    figure = Figure()
    axes = figure.add_subplot(111)

    patients = data.read() #Reads the data  from the data module
    categories = (patient["category"] for patient in patients) #Interetes over each "patient" dict, retrieves the key "category" using the dict index. Assing it to "categories" becoming an interable.

    occurrences = dict(Counter(categories)) #Count the cocurences os each category
    axes.pie(occurrences.values(), labels=occurrences.keys(), autopct="%1.1f%%")

    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().pack()


statistics_button = Button(frame, text="Show Statistics", command=show_statistics)
statistics_button.grid(row=4, column=0, padx=10, pady=10, sticky=W)

main_window.mainloop()
