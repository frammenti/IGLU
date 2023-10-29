libretto = 'libretto.txt'

import copy
from datetime import datetime
from datetime import date

# DEFINITION OF CLASS AND OPERATIONS
# Class of object exam
class exam:
    data = None
    def __init__(self, year, name, cfu, grade, date):
        self.year = year
        self.name = name
        self.cfu = cfu
        self.grade = grade
        self.date = date

# Function to print data in tabular format
def print_table(table):
    print("\n{0:^55}{1:^7}{2:^12}{3:^12}".format("Esame", "Crediti", "Voto", "Data"))
    for row in table:
        if row[0] in years_to_int.keys():
            print("\n{0:<2}{1:<24}".format("", row[0]))
        elif not row[0] == "":
            print("{0:>55.53}{1:^7}{2:^12}{3:^12}".format(row[1], row[2], row[3], row[4]))

# Function to print lists of 2+ elements with commas and 'and'
def comma(abc):
    str1 = ""
    for i in abc[0:-2]:
        str1 += i+', '
    str2 = abc[-2] + " e " + abc[-1] # second last and last string are separated with 'and'
    return str1+str2

# Average
def average(record_avg):
    n = 0
    d = 0
    for obj in record_avg:
        if isinstance(obj.grade, int):
            n += obj.grade
            d += 1
    return round(n/d, 1)

# Weighted average
def waverage(record_avg):
    n = 0.00
    d = 0.00
    for obj in record_avg:
        if isinstance(obj.grade, int):
            n += obj.grade*obj.cfu
            d += obj.cfu
    return round(n/d, 2)

# On \110 base
def graduation(func):
    graduation = round(func*11/3)
    return graduation

# IGLU judges your grades
def judging(record_avg):
    if waverage(record_avg) <= 27:
        return "Mi fa pena"
    elif waverage(record_avg) <= 29:
        return "Niente male"
    else:
        return "Che noia"

# Cum laude counter
def cum_laude(record):
    num_laude = phrases.count('30 con Lode')
    if num_laude == 0:
        return "e nessuna lode"
    elif num_laude == 1:
        return "e una lode"
    else:
        return f'e {str(num_laude)} lodi'

# Median
def median(record_avg):
    half = round(len(grades)/2) # 0.5 rounded gives 1
    if len(grades) % 2 == 0: # is even
        median = (grades[half-1] + grades[half])/2
    else:
        median = grades[half]
    return median

# Mode
def mode(record_avg):
    # Create a dictionary with grades as keys and frequencies as values
    count = {}
    # Iteration through grades list, frequency is increased by 1 each time the same grade is met
    for grade in grades:
        count[grade] = count.get(grade, 0) + 1
    # Dictionary is converted to a list of tuples by items() and sorted for descending frequency (second element of tuple = tup[1])
    freqs = sorted(count.items(), key=lambda tup: tup[1], reverse=True)
    # Return mode and frequency
    mode = freqs[0][0] # most common grade
    mfreq = freqs[0][1] # most common grade frequency
    perc = round(mfreq*100/sum(freq for grade, freq in freqs)) # percentage is calculated without "qualified" grades
    if mfreq >= 2:
        return f'\nFioccano i {str(mode)}: ne ha presi ben {str(mfreq)}, il {str(perc)}% sul totale degli esami.'
    else:
        return ""

