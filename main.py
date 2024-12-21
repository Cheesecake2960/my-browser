import tkinter as tk
import tkinter.messagebox
import urllib.parse
import requests
import json
import bs4
import re

def tag_to_tk_label(tag: bs4.element.Tag) -> tk.Label | None:
    with open('tags.json') as f:
        tags_setting = json.load(f)
    for tag_setting in tags_setting:
        if tag_setting['name'] == tag.name:
            if tag.find_all():
                return None
            label = tk.Label(elements,text=tag.text,font=("Arial",tag_setting['font-size']))
            if tag.name == 'a' and tag.get('href'):
                label.config(fg='blue', cursor='hand2')
                label.bind("<Button-1>", lambda e: jump_to_url(tag.get('href')))
            return label
    return None

def get_page(e) -> list[tk.Label]:
    url = address_bar.get()
    try:
        soup = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')
    except requests.exceptions.RequestException:
        tkinter.messagebox.showerror('Error', 'Failed to get the page')
    tags = []
    for elm in soup.find_all():
        tags.append(tag_to_tk_label(elm))
    for tag in tags:
        if tag:
            tag.pack()

def jump_to_url(jump_url):
    global elements
    elements.destroy()
    elements = tk.Frame(root)
    elements.pack()
    if re.search(r"^https?://", jump_url):
        new_url = jump_url
    else:
        new_url = urllib.parse.urljoin(address_bar.get(),jump_url)

    address_bar.delete(0, tk.END)
    address_bar.insert(0, new_url)
    get_page(new_url)

root = tk.Tk()
root.title('Look')
root.state("zoomed")

address_bar = tk.Entry(width=200)
address_bar.insert(0, "https://example.com")
address_bar.pack()
address_bar.bind("<Return>",get_page)

elements = tk.Frame(root)
elements.pack()

root.mainloop()