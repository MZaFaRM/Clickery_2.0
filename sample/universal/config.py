from json import load as listify

# Change value to adjust cursor speed while moving [default 0.50]
Move_Speed = 0.50
# Change value to adjust cursor speed while draggging [default 0.50]
Drag_Speed = 0.50

# Change value to adjust typing speed [default 0.15]
Type_Speed = 0.15

# lists and dictionaries used
record = []

# actions = ["move", "click", "drag", "write", "image", "sleep", "hotkey", "key", "screenshot"]

f = open(r"sample\universal\actions.json")
actions_list = listify(f)
f.close()

f = open(r"sample\universal\replace.json")
replace_list = listify(f)
f.close()