# Best year
def best_year(record):
    # Sum of all cfu recorded in the course of studies (with "qualified" grades)
    cfu_tot = 0
    for obj in record:
        cfu_tot += obj.cfu 
        try:
            obj.date = obj.date.year # carry only year from date object
        except:
            pass
    # Create list of tuples with date (actual year of record), cfu and academic year for each exam
    cfu_list = [(obj.date,obj.cfu,obj.year) for obj in record if obj.name != 'Prova finale' and obj.name != 'Final examination']
    # Create a dictionary cy (cfu per year), where each date in list is associated with a counter set to 0
    cy = {date: 0 for date, cfu, year in cfu_list}
    # Cfu recorded in that year are added to the counter
    for date, cfu, year in cfu_list:
        cy[date] += cfu
    # Convert dictionary with paired year and cfu per year to list of tuples
    cy_list = list(map(tuple, cy.items()))
    # Sort for second element (cfu per year) of tuple
    cy_list.sort(key=lambda tup: tup[1], reverse=True)
    # If most cfu are not associated to a year, a warning message is printed and that tuple is removed from the statistics
    if type(cy_list[0][0]) != int:
        del cy_list[0]
        first_message = f"Pare che la maggior parte degli esami non sia stata ancora sostenuta o derivi da un passaggio di Corso. Ad ogni modo...\n"
    else:
        cy_list = [(date, cy) for date, cy in cy_list if type(date) == int] # blank year tuple is removed from list
        first_message = "" # no message printed
    # Different messages if a single year has most cfu or there is a tie
    if cy_list[0][1] == cy_list[1][1]: # if first year has same cfu as second year
        best_list = [(date, cy) for date, cy in cy_list if cy == cy_list[0][1]] # list of years in tie
        best_years = sorted([str(date) for date, cy in best_list])
        best_cy = cy_list[0][1] # cfu recorded in best years
        second_message = f"I Suoi anni più produttivi sono stati a pari merito {comma(best_years)}, in ciascuno dei quali ha conseguito {str(best_cy)} crediti.\n"
    else:
        best_year = cy_list[0][0] # year with most cfu
        best_cy = cy_list[0][1] # cfu recorded in best year
        year_list = [(date, cfu, year) for date, cfu, year in cfu_list if date == best_year] # list of grades recorded in best year
        best_exn = len(year_list) # number of exams in best year
        ay_list = [year for date, cfu, year in year_list] # academic years of exams in best year
        # Create a dictionary with academic years as keys and frequencies as values
        count = {}
        # Iteration through ay_list, frequency is increased by 1 each time the same academic year is met
        for ay in ay_list:
            count[ay] = count.get(ay, 0) + 1
        # Dictionary is converted to a list of tuples by items() and sorted for descending frequency (second element of tuple = tup[1])
        freqs = sorted(count.items(), key=lambda tup: tup[1], reverse=True)
        best_ay_list = [ay for ay, freq in count.items() if freq == freqs[0][1]] # list of most frequent academic years
        best_ay = ' e '.join(str(ay) for ay in best_ay_list)
        for key, value in years_to_str.items():
            best_ay = best_ay.replace(key, value)
        second_message = f"Il Suo anno più produttivo è stato il {str(best_year)}, nel quale ha conseguito {str(best_cy)} crediti sui {str(cfu_tot)} del Suo Corso di Studi.\nIn quell'anno ha superato {str(best_exn)} esami, afferenti per la maggior parte al {best_ay} Anno Accademico."
    return f'{first_message}{second_message}'

# Best exam
def best_exam(record_rank):
    num_laude = [grade for grade, name in rank].count(31) # number of cum laude
    best_exam = [name for grade, name in rank if grade == rank[0][0]]
    best_grade = rank[0][0]
    exam_list = '\n'.join(best_exam)
    if num_laude > 3: return f"Lei è proprio un geniaccio. Altro che miglior esame, a momenti la lista dei Suoi 30 e Lode esce dallo schermo:\n\n{exam_list}.\n"
    elif num_laude >= 2: return f"Ma che genietto, ha messo nel sacco dei 30 e Lode negli esami di {comma(best_exam)}."
    elif num_laude == 1: return f"Ha assaporato il nettare della perfezione in una singola, indimenticabile occasione, l'esame di {best_exam[0]}, nel quale ha preso 30 e Lode."
    elif best_grade == rank[3][0]: return f"Che mediocrità, può solo invidiare dall'imo l'Olimpo della perfezione. Tuttavia, ha preso vari {best_grade} nei seguenti esami:\n\n{exam_list}.\n"
    elif best_grade == rank[1][0]: return f"Vive talmente immerso nella mediocrità da non conoscere nient'altro. I Suoi esami migliori sono {comma(best_exam)}, nei quali ha preso {best_grade}."
    else: return f"Spero per Lei che il suo Corso di Laurea sia molto difficile, perché il suo voto migliore è un signolo, misero {best_grade} nell'esame di {best_exam[0]}."

