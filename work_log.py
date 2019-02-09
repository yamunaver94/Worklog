import csv
import datetime
import os
import re
import sys
import time
from textwrap import dedent


def main():
    """ Prints a menu choice and directs to corresponding function"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(dedent("""
        WORK log
        What would you like to do?
        a) Add new entry
        b) Search in existing entries
        c) Quit program"""))
    choice = input("> ")

    if choice == "a":
        return add()
    elif choice == "b":
        try:
            with open('log.csv', newline='\n') as work_log:
                log_reader = csv.reader(work_log, delimiter=',')
        except:
            print("No entries to search. Add entries.")
            time.sleep(2)
            return main()
        return search()
    elif choice == "c":
        print("Thanks for using WORK LOG!")
        sys.exit()
    else:
        print("Please enter a, b or c.")
        time.sleep(3)
        return main()


def add():
    """ Takes input for new entry and passes to to_csv as a list"""
    try:
        date = input(str("Enter date of the task, use DD/MM/YYYY: "))
        date_test = datetime.datetime.strptime(date, '%d/%m/%Y')
    except:
        print("Must be in correct DD/MM/YYYY format.")
        return add()
    while True:
        title = input("Enter the title of this task: ")
        try:
            if title == "":
                raise ValueError("Please enter a valid string.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    while True:
        duration = input("Enter the duration of this task in minutes: ")
        try:
            if not duration.isdigit():
                raise ValueError("Please enter a valid integer.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    notes = input("Enter any notes (optional): ")
    new_entry = [date, title, duration, notes]
    return to_csv(new_entry)


def to_csv(new_entry):
    """ Appends new entry to log.csv """
    with open('log.csv', 'a') as csvfile:
        entrywriter = csv.writer(csvfile)
        entrywriter.writerow(new_entry)
    return main()


def search():
    """ Presents user with search menu and directs to corresponding function"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(dedent("""
        What do you want to search by?
        a) Exact date
        b) Range of dates
        c) Time spent
        d) Exact search
        e) Regex pattern
        f) Return to main menu
        """))
    choice = input("> ")

    if choice == "a":
        return search_date_exact()
    elif choice == "b":
        return search_date_range()
    elif choice == "c":
        return search_time_spent()
    elif choice == "d":
        return search_exact()
    elif choice == "e":
        return search_pattern()
    elif choice == "f":
        return main()
    else:
        print("Please enter a valid choice")
        time.sleep(3)
        return search()


def search_date_exact():
    """ Searches for entries given exact date. Returns a list of results """
    results = []
    exact_date = input("Enter date to search (DD/MM/YYYY): ")
    try:
        exact_date_test = datetime.datetime.strptime(exact_date, '%d/%m/%Y')
    except:
        print("Must be in correct DD/MM/YYYY format.")
        return search_date_exact()
    with open('log.csv', newline='\n') as work_log:
        log_reader = csv.reader(work_log, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            if row[0] == exact_date:
                results.append(row)
    if len(results) > 0:
        return view_results(results)
    else:
        print("No results found.")
        time.sleep(3)
        return search()


def search_date_range():
    """ Searches for entries given date range. Returns a list of results """
    results = []
    os.system('cls' if os.name == 'nt' else 'clear')
    start_date = input("Enter beginning date to search (DD/MM/YYYY): ")
    end_date = input("Enter end date to search (DD/MM/YYYY): ")
    try:
        start_date_test = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        start_date_ts = start_date_test.timestamp()
        end_date_test = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        end_date_ts = end_date_test.timestamp()
    except:
        print("Must be in correct DD/MM/YYYY format.")
        return search_date_range()

    with open('log.csv', newline='\n') as work_log:
        log_reader = csv.reader(work_log, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            entry_date = datetime.datetime.strptime(row[0], '%d/%m/%Y')
            entry_date_ts = entry_date.timestamp()
            if entry_date_ts <= end_date_ts and entry_date_ts >= start_date_ts:
                results.append(row)
    if len(results) > 0:
        return view_results(results)
    else:
        print("No results found.")
        time.sleep(3)
        return search()


def search_time_spent():
    """ Searches for entries given duration. Returns a list of results """
    results = []
    os.system('cls' if os.name == 'nt' else 'clear')
    duration = input("Enter duration to search for: ")
    with open('log.csv', newline='\n') as work_log:
        log_reader = csv.reader(work_log, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            if row[2] == duration:
                results.append(row)
    if len(results) > 0:
        return view_results(results)
    else:
        print("No results found.")
        time.sleep(3)
        return search()


def search_exact():
    """ Searches for entries given any string. Returns a list of results """
    results = []
    os.system('cls' if os.name == 'nt' else 'clear')
    exact_string = input("Enter string to search for: ")
    with open('log.csv', newline='\n') as work_log:
        log_reader = csv.reader(work_log, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            if exact_string in row[1] or exact_string in row[3]:
                results.append(row)
    if len(results) > 0:
        return view_results(results)
    else:
        print("No results found.")
        time.sleep(3)
        return search()


def search_pattern():
    """ Searches for entries given regex pattern. Returns a list of results """
    results = []
    os.system('cls' if os.name == 'nt' else 'clear')
    pattern = input(str("Enter regex pattern to search for: "))
    with open('log.csv', newline='\n') as work_log:
        log_reader = csv.reader(work_log, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            for item in row:
                if len(re.findall(f"{pattern}", item)) > 0:
                    results.append(row)
                    break
    if len(results) > 0:
        return view_results(results)
    else:
        print("No results found.")
        time.sleep(3)
        return search()


def view_results(results):
    """ Function to show user results of chosen search """
    num_results = len(results)
    num_count = 0
    choice = None
    while choice != "e" and choice != "d" and choice != "r":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(dedent(f"""
        Date: {results[num_count][0]}
        Title: {results[num_count][1]}
        Duration: {results[num_count][2]}
        Notes: {results[num_count][3]}

        Entry {num_count+1} of {num_results}
        """))
        if num_results == 1:
            print(dedent("""
            Please make a selection:
            (e)dit (d)elete (r)eturn to menu
            """))
        else:
            if num_count == 0:
                print(dedent("""
                Please make a selection:
                (n)ext (e)dit (d)elete (r)eturn to menu
                """))
            elif num_count+1 == num_results:
                print(dedent("""
                Please make a selection:
                (p)revious (e)dit (d)elete (r)eturn to menu
                """))
            else:
                print(dedent("""
                Please make a selection:
                (p)revious (n)ext (e)dit (d)elete (r)eturn to menu
                """))
        choice = input("> ")
        if choice == "p" and num_count != 0:
            num_count -= 1
        elif choice == "n" and num_count+1 != num_results:
            num_count += 1
        elif choice == "e":
            return edit(results, num_count)
        elif choice == "d":
            return delete(results, num_count)
        elif choice == "r":
            return search()
        else:
            print("Please enter a valid choice.")
            time.sleep(3)
            return view_results(results)


def delete(results, num_count):
    """ Delets entry in CSV file """
    with open('log.csv', newline='\n') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            if row == results[num_count]:
                rows.remove(row)

    with open('log.csv', 'w') as csvfile:
        entrywriter = csv.writer(csvfile)
        for row in rows:
            entrywriter.writerow(row)
    print("Entry deleted!")
    time.sleep(2)
    return search()

def edit(results, num_count):
    """ Prompts user what part of the entry to edit, edits CSV file """
    os.system('cls' if os.name == 'nt' else 'clear')
    with open('log.csv', newline='\n') as csvfile:
        log_reader = csv.reader(csvfile, delimiter=',')
        rows = list(log_reader)
        for row in rows:
            if row == results[num_count]:
                print(dedent(f"""
                Date: {results[num_count][0]}
                Title: {results[num_count][1]}
                Duration: {results[num_count][2]}
                Notes: {results[num_count][3]}

                Which field would you like to edit?
                (D)ate, (T)itle, D(u)ration, (N)otes
                """))
                choice = input("> ")
                if choice == "D":
                    while True:
                        edit_val = input("Enter new value: ")
                        try:
                            edit_val = datetime.datetime.strptime(edit_val,
                            '%d/%m/%Y')
                            edit_val = edit_val.strftime("%d/%m/%Y")
                        except:
                            print("Must be in correct DD/MM/YYYY format.")
                        else:
                            break
                    row[0] = edit_val
                elif choice == "T":
                    edit_val = input("Enter new value: ")
                    row[1] = edit_val
                elif choice == "u":
                    while True:
                        duration = input("Enter new value: ")
                        try:
                            if not duration.isdigit():
                                raise ValueError(
                                "Please enter a valid integer.")
                        except ValueError as err:
                                print(f"Whoops! {err}")
                        else:
                            break
                    row[2] = duration
                elif choice == "N":
                    edit_val = input("Enter new value: ")
                    row[3] = edit_val
                else:
                    print("Please enter a valid choice.")
                    time.sleep(1)
                    return edit(results, num_count)

    with open('log.csv', 'w') as csvfile:
        entrywriter = csv.writer(csvfile)
        for row in rows:
            entrywriter.writerow(row)
    return search()


if __name__ == '__main__':
    main()
