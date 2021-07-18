from OmegaExpansion import onionI2C
from enum import Enum
import time



  
# Get I2C bus
i2c = onionI2C.OnionI2C()

class MCP23017Register(Enum):

	IODIR_A		= 0x00		    # Controls the direction of the data I/O for port A.
	IODIR_B		= 0x01			# Controls the direction of the data I/O for port B.
	IPOL_A		= 0x02			# Configures the polarity on the corresponding GPIO_ port bits for port A.
	IPOL_B		= 0x03			# Configures the polarity on the corresponding GPIO_ port bits for port B.
	GPINTEN_A	= 0x04			# Controls the interrupt-on-change for each pin of port A.
	GPINTEN_B	= 0x05			# Controls the interrupt-on-change for each pin of port B.
	DEFVAL_A	= 0x06			# Controls the default comparaison value for interrupt-on-change for port A.
	DEFVAL_B	= 0x07			# Controls the default comparaison value for interrupt-on-change for port B.
	INTCON_A	= 0x08			# Controls how the associated pin value is compared for the interrupt-on-change for port A.
	INTCON_B	= 0x09			# Controls how the associated pin value is compared for the interrupt-on-change for port B.
	IOCON		= 0x0A			# Controls the device.
	GPPU_A		= 0x0C			# Controls the pull-up resistors for the port A pins.
	GPPU_B		= 0x0D			# Controls the pull-up resistors for the port B pins.
	INTF_A		= 0x0E			# Reflects the interrupt condition on the port A pins.
	INTF_B		= 0x0F			# Reflects the interrupt condition on the port B pins.
	INTCAP_A	= 0x10			# Captures the port A value at the time the interrupt occured.
	INTCAP_B	= 0x11			# Captures the port B value at the time the interrupt occured.
	GPIO_A		= 0x12			# Reflects the value on the port A.
	GPIO_B		= 0x13			# Reflects the value on the port B.
	OLAT_A		= 0x14			# Provides access to the port A output latches.
	OLAT_B		= 0x15			# Provides access to the port B output latches.

def bitRead(bit,pos):
	string =format(bit, '08b')
	k = string[-pos-1]
	return (k == '1')
	
class MCP23017:
	def __init__(self,MCP23017Adress):
		self.MCP23017Adress=MCP23017Adress
		

	def init(self):
		#BANK = 	0 : sequential register addresses
		#MIRROR = 	0 : use configureInterrupt 
		#SEQOP = 	1 : sequential operation disabled, address pointer does not increment
		#DISSLW = 	0 : slew rate enabled
		#HAEN = 	0 : hardware address pin is always enabled on 23017
		#ODR = 	    0 : open drain output
		#INTPOL = 	0 : interrupt active low
		try:
			i2c.writeByte(self.MCP23017Adress, 0b00100000,)

		except:
			print("port is busy")


		


	def portMode(self,Port=0,directions=0):
		try:

			if Port == 'A' :
				i2c.writeByte(self.MCP23017Adress,MCP23017Register.IODIR_A.value, directions)
				#print('MCP23017Adress',MCP23017Adress,'port address',MCP23017Register.IODIR_A.value,'directions',directions)
			elif Port == 'B'  :
				i2c.writeByte(self.MCP23017Adress,MCP23017Register.IODIR_B.value, directions)
				#print('MCP23017Adress',MCP23017Adress,'port address',MCP23017Register.IODIR_B.value,'directions',directions)
			else :
				print('Wrong Port Name')

		except:
			print("port is busy")
	
	def pinMode(self,Pin,Mode):
		try:
			# pin [0,15]
			iodirreg= MCP23017Register.IODIR_A.value
			if Pin > 7 :
				iodirreg = MCP23017Register.IODIR_B.value
				Pin-= 8
				
			iodirr = i2c.readBytes(self.MCP23017Adress, iodirreg,1)
			iodir =iodirr[0]
			if  ((Mode == input) or (Mode == 1)):
				iodir = iodir or 1<<Pin
			else :
				iodir = iodir or 0<<Pin
			i2c.writeByte(self.MCP23017Adress,iodirreg,iodir)
		except:
			print("port is busy")

	def digitalWrite(self,Pin,State):
		try:
		 # pin [0,15]
			gpioreg = MCP23017Register.GPIO_A.value
			if Pin > 7 :
				gpioreg = MCP23017Register.GPIO_B.value
				Pin-=8
			gpioo = i2c.readBytes(self.MCP23017Adress,gpioreg,1)
			gpio=gpioo[0]
			if  ((State == "HIGH") or (State == 1)):
				gpio = gpio or 1<<Pin
			else :
				gpio = (gpio & ( ~(1 << Pin)))
			
			i2c.writeByte(self.MCP23017Adress,gpioreg,gpio)

		except:
			print("port is busy")



		
	
	def digitalRead(self,Pin):
		try:
			# pin [0,15]
			gpioreg = MCP23017Register.GPIO_A.value
			if Pin > 7 :
				gpioreg = MCP23017Register.GPIO_B.value
				Pin-=8
			gpioo = i2c.readBytes(self.MCP23017Adress,gpioreg,1)
			gpio=gpioo[0]

			if  (bitRead(gpio,Pin)):
				return (True)
			else :
				return (False)
		except:
			print("port is busy")
	
if __name__ == "__main__":


	port1 =MCP23017(0x20)	
	port1.portMode('A',1)		
	port1.portMode('B',0)
	port1.digitalWrite(15,1)
	time.sleep(2)
	port1.digitalWrite(15,0)
	time.sleep(2)
	while(True):
			if (port1.digitalRead(7)== True):
					port1.digitalWrite(15,1)
					print("its on")
			else :
					port1.digitalWrite(15,0)
					print("its off")

			time.sleep(2)
		
	
	
	


		

		

	
	
	
		

	






