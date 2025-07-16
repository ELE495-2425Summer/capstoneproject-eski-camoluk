from APIProcessor import APIProcessor
from CommandParser import CommandParser
from MotorController import MotorController
from TCP_sender import TCP_sender
from DBService import DBService
import threading


processor = APIProcessor()
parser = CommandParser()
motor_controller = MotorController()
db = DBService()
db.connect_db()

while True:
    command, is_recognize = processor.speech_to_text(db)
    if(is_recognize == False):
        processor.speech("Seçilen kişi algılanamadı.")
        continue
    
    db.update_data("ses_ciktisi", {"$set": {"ses": command}})
    command_list = processor.getJSON(command)
    db.update_data("algilanan_json", {"$set": {"json": command_list}})
    print(command_list)
    parser.parse_json(command_list)

    if(parser.suggestion):
        processor.speech(parser.suggestion)
        continue


    for i,cmd in enumerate(parser.commands):
        if((cmd.action == "forward" or cmd.action == "backward")):
            if(cmd.condition):
                a = None
            else:
                a = cmd.conditiom["limit"]
            motor_controller.go(db, processor, cmd.action, cmd.distance, cmd.duration, a)
                        
        elif(cmd.action == "turn"):
           motor_controller.turn(db, cmd.angle, processor) 
        else:
            motor_controller.stop(db, processor, cmd.duration)
    
    threading.Thread(target=TCP_sender,args=("dur",), daemon=True).start()


        




    
        
        
            

