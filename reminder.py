from datetime import datetime
from database import medicines_collection

def check_reminders(user_id):
    now = datetime.now().strftime("%H:%M")
    medicines = medicines_collection.find({"user_id": user_id})
    
    due_medicines = []
    for med in medicines:
        if med["time"] == now:
            due_medicines.append(med["medicine_name"])
    
    return due_medicines