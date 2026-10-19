# A PC part manager.
# Lets the user add, list, update, and remove PC parts from the command line.
# Parts are saved to a CSV file so they persist between runs, and the program
# reads key actions aloud using text-to-speech.
import pyttsx3
import csv

# Text-to-speech engine shared by the whole program
engine = pyttsx3.init()
# CSV file where the parts list is stored
FILE_NAME = "partDatabase.csv"

def speak(words):
    # Use this to add speech to your methods
    engine.say(words)
    engine.runAndWait()

def writeParts(my_parts):
    # Overwrite the CSV with the current parts list (one row per part)
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(my_parts)

def readParts():
    # Load every saved part from the CSV into a list of rows.
    # If the file doesn't exist yet, creates an empty one and start fresh.
    my_parts = []
    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.reader(file)
            for line in reader:
                # Skip blank or incomplete rows so they can't crash listParts
                if len(line) >= 3:
                    my_parts.append(line)
    except FileNotFoundError:
        writeParts(my_parts)
    return my_parts

def getPartNumber(prompt, my_pc_parts):
    # Ask for a part number from the list; returns None if it isn't valid
    try:
        part_number = int(input(prompt).strip())
    except ValueError:
        return None
    if part_number < 1 or part_number > len(my_pc_parts):
        return None
    return part_number

def getText(prompt):
    # Keep asking until something other than blank is entered
    text = input(prompt).strip()
    while text == "":
        print("This field cannot be blank.")
        text = input(prompt).strip()
    return text

def getQuantity(prompt):
    # Keep asking until the quantity is a whole number of at least 1
    while True:
        try:
            quantity = int(input(prompt).strip())
        except ValueError:
            quantity = 0
        if quantity >= 0:
            return quantity
        print("Quantity must be a whole number of at least 0.")

def removeParts(my_pc_parts):
    # Remove a part by its number as shown in the list
    speak("Remove a Part")
    part_number = getPartNumber("Enter Part Number to Remove: ", my_pc_parts)
    if part_number is None:
        print("Invalid part number. \n")
    else:
        my_part = my_pc_parts.pop(part_number - 1)
        writeParts(my_pc_parts)
        # The name is at index 1 in the 4-item format, index 0 in the old 3-item format
        name = my_part[1] if len(my_part) >= 4 else my_part[0]
        print(f"{name} was removed.\n")

def getCost(prompt):
    # Keep asking until the cost is a valid non-negative number
    while True:
        # Allow an optional leading "$" (e.g., "$199.99")
        try:
            cost = float(input(prompt).strip().lstrip("$"))
        except ValueError:
            cost = -1
        # Also rejects infinity
        if 0 <= cost < float("inf"):
            return cost
        print("Cost must be a non-negative number (e.g., 199 or 199.99).")

def addParts(my_pc_parts):
    speak("Add a Part")

    # Category is required, so re-prompt until something is entered
    category = getText("Enter PC part category: ")

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

    # Collects the rest of the part details
    name = getText(f"Enter component name (e.g., {example}): ")
    cost = getCost("Cost of Part: ")
    quantity = getQuantity("Quantity: ")

    # Stored as [category, name, cost, quantity]
    new_part = [category, name, cost, quantity]
    my_pc_parts.append(new_part)
    writeParts(my_pc_parts)
    print(f"{name} ({category}) was added.\n")

def listParts(my_pc_parts):
    # Print every part as a numbered list; these numbers are what
    # update and remove ask for
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
    # Replace an existing part (chosen by its list number) with new details
    speak("Update your Parts")
    part_number = getPartNumber("Enter Part Number to Update: ", my_pc_parts)
    if part_number is None:
        print("Your Part number is invalid.\n")
    else:
        # Ask for all new values; the old entry is fully overwritten
        category = getText("New Category: ")
        name = getText("New Name of Part: ")
        cost = getCost("New Cost of Part: ")
        quantity = getQuantity("New Quantity: ")

        # Swap in the updated part at the same position and save
        updated_part = [category, name, cost, quantity]
        my_pc_parts[part_number - 1] = updated_part
        writeParts(my_pc_parts)
        print(f"{name} was updated.\n")


def listCommands():
    # Show the menu of available commands
    print(f"list - List Parts\n"
          f"update - Update Parts\n"
          f"add - Add Parts\n"
          f"remove - Remove Parts\n"
          f"exit - Exit the Program\n")

def main():
    # Show the menu, greet the user, and load saved parts from the CSV
    print(f"PC Part Manager:\n")
    listCommands()
    speak("PC Part Manager")
    my_pc_parts = readParts()

    # Main loop: keep reading commands until the user types "exit"
    while True:
        entry = input("Enter in a command: ").strip().lower()

        # Run the function that matches the command
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


# Only start the program when this file is run directly (not when imported)
if __name__ == '__main__':
    main()
