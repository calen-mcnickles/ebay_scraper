from tkinter import *
import main

"""
Basic GUI for the scraper. 
"""

window = Tk()
window.title("Ebay Scraper")
window.minsize(width=500, height=200)
window.config(padx=20, pady=20)

title = Label(text="EbayScraper", font=("Arial", 20, "bold"))
title.grid(column=0, row=0)

output_label = Label(text="Output CSV", )
output_label.grid(column=0, row=1)

input_label = Label(text="Keywords", )
input_label.grid(column=1, row=1)

max_price_label = Label(text="Max Price", )
max_price_label.grid(column=2, row=1)

pages_to_scrape_label = Label(text="# of pages to scrape", )
pages_to_scrape_label.grid(column=3, row=1)

output_csv = Entry()
output_csv.insert(END, string="ex. output.csv")
output_csv.grid(column=0, row=2)

search_title = Entry()
search_title.insert(END, string="ex. pokemon cards")
search_title.grid(column=1, row=2)

max_price = Entry()
max_price.insert(END, string="ex. 100")
max_price.grid(column=2, row=2)

pages_to_scrape = Entry()
pages_to_scrape.insert(END, string="ex. 2")
pages_to_scrape.grid(column=3, row=2)


# Radio button
def radio_used():
    print(radio_state.get())
    return radio_state.get()


def run_scraper():
    main.ebay_scraper_keyword(output_csv.get(), search_title.get(), int(max_price.get()), int(pages_to_scrape.get()),
                              radio_used())


radio_state = BooleanVar()
radio_active = Radiobutton(text="Active", value=False, variable=radio_state, command=radio_used)
radio_sold = Radiobutton(text="Sold", value=True, variable=radio_state, command=radio_used)
radio_active.grid(column=4, row=2)
radio_sold.grid(column=5, row=2)

run_but = Button(text="Run", command=run_scraper)
run_but.grid(column=6, row=2)

window.mainloop()
