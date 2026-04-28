import subprocess

process1 = subprocess.Popen(['python', 'app.py'])
process2 = subprocess.Popen(['python', 'appSimulacion.py'])

process1.wait()
process2.wait()