# Worst exam
def worst_exam(record_rank):
    wrank = sorted(rank)
    worst_exam = [name for grade, name in wrank if grade == wrank[0][0]]
    worst_grade = wrank[0][0]
    exam_list = '\n'.join(worst_exam)
    if worst_grade <= 22: first_message = f"Se ha accettato un voto del genere, un {worst_grade}, non c'è speranza per Lei."
    elif worst_grade <= 24: first_message = f"Mi disgusta, ha accettato un infimo {worst_grade}."
    elif worst_grade <= 26: first_message = f"Non è così perfetto come sembra se ha accettato un {worst_grade}."
    elif worst_grade <= 29: first_message = f"Mi immagino la Sua faccia quando Le hanno dato quel {worst_grade}."
    else: first_message = f"Lei è maniacale. Mai una scivolata, mai una sbavatura, mai un'incertezza. Solo 30"
    if worst_grade == 30:
        if worst_grade == wrank[3][0]: second_message = f", sebbene alcuni senza Lode negli esami di: \n\n{exam_list}\n"
        elif worst_grade == wrank[1][0]: second_message = f", sebbene alcuni senza Lode negli esami di {comma(worst_exam)}."
        else: second_message = f", sebbene in un singolo esame, {worst_exam[0]}, non abbia preso la Lode."
    elif worst_grade == 31: second_message = " e Lode in tutti gli esami. Impressionante."
    elif worst_grade == wrank[3][0]: second_message = f" Ed è stato pure recidivo, questi gli esami incriminati:\n\n{exam_list}\n" 
    elif worst_grade == wrank[1][0]: second_message = f" Si è macchiato di tale colpa negli esami di {comma(worst_exam)}."
    else: second_message = f" L'esame di {worst_exam[0]} è da dimenticare."
    return f"{first_message}{second_message}"

# DICTIONARIES
# Definition of inputs
yes_choices = ['sì', 'si', 's', 'ok', 'o']
no_choices = ['no', 'n']
exit = ['e', 'exit', 'a', 'arrivederla']

# Dictionary of error messages
errormsg = {}
errormsg['type'] = "Temo che il caricamento del Suo Libretto sia fallito a causa dell'inconsistenza dei dati nel file di testo. Verifichi la congruenza con il modello atteso e riprovi. Arrivederci"
errormsg['index'] = "Temo che il caricamento del Suo libretto sia fallito perché non è stato nemmeno in grado di selezionare il testo seguendo le istruzioni. Ritenti o magari si faccia aiutare."
errormsg['filenotfound'] = "Temo che non abbia neanche capito come creare un banalissimo file di testo nella cartella giusta. Ci rinuncio."
errormsg['exception'] = "Non è facile sorprendermi, ma con la Sua stupidità c'è riuscito. Complimenti."
errormsg['yearnotfound'] = "Mancano gli anni accademici, mi dica un po' Lei perché sta sprecando il mio tempo. Vada al diavolo!"
errormsg['zerodivision'] = "Pare che abbia caricato un libretto senza alcun esame. Un genio."

# Dictionary to replace academic year with integer
years_to_int = {
    'Primo anno di corso': '1',
    'Secondo anno di corso': '2',
    'Terzo anno di corso': '3',
    'Quarto anno di corso': '4',
    'Quinto anno di corso': '5',
    'Sesto anno di corso': '6',
}

# Dictionary for best year answer
years_to_str = {
    '1': 'primo',
    '2': 'secondo',
    '3': 'terzo',
    '4': 'quarto',
    '5': 'quinto',
    '6': 'sesto',
}

# Create menu as dictionary
menu = {}
menu['0']="Riepilogo sinottico della carriera" 
menu['1']="Media" 
menu['2']="Media ponderata"
menu['3']="Voto mediano"
menu['4']="Anno più produttivo per crediti"
menu['5']="Miglior esame"
menu['6']="Peggior esame"


# ---------------------------------------------- MAIN

