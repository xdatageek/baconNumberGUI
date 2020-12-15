import tkinter,json
from tkinter.filedialog import Tk,Frame,Button,Listbox,Scrollbar,askopenfile
from tkinter.messagebox import showinfo
import utils 

app = Tk()
ActorWithActors = {}
ActorWithFilms = {}
FilmsWithYears = {}

def load_data():
    opened_file = askopenfile(defaultextension=".json", filetypes=[("All types", ".json")])
    read_json = json.loads(opened_file.read())
    list_box.delete(0, tkinter.END)

    for item in read_json:
        list_box.insert(tkinter.END, item['name'])
        films = ''
        for film in item['films']:
            films = "{},,{}".format(films, film['title'])

            if film['title'] not in FilmsWithYears.keys():
                FilmsWithYears[film['title']] = film['year']

        ActorWithActors[item['name']] = utils.get_actors(read_json, item['films'], item['name'])
        ActorWithFilms[item['name']] = films.split(',,')[1:]


def find_bacon_number():
    selected = list_box.curselection()

    if list_box.size() and len(selected):
        result = utils.create_result(ActorWithFilms, ActorWithActors, FilmsWithYears, selected[0])
        showinfo("Bacon Number", result)
    return


f = Frame()
f.pack(side=tkinter.LEFT, padx=30)

Button(f, text="Upload JSON", command=load_data).pack(fill=tkinter.X)
Button(f, text="Get Bacon Number", command=find_bacon_number).pack(fill=tkinter.X)

list_box = Listbox(width=35, height=20)
list_box.pack(side=tkinter.RIGHT)
scroll = Scrollbar(command=list_box.yview())
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
list_box.config(yscrollcommand=scroll.set)

app.mainloop()
