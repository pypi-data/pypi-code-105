import subprocess

def replit(path):
  subprocess.check_call(['mkdir','TayTulesInit/'])
  f = open('TayTulesInit/boot.py','w')
  f.write("import subprocess\nimport os\npackage='TayTules'\nsubprocess.check_call(['pip','install',package,'--upgrade'])\nsubprocess.check_call(['python3','"+path+"\nif os.name == nt: os.system('cls')\nelse: os.system('clear')'])")
  f.close()
  
  f = open(".replit", 'w')
  f.write("run= \"python3 TayTulesInit/boot.py\"")
  f.close()
  