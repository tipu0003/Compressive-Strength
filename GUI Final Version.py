import pickle
import pandas as pd
import tkinter as tk
from tkinter import messagebox
# from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import unicodeit


# Load the trained XGBRegressor model
with open('GB_compressive_strength.pkl', 'rb') as model_file:
    gb_loaded = pickle.load(model_file)

# tkinter GUI
root = tk.Tk()
root.title(f"Prediction of Compressive Strength")

canvas1 = tk.Canvas(root, width=550, height=550)
canvas1.configure(background='#e9ecef')
canvas1.pack()

label0 = tk.Label(root, text='Developed by Mr. Rupesh Kumar', font=('Times New Roman', 15, 'bold'), bg='#e9ecef')
canvas1.create_window(20, 20, anchor="w", window=label0)

label_phd = tk.Label(root, text='K. R. Mangalam University, India.\nEmail: tipu0003@gmail.com',
                     font=('Futura Md Bt', 12), bg='#e9ecef')

canvas1.create_window(20, 50, anchor="w", window=label_phd)

label_input = tk.Label(root, text='Input Variables', font=('Times New Roman', 12, 'bold', 'italic', 'underline'),
                       bg='#e9ecef')
canvas1.create_window(20, 90, anchor="w", window=label_input)

# Labels and entry boxes
labels = ['Iron Waste (%)', 'Water (kg/m\u00b3)',
          'Coarse Aggregate (kg/m\u00b3)', 'Fine Aggregate (kg/m\u00b3)',
          'Fine Aggregate (%)', 'Age of concrete (days)']

entry_boxes = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=unicodeit.replace(label_text), font=('Times New Roman', 12, 'italic'), bg='#e9ecef', pady=5)
    canvas1.create_window(20, 120 + i * 30, anchor="w", window=label)

    entry = tk.Entry(root)
    canvas1.create_window(480, 120 + i * 30, window=entry)
    entry_boxes.append(entry)

label_output = tk.Label(root, text='Output (Compressive Strength)', font=('Times New Roman', 12,'bold'),
                        bg='#e9ecef')
canvas1.create_window(50, 520, anchor="w", window=label_output)


def values():
    # Validate and get the values from the entry boxes
    input_values = []
    for entry_box in entry_boxes:
        value = entry_box.get().strip()
        if value:
            try:
                input_values.append(float(value))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
                return
        else:
            messagebox.showerror("Error", "Please fill in all the input fields.")
            return

    # If all input values are valid, proceed with prediction
    input_data = pd.DataFrame([input_values],
                              columns=['Iron Waste (%)',	'Water', 	'Coarse Aggregate',  	'Fine Aggregate', 	
                                       'Fine Aggregate (%)',	'Age (day)'
])

    # Predict using the loaded XGBRegressor model
    prediction_result = gb_loaded.predict(input_data)
    prediction_result = round(prediction_result[0], 2)

    # Display the prediction on the GUI
    label_prediction = tk.Label(root, text=(f'{str(prediction_result)} MPa'), font=('Times New Roman', 20, 'bold'), bg='brown')
    canvas1.create_window(280, 520, anchor="w", window=label_prediction)


button1 = tk.Button(root, text='Predict', command=values, bg='#4285f4', fg='white', font=('Times New Roman', 12,'bold'),
                    bd=3, relief='ridge')
canvas1.create_window(450, 520, anchor="w", window=button1)

# def save_canvas():
#     # Save the canvas as a postscript file
#     canvas1.postscript(file="canvas_interface.ps", colormode="color")

# # Create a button to save the canvas
# button_save = tk.Button(root, text='Save Canvas', command=save_canvas, bg='#4285f4', fg='white', font=('Times New Roman', 12, 'bold'), bd=3, relief='ridge')
# canvas1.create_window(20, 520, anchor="w", window=button_save)

# def save_canvas():
#     # Create a figure to represent the tkinter interface
#     figure = plt.Figure(figsize=(7, 7), dpi=100)
#     FigureCanvasAgg(figure).draw()

#     # Save the figure as an image (e.g., PNG) or vector file (e.g., SVG, PDF)
#     figure.savefig("canvas_interface.png", format="png", bbox_inches='tight')

# # Create a button to save the canvas
# button_save = tk.Button(root, text='Save Canvas', command=save_canvas, bg='#4285f4', fg='white', font=('Times New Roman', 12, 'bold'), bd=3, relief='ridge')
# canvas1.create_window(20, 520, anchor="w", window=button_save)

root.mainloop()
