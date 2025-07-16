import json
from typing import List, Optional, Dict, Any


class Command:
    def __init__(
        self,
        action: str,
        angle: Optional[float],
        distance: Optional[float],
        duration: Optional[float],
        condition: Optional[Dict[str, Any]]
    ):
        self.action = action
        self.angle = angle
        self.distance = distance
        self.duration = duration
        self.condition = condition

    def __repr__(self):
        return f"Command(action={self.action}, angle={self.angle}, distance={self.distance}, duration={self.duration}, condition={self.condition})"


class Issue:
    def __init__(self, index: int, field: str, issue: str):
        self.index = index
        self.field = field
        self.issue = issue
        #Buraya optional eklemen lazım mı ona bir daha bak aynı Command classındaki gibi
    
    def __repr__(self):
        return f"Issue(index={self.index}, field={self.field}, issue={self.issue})"


class CommandParser:
    def __init__(self):
        self.commands: List[Command] = []
        self.errors: List[Issue] = []
        self.warnings: List[Issue] = []
        self.suggestion: Optional[str] = None

    def parse_json(self, json_data: str):

        self.commands.clear()
        self.errors.clear()
        self.warnings.clear()
        self.suggestion = None
        
        try:
            print(f"Gelen json_data:\n{json_data!r}")
            data = json.loads(json_data)
            
            # Komutları işle
            for cmd in data.get("commands", []):
                command = Command(
                    action=cmd.get("action"),
                    angle=cmd.get("angle"),
                    distance=cmd.get("distance"),
                    duration=cmd.get("duration"),
                    condition=cmd.get("condition")
                )
                self.commands.append(command)

            # Hataları işle
            for err in data.get("errors", []) or []:
                error = Issue(
                    index=err["index"],
                    field=err["field"],
                    issue=err["issue"]
                )
                self.errors.append(error)

            # Uyarıları işle
            for warn in data.get("warnings", []) or []:
                warning = Issue(
                    index=warn["index"],
                    field=warn["field"],
                    issue=warn["issue"]
                )
                self.warnings.append(warning)

            # Global suggestion
            self.suggestion = data.get("suggestion")

        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
