__version__ = '0.1.0'

# Reset data
stops = "false"
entcommands = []
build = "2 Beta" # Intentionally uses string instead of number
tileos = "1.1"

# Reset settings/configs
confLines = "true" # Insert lines or not

# cmdlist helper functions and variables
cmdsgeneral = ["cmdlist - A list of commands, the thing you're viewing right now!", "datetime - The current date and time in UTC", "stop - Stops BluePrompt", "clear - Clears the terminal history", "enteredcmds - A list of commands you entered into BluePrompt", "bpset - Set some blueprompt configs/settings!"]

# Functions
def lines():
  if confLines == "true":
    print("-------------------")

# Modules
import datetime # for datetime

# Start prompt
lines()
print(f"BluePrompt Build {build} (Part of TileOS v{tileos})")
print("Type in \"cmdlist\" for a list of commands!")

while stops == "false":
  lines()
  c = input("Enter command\n>> ")
  lines()
  entcommands.append(c)
  if c == "datetime":
    print(f"{datetime.datetime.today():%A, %B %d, %Y %H:%M:%S (%I %p) UTC}")
  elif c == "stop":
    stops = "true"
    print("Stopped BluePrompt")
    lines()
  elif c == "clear":
    print("\n" * 100)
  elif c == "enteredcmds":
    print(", ".join(entcommands))
  elif c.startswith("cmdlist"):
    if c == "cmdlist":
      print("BluePrompt Command List - Please select a category of commands you want to view.\n\"cmdlist gen\" for general commands")
    elif c == "cmdlist gen":
      print("\n".join(cmdsgeneral))
    else:
      print("Unknown command list category.")
  elif c.startswith("bpset"): # BluePrompt settings
    if c == "bpset lines true":
      confLines = "true"
      print("Set setting \"Lines\" to true.")
    elif c == "bpset lines false":
      confLines = "false"
      print("Set setting \"Lines\" to false.")
    else:
      print("Unknown BluePrompt setting.")
  elif c.startswith("displaytext"):
    print(c[12:])