# 0. Move cursor to (935, 697)
# 1. Left click
# 2. Right click
# 3. Drag cursor to (1031, 955)
# 4. Write text "Hello World"
# 5. Wait 1 second
# 6. Wait for image "C:/Users/images/image-to-search.png"
# 7. Wait for key input "shift"
# 8. Insert key "shift"
# 9. Insert hotkey "ctrl + C"

# actions = [
# {'id': 0, 'move':{'x': 935, 'y': 697}},
# {'id': 1, 'left_click': 1},
# {'id': 2, 'right_click': 1},
# {'id': 3, 'drag' : {'x': 1031, 'y': 955}},
# {'id': 4, 'write': 'Hello World'},
# {'id': 5, 'sleep': 1},
# {'id': 6, 'image': 'C:/Users/images/image-to-search.png'},
# {'id': 7, 'wait_key': 'shift'},
# {'id': 8, 'key': 'shift'},
# {'id': 9, 'hotkey': ['ctrl', 'C']},
# ]

import re


def JSON_lingualizer(actions):
    
    text = ""

    # Does what's recorded
    for action in actions:
        for (key, value) in action.items():
            position = value
            # For moving
            if key == "move":
                
                text += f'{action["id"]}. Move cursor to ({position["x"]}, {position["y"]})\n'
                
            elif key == "left_click":
                
                text += f'{action["id"]}. Left click \n'

            elif key == "right_click":

                text += f'{action["id"]}. Right click \n'
                
            elif key == "drag":

                text += f'{action["id"]}. Drag cursor to ({position["x"]}, {position["y"]})\n'
                
            elif key == "write":

                text += f'{action["id"]}. Write text "{action["write"]}"\n'
                
            elif key == "image":
                
                text += f'{action["id"]}. Wait for image "{action["image"]}"\n'
                
            elif key == "sleep":
                
                text += f'{action["id"]}. Wait for time ({action["sleep"]})s\n'
                
            elif key == "hotkey":
                    
                text += f"""{action['id']}. Insert hotkey "{' + '.join(action['hotkey'])}"\n"""

            elif key == "key":
                
                text += f"""{action["id"]}. Insert key "{action['key']}"\n"""
                
            elif key == "wait_key":
                
                text += f"""{action["id"]}. Wait for key "{action['wait_key']}"\n"""
                
            else:
                continue
            
    return text

def lang_to_json(input_str):
        
    input_lines = input_str.lower().split("\n")
    actions = []
    
    for line in input_lines:
        
        if not line:
            continue
        
        action = {}
        
        if re.match(r'^\d+.', line):
            action_id = re.findall(r'^\d+.', line)[0]
            action['id'] = int(action_id.replace('.', ''))
        
        if re.match(r'.*move.*', line):

            # Extract the string inside the parentheses
            coordinate_str = re.findall(r'(\d+, \d+)', line)[0]
            x, y = coordinate_str.split(",")

            action['move'] = {'x': int(x), 'y': int(y)}
        
        elif re.match(r'.*left.?click.*', line):
            
            action['left_click'] = 1
            
        elif re.match(r'.*right.?click.*', line):
            
            action['right_click'] = 1

        elif re.match(r'.*drag.*', line):

            # Extract the string inside the parentheses
            coordinate_str = re.findall(r'(\d+, \d+)', line)[0]
            x, y = coordinate_str.split(",")

            action['drag'] = {'x': int(x), 'y': int(y)}
            
        elif re.match(r'.*write.*', line):

            # Extract the string inside the parentheses
            action['write'] = re.findall(r'\".*\"', line)[0].strip('"')

        elif re.match(r'.*wait.*time.*', line):
            
            seconds = re.findall(r'(\d+)', line)[0].strip('(').strip(')')
            action['sleep'] = int(seconds)

        elif re.match(r'.*wait.*image.*', line):

            # Extract the string inside the parentheses
            action['image'] = re.findall(r'\".*\"', line)[0].strip('"')
            
        elif re.match(r'.*wait.*key.*', line):

            # Extract the string inside the parentheses
            action['wait_key'] = re.findall(r'\".*\"', line)[0].strip('"')
            
        elif re.match(r'.*hot.?key.*', line):

            # Extract the string inside the parentheses
            hotkeys = re.findall(r'\".*\"', line)[0].strip('"')
            action["hotkey"] = [key.strip() for key in hotkeys.split('+')]
            
        elif re.match(r'.*key.*', line):

            # Extract the string inside the parentheses
            action['key'] = re.findall(r'\".*\"', line)[0].strip('"')
            
        else:
            class InvalidRequest(Exception):
                pass
            raise InvalidRequest(f"'{line}' is not defined")
        
        actions.append(action)
        
    return actions
