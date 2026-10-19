# A PC part manager.
import pyttsx3
import csv

engine = pyttsx3.init()
FILE_NAME = "partDatabase.csv"

def speak(words):
    # Use this to add speech to your methods
    engine.say(words)
    engine.runAndWait()

def writeParts(my_parts):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(my_parts)

def readParts():
    my_parts = []
    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.reader(file)
            for line in reader:
                my_parts.append(line)
    except FileNotFoundError:
        writeParts(my_parts)
    return my_parts
    
def removeParts(my_pc_parts):
    speak("Remove a Part")
    part_number = int(input("Enter Part Number to Remove: "))
    if part_number < 1 or part_number > len(my_pc_parts):
        print("Invalid part number. \n")
    else:
        my_part = my_pc_parts.pop(part_number - 1)
        writeParts(my_pc_parts)
        print(f"{my_part[0]} was removed.\n")

def addParts(my_pc_parts):
    speak("Add a Part")
    
    category = input("Enter PC part category: ").strip()
    while category == "":
        print("Category cannot be blank.")
        category = input("Enter PC part category: ").strip()

    match category.lower():
        case "cpu":
            example = "AMD Ryzen 5 7600X"
        case "gpu":
            example = "NVIDIA GeForce RTX 4060"
        case "motherboard":
            example = "Gigabyte B650 AORUS Elite AX"
        case "power supply" | "powersupply" | "psu":
            example = "Corsair RM750e"
        case "ram":
            example = "Corsair Vengeance 32GB DDR5"
        case "storage" | "ssd" | "hdd":
            example = "Samsung 990 PRO 1TB"
        case _:
            example = "brand and model"

    name = input(f"Enter component name (e.g., {example}): ").strip()
    cost = input("Cost of Part: ").strip()
    quantity = input("Quantity: ").strip()
    
    # Stored as [category, name, cost, quantity]
    new_part = [category, name, cost, quantity]
    my_pc_parts.append(new_part)
    writeParts(my_pc_parts)
    print(f"{name} ({category}) was added.\n")

def listParts(my_pc_parts):
    speak("Listing all Parts")
    if len(my_pc_parts) == 0:
        print("There are no PC Parts in the list.\n")
    else:
        i = 1
        for my_part in my_pc_parts:
            # Check if the row has the new 4-item format or old 3-item format
            if len(my_part) >= 4:
                print(f"{i}. [{my_part[0]}] {my_part[1]} | Cost: ${my_part[2]} | Qty: {my_part[3]}")
            else:
                # Fallback for old data in your CSV
                print(f"{i}. [Uncategorized] {my_part[0]} | Cost: ${my_part[1]} | Qty: {my_part[2]}")
            i = i + 1
        print()

def updatePartListing(my_pc_parts):
    speak("Update your Parts")
    part_number = int(input("Enter Part Number to Update: "))
    if part_number < 1 or part_number > len(my_pc_parts):
        print("Your Part number is invalid.\n")
    else:
        category = input("New Category: ").strip()
        name = input("New Name of Part: ").strip()
        cost = input("New Cost of Part: ").strip()
        quantity = input("New Quantity: ").strip()
        
        updated_part = [category, name, cost, quantity]
        my_pc_parts[part_number - 1] = updated_part
        writeParts(my_pc_parts)
        print(f"{name} was updated.\n")
    

def listCommands():
    print(f"list - List Parts\n"
          f"update - Update Parts\n"
          f"add - Add Parts\n"
          f"remove - Remove Parts\n"
          f"exit - Exit the Program\n")

def main():
    print(f"PC Part Manager:\n")
    listCommands()
    speak("PC Part Manager")
    my_pc_parts = readParts()

    while True:
        entry = input("Enter in a command: ").strip().lower()

        match entry.lower():
            #Added shortened alternatives for faster testing.
            case "add" | "a":
                addParts(my_pc_parts)

            case "list" | "l":
                listParts(my_pc_parts)

            case "update" | "u":
                updatePartListing(my_pc_parts)

            case "remove" | "r":
                removeParts(my_pc_parts)
            case "exit" | "e":
                speak("GoodBye!")
                print("GoodBye!")
                break

            case _:
                # Made error red showing in terminal
                print(f"Invalid command: \033[31m{entry}\033[0m:\n"
                    f"Try Again\n\n\n")
                speak(f"{entry} is an invalid command. Try Again ")


if __name__ == '__main__':
    main()