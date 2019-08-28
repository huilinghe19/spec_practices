import SpecMotor
import SpecCommand 
m = SpecMotor.SpecMotor('copley', 'localhost:spec')
print m.getPosition()
cmd = SpecCommand.SpecCommand('', 'localhost:spec')

cmd.executeCommand("mv copley 2000")
#print m.getPosition()
#cmd.executeCommand("mv copley -1000")
#print m.getPosition()