# FIRST INTERACTION
# Ask if first time
print("Benvenuto nell'Interfaccia di Gestione del Libretto Universitario, può chiamarmi IGLU.")
# If 'yes' proceed, if 'no' explanation
while True:
    user_input = input("È già aduso al servizio? (sì/no):\n")
    if user_input.lower() in yes_choices:
        print("La ringrazio infinitamente per la fiducia accordatami.\nCaricamento...")
        break
    elif user_input.lower() in no_choices:
        print("Sarò onorato di aiutarLa a ripercorrere la Sua preclara gloria accademica.\nTroverà il Suo libretto su Studenti Online seguendo il percorso:\n\nHome > Libretto online > Dettaglio carriera\n\nLa prego di selezionare l'intera tabella da 'Dettaglio carriera' all'ultima data e di copiarne il contenuto su un file 'libretto.txt', avendo cura di riporlo nella stessa directory nella quale mi trovo.")
        # Record is loaded only after positive answer
        while True:
            user_input = input("Quando se la sente è pregato di digitare 'ok':\n")
            if user_input.lower() in yes_choices:
                print("Era ora. Caricamento...")
                break
            else:
                print("Non stiamo scherzando qui.")
                continue
        break # After 'ok' first question is not repeated
    else:
        print("Quanta ignoranza. Non si aspetterà di certo un sinonimo.")
        continue

# IMPORT TABLE, CHECK AND DATA CLEANING
try:
    file = open(libretto, 'r', encoding="utf-8")
except FileNotFoundError as err:
    raise SystemExit(errormsg['filenotfound']) # Error if file not found
exam_list = []
# Iter through table for data cleaning and append each row as a list to a list
for row in file:
    # Split on tab characters
    row = row.split("\t")
    try:
        del row[2] # Delete empty column
    except:
        pass
    try:
        row[2] = int(row[2]) # Convert cfu to integers
    except:
        pass
    try:
        row[3] = int(row[3]) # Convert grade to integers
    except:
        pass
    try:
        row[0] = row[0].strip() # Delete blanks in first column
    except:
        pass
    try:
        row[1] = row[1].strip() # Delete blanks in second column
    except:
        pass
    try:
        row[2] = row[2].strip() # Delete blanks in third column
    except:
        pass
    try:
        row[3] = row[3].strip() # Delete blanks in fourth column
    except:
        pass
    try:
        row[4] = row[4].strip() # Delete blanks in last column
    except:
        pass
    try:
        row[4] = datetime.strptime(row[4], "%d/%m/%Y") # Convert dates to datetime format
        row[4] = row[4].date()
    except:
        pass
    # Append to list of lists
    exam_list.append(row)

# Clean unwanted headers
if exam_list[0] == [""]:
    del exam_list[0]
if exam_list[0] == ["Dettaglio carriera"]:
    del exam_list[0]
if exam_list[0] == ['Cod.', 'Attività formativa', 'Crediti', 'Esito', 'Data verb.']:
    del exam_list[0]

# Create copy for display
table = copy.deepcopy(exam_list)
# Loop through rows to change date format and replace blanks with "-"
for row in table:
    try:
        if row[4] != "":
            row[4] = row[4].strftime("%d/%m/%Y")
        else:
            row[4] = "-"
    except:
        pass
    try:
        if row[3] == "":
            row[3] = "-"
    except:
        pass

# Nested iteration to replace literal acadamic years with integers
if exam_list[0] == ["Primo anno di corso"]:
    for key, value in years_to_int.items(): # For each dictionary entry
        for entry in exam_list: # Iter through first field of each entry looking for substitution
            if entry[0] == key:
                entry[0] = entry[0].replace(key, value)
                entry[0] = int(entry[0]) # Make the academic year number an integer
else:
    raise SystemExit(errormsg['yearnotfound']) # Error if first academic year is missing
