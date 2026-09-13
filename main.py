from pathlib import Path
import shutil

def readAndOpen():
    print("\nDirectory Map :")
    path=Path('.')
    items=[p for p in sorted(path.rglob('*')) if not p.name.startswith('.')]
    map={}
    for i,val in enumerate(items,1):
        depth=len(val.relative_to(path).parts)
        spaces='  '*(depth-1)
        icon="📁" if val.is_dir() else " "
        print(f"{i:2} : {spaces}{icon}  {val.name}")
        map[i]=val
    print("-------------\n")
    return map
        
def get_selected_path(map,act_text):
    while True:
        try:
            pick=input(f"Enter the item number to perform {act_text} (or 0 to cancel):").strip()
            if pick=='0':
                return None
            num=int(pick)
            if num in map:
                return map[num]
            else:
                print("Invalid number. Please try again.")
        except ValueError :
            print("Please enter a valid Integer.")

def create():
    print("[1] Create File")
    print("[2] Create Folder")
    pick=input("What do you want to create? [1/2]: ").strip()
    if pick not in ['1','2']:
        print("Invalid choice , Cancelling...")
        return
    mapping=readAndOpen()
    print(f"0 : Current Directory")
    dest=Path('.')
    while True:
        try:
            choice=input("\n Enter the number of the folder name (or 0 for Root)")
            if choice=='0':
                break
            num=int(choice)
            if num in mapping and mapping[num].is_dir():
                dest=mapping[num]
                break
            else:
                print("Select a valid folder corresponding to a FOLDER.")
        except ValueError:
            print("Please enter a valid Integer.")
    name=input(f"\nPlease enter the name of the new {'file' if pick=='1' else 'folder'}: ")
    target=dest/name
    try:
        if target.exists():
            print("Item already exists.")
            return
        if pick=='1':
            with open(target, 'w') as f:
                data = input("Please write into the file (leave blank for empty): ")
                f.write(data)
            print(f"✅ FILE '{target.name}' CREATED SUCCESSFULLY in '{dest}'!")
        elif pick=='2':
            target.mkdir(parents=True,exist_ok=True)
            print(f"✅ FOLDER '{target.name}' CREATED SUCCESSFULLY in '{dest}'!")
    except Exception as e:
        print(f"An Error {e} has occured.")
    
def read():
    mapping=readAndOpen()
    if not mapping:
        print("Directory is empty.")
        return
    p = get_selected_path(mapping, "read")
    if not p: return
    try:
        if p.is_file():
            print("\n--- File Content ---")
            print(p.read_text())
            print("--------------------\n")
        elif p.is_dir():
            print(f"\n--- Folder Contents: {p.name} ---")
            for child in p.iterdir():
                icon = "📁" if child.is_dir() else "📄"
                print(f"{icon} {child.name}")
            print("--------------------\n")
    except Exception as e:
            print(f"An error occured as {e}")

def update():
    mapping=readAndOpen()
    if not mapping:
        print("Directory is empty.")
        return

    p = get_selected_path(mapping, "update")
    if not p: return

    try:
        if p.is_dir():
            print(f"Updating Folder: {p.name}")
            new_name = input("Enter new name for this folder: ")
            new_path = p.parent / new_name
            p.rename(new_path)
            print("✅ FOLDER RENAMED SUCCESSFULLY!")
            
        elif p.is_file():
            print(f"\nUpdating File: {p.name}")
            print("Type 'r' to rename the file.")
            print("Type 'a' to append content.")
            print("Type 'o' to overwrite content.")
            print("Type 'c' to cancel.")
            while True:
                s=input("Which option do you pick?").strip().lower()
                if s=='r':
                    new_name = input("Rename the file to: ")
                    new_path = p.parent / new_name
                    p.rename(new_path)
                    print("✅ FILE RENAMED SUCCESSFULLY!")
                    break
                elif s=='a':
                    with open(p,'a') as f:
                        data=input("The new content shall be -")
                        f.write(" "+data)
                        break
                elif s=='o':
                    with open(p,'w') as f:
                        data=input("The new content shall be -")
                        f.write(data)
                        break
                elif s=='c':
                    print("Cancelled the operation.Exiting...")
                    break
                else:
                    print(f"{s} is not applicable.Please try again\n")
            print(f"FILE UPDATED SUCCESSFULLY!")
    except Exception as e:
            print(f"An error occured as {e}")
            
def delete():
    mapping = readAndOpen()
    if not mapping:
        print("Directory is empty.")
        return
    p = get_selected_path(mapping, "delete")
    if not p: return
    try:
        confirm = input(f"Are you SURE you want to delete '{p.name}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        if p.is_file():
            p.unlink()
            print(f"✅ FILE '{p.name}' DELETED.")
        elif p.is_dir():
            try:
                p.rmdir() # Tries to delete if empty
                print(f"✅ EMPTY FOLDER '{p.name}' DELETED.")
            except OSError:
                deep = input("⚠️ Folder is not empty! Delete it and ALL contents? (y/n): ").lower()
                if deep == 'y':
                    shutil.rmtree(p)
                    print(f"✅ FOLDER '{p.name}' AND ALL CONTENTS DELETED.")
                else:
                    print("Deletion cancelled.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
while True:
    print("\n========== FILE MANAGER ==========")
    print("Press 1 for Creating a File/Folder.")
    print("Press 2 for Reading a File/Folder.")
    print("Press 3 for Updating a File/Folder.")
    print("Press 4 for Deleting a File/Folder.")
    print("Press 5 to EXIT.")
    print("==================================")
    inp = input("Please pick an option: ").strip()
    if inp == '1':
        create()
    elif inp == '2':
        read()
    elif inp == '3':
        update()
    elif inp == '4':
        delete()
    elif inp == '5':
        print("Exiting File Manager. Goodbye!")
        break
    else:
        print("⚠️ Invalid option. Please pick a number between 1 and 5.")