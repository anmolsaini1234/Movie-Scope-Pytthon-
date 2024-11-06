import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
import tkinter as tk
from PIL import Image, ImageTk 

movieNames = []


window = tk.Tk()
window.title("Netflix Analysis")
window.geometry('1280x720')


background_image = Image.open("image.png")  
bg_image = ImageTk.PhotoImage(background_image)

bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  

def onClick(c):
    print(c)
    url = f"https://api.themoviedb.org/3/movie/{c}?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNDJkM2MyNjY1ZGY5YWI5MGM1NTE3ZGQyOGRiZTkwMCIsIm5iZiI6MTcyOTY4OTA0Ny44MDY2NTksInN1YiI6IjY3MThmNTY1YTRhYzhhNDMyYzViZGM2YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ybaa-tRcN1DEmlrlwT2Ia-bHTExceD5uWLoCobNdRbc"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    movies = data["results"]

    for i in movies:
        movieNames.append(i['original_title'])
       

    release_years = [datetime.datetime.strptime(movie["release_date"], "%Y-%m-%d").year for movie in movies]
    hist_window = tk.Toplevel(window)
    hist_window.title("Top Rated Movies Release Year Histogram")

    fig, ax = plt.subplots()
    ax.hist(release_years, bins=10, edgecolor='black')
    ax.set_title("Distribution of Movie Release Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")

    canvas = FigureCanvasTkAgg(fig, master=hist_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    hist_window.mainloop()


main_frame = tk.Frame(window, bg="lightgrey", bd=10)
main_frame.place(relx=0.5, rely=0.5, anchor="center")


label = tk.Label(main_frame, text="Welcome to Netflix Analysis", font=("Arial", 24, "bold"), fg='red', bg='black')
label.pack(pady=20)


button_frame = tk.Frame(main_frame, bg="lightgrey")
button_frame.pack(pady=10)

categories = ["top_rated", "popular", "upcoming"]
for category in categories:
    button = tk.Button(button_frame, text=category.replace("_", " ").title(), font=("Arial", 14), width=15, height=2, 
                       command=lambda c=category: onClick(c), bg="#4CAF50", fg="white")
    button.pack(side="left", padx=10)

window.mainloop()