# Replace exam codes with academic year of exam
years_list = [entry[0] for entry in exam_list] # Extract list of academic years
#Iterate through index of list to fill in the gaps between years
for i, value in enumerate(years_list): # Enumerate() pairs each value with corresponding index number i
    # If year is present, its value is replaced in other entries until next year
    if 6 in years_list and i >= years_list.index(6):
       years_list[i] = 6
    elif 5 in years_list and i >= years_list.index(5):
        years_list[i] = 5
    elif 4 in years_list and i >= years_list.index(4):
        years_list[i] = 4
    elif 3 in years_list and i >= years_list.index(3):
        years_list[i] = 3
    elif 2 in years_list and i >= years_list.index(2):
        years_list[i] = 2
    else:
        years_list[i] = 1
# Overlap years_list with exam_list
for entry in exam_list:
    # First value in entry is replaced with value from corresponding index in year_list
    entry[0] = years_list[exam_list.index(entry)]
# Single years entries are excluded from record
exam_list = [entry for entry in exam_list if len(entry) > 2]

# Create record as an array of objects where each property is filled with element of list
try:
    record = [exam(*x) for x in exam_list]
except TypeError as err:
    raise SystemExit(errormsg['type']) # Error if number of positional arguments is incorrect

# Copy of record where cum laude is removed for average
record_avg = copy.deepcopy(record)
for obj in record_avg:
    if isinstance(obj.grade, str):
        obj.grade = obj.grade.replace('30 con Lode', '30')
    try:
        obj.grade = int(obj.grade)
    except:
        pass
# Copy of record where cum laude is considered 31 for best exams
record_rank = copy.deepcopy(record)
for obj in record_rank:
    if isinstance(obj.grade, str):
        obj.grade = obj.grade.replace('30 con Lode', '31')
    try:
        obj.grade = int(obj.grade)
    except:
        pass
# Build list of ordered grades
grades = sorted([obj.grade for obj in record_avg if isinstance(obj.grade, int)])
# Build list of other phrases in grade attribute
phrases = [obj.grade for obj in record if isinstance(obj.grade, str)]
# Build tuples list for ranking
rank = sorted([(obj.grade, obj.name) for obj in record_rank if isinstance(obj.grade, int)], key=lambda entry: entry[0], reverse=True)

# Check if average is computable
try:
    waverage(record_avg)
except ZeroDivisionError as err:
    raise SystemExit(errormsg['zerodivision'])

# SECOND INTERACTION
# Looping menu
print("\nBenissimo, cosa posso fare per Lei quest'oggi? Può scegliere tra:\n")
options=menu.keys()
for entry in options:
    print(entry, menu[entry])
while True: 
    user_input = input("\nDigiti il numero corrispondente, prego, oppure può scrivere 'Arrivederla' per uscire.\nSono sicuro che lo Stimato Utente ci tenga alle buone maniere.\n") 
    if user_input == '0':
        print_table(table)
        print(f'\nEcco il riepilogo della Sua carriera, ma questo Lei lo conosceva già.\nPosso produrre per Lei ogni genere di statistica:',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '1':
        print(f'\nAh, la media, la più banale delle operazioni. Posso fare di meglio, ad ogni modo la Sua media è di {average(record_avg)}.\nMi metta alla prova:',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '2':
        print(f'\nSiamo ansiosetti, eh? Da questa media dipenderà il Suo voto di Laurea.\nVediamo, {waverage(record_avg)} su 30. {judging(record_avg)}, si presenta alla discussione della Tesi con un punteggio di {graduation(waverage(record_avg))} su 110 {cum_laude(record)}.\nAncora!',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '3':
        print(f'\nIl Suo voto mediano è {median(record_avg)}, ma non si monti la testa: la Sua vita in Università sarà un rincorrere asintoticamente la perfezione.{mode(record_avg)}',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '4':
        print(f'\n{best_year(record)}\nSe solo me lo permettesse, potrei dirLe molto di più:',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '5':
        print(f'\n{best_exam(record_rank)}\nAvanti, non sia pavido:',end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input == '6':
        print(f"\n{worst_exam(record_rank)}\nDemoralizzato? Bene. Mi lasci infierire ancora un po':",end='\n\n')
        for entry in options:
            if entry != user_input:
                print(entry, menu[entry])
    elif user_input.lower() in exit:
        raise SystemExit("Arrivederci.")
    else: 
        print("\nForse non ci siamo intesi. Magari questa sarà la volta buona.")
