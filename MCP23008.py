# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MCP23008
# This code is designed to work with the MCP23008_REG_I2CR8G5LE_10A I2C relay controller available from ControlEverything.com.
# https://www.controleverything.com/content/Relay-Controller?sku=MCP23008_REG_I2CR8G5LE_10A#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MCP23008_DEFAULT_ADDRESS            = 0x20

# MCP23008 Register Map
MCP23008_REG_IODIR                    = 0x00 # I/O DIRECTION Register
MCP23008_REG_IPOL                    = 0x01 # INPUT POLARITY PORT Register
MCP23008_REG_GPINTEN                = 0x02 # INTERRUPT-ON-CHANGE PINS
MCP23008_REG_DEFVAL                    = 0x03 # DEFAULT VALUE Register
MCP23008_REG_INTCON                    = 0x04 # INTERRUPT-ON-CHANGE CONTROL Register
MCP23008_REG_IOCON                    = 0x05 # I/O EXPANDER CONFIGURATION Register
MCP23008_REG_GPPU                    = 0x06 # GPIO PULL-UP RESISTOR Register
MCP23008_REG_INTF                    = 0x07 # INTERRUPT FLAG Register
MCP23008_REG_INTCAP                    = 0x08 # INTERRUPT CAPTURED VALUE FOR PORT Register
MCP23008_REG_GPIO                    = 0x09 # GENERAL PURPOSE I/O PORT Register
MCP23008_REG_OLAT                    = 0x0A # OUTPUT LATCH Register 0

# MCP23008 I/O Direction Register Configuration
MCP23008_IODIR_PIN_7_INPUT            = 0x80 # Pin-7 is configured as an input
MCP23008_IODIR_PIN_6_INPUT            = 0x40 # Pin-6 is configured as an input
MCP23008_IODIR_PIN_5_INPUT            = 0x20 # Pin-5 is configured as an input
MCP23008_IODIR_PIN_4_INPUT            = 0x10 # Pin-4 is configured as an input
MCP23008_IODIR_PIN_3_INPUT            = 0x08 # Pin-3 is configured as an input
MCP23008_IODIR_PIN_2_INPUT            = 0x04 # Pin-2 is configured as an input
MCP23008_IODIR_PIN_1_INPUT            = 0x02 # Pin-1 is configured as an input
MCP23008_IODIR_PIN_0_INPUT            = 0x01 # Pin-0 is configured as an input
MCP23008_IODIR_PIN_INPUT            = 0xFF # All Pins are configured as an input
MCP23008_IODIR_PIN_OUTPUT            = 0x00 # All Pins are configured as an output

# MCP23008 Pull-Up Resistor Register Configuration
MCP23008_GPPU_PIN_7_EN                = 0x80 # Pull-up enabled on Pin-7
MCP23008_GPPU_PIN_6_EN                = 0x40 # Pull-up enabled on Pin-6
MCP23008_GPPU_PIN_5_EN                = 0x20 # Pull-up enabled on Pin-5
MCP23008_GPPU_PIN_4_EN                = 0x10 # Pull-up enabled on Pin-4
MCP23008_GPPU_PIN_3_EN                = 0x08 # Pull-up enabled on Pin-3
MCP23008_GPPU_PIN_2_EN                = 0x04 # Pull-up enabled on Pin-2
MCP23008_GPPU_PIN_1_EN                = 0x02 # Pull-up enabled on Pin-1
MCP23008_GPPU_PIN_0_EN                = 0x01 # Pull-up enabled on Pin-0
MCP23008_GPPU_PIN_EN                = 0xFF # Pull-up enabled on All Pins
MCP23008_GPPU_PIN_DS                = 0x00 # Pull-up disabled on All Pins

# MCP23008 General Purpose I/O Port Register
MCP23008_GPIO_PIN_7_HIGH            = 0x80 # Logic-high on Pin-7
MCP23008_GPIO_PIN_6_HIGH            = 0x40 # Logic-high on Pin-6
MCP23008_GPIO_PIN_5_HIGH            = 0x20 # Logic-high on Pin-5
MCP23008_GPIO_PIN_4_HIGH            = 0x10 # Logic-high on Pin-4
MCP23008_GPIO_PIN_3_HIGH            = 0x08 # Logic-high on Pin-3
MCP23008_GPIO_PIN_2_HIGH            = 0x04 # Logic-high on Pin-2
MCP23008_GPIO_PIN_1_HIGH            = 0x02 # Logic-high on Pin-1
MCP23008_GPIO_PIN_0_HIGH            = 0x01 # Logic-high on Pin-0
MCP23008_GPIO_PIN_HIGH                = 0xFF # Logic-high on All Pins
MCP23008_GPIO_PIN_LOW                = 0x00 # Logic-low on All Pins


#possibly pass number of relays in instantiation to automatically select how many GPIOs. Or just pass those in during object instantiate to statically set/turn off access to them

class MCP23008:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)
        #set address to default if not passed
        if not hasattr(self, 'address'):
            self.address = MCP23008_DEFAULT_ADDRESS
        
        #we only need to know which are outputs as the chip sets all GPIOs as inputs by default for safety reasons.
        if hasattr(self, 'gpio_output_map'):
            register_byte = 255
            print self.gpio_output_map
            for channel in self.gpio_output_map:
                register_byte = register_byte ^ 1 << channel
                
            if(register_byte != 0):
                self.set_output_register(register_byte)

        

    def set_output_register(self, register_value):
        bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_IODIR, register_value)
    
    #not currently used
    def set_register(self, register_number, register_value):
        self.dostuff()
        #set register based on value
        #I don't think we need to break it down, into methods like set relay_register, but depends on how often we need to use it.
        

# Need to check and make sure the registration bits are correct
    def set_gpio_high(self, target_gpio, status = None):
        if(status == None):
            status = self.get_all_gpio_status()
            
        target_byte_value = 1 << target_gpio
        print target_byte_value
        new_status_byte = status | target_byte_value
        print new_status_byte
        bus.write_byte_data(self.address, MCP23008_REG_GPIO, new_status_byte)

#pseudo method
    def turn_on_relay(self, target_relay, status = None):
        self.set_gpio_high(target_relay, status)
        
# Need to check and make sure the registration bits are correct
    def set_gpio_low(self, target_gpio, status = None):
        if(status == None):
            status = self.get_all_gpio_status()
        target_byte_value = 1 << target_gpio
        new_status_byte = status ^ target_byte_value
        bus.write_byte_data(self.address, MCP23008_REG_GPIO, new_status_byte)

#pseudo method
    def turn_off_relay(self, target_relay, status = None):
        self.set_gpio_low(target_relay, status)
        
    def toggle_gpio(self, target_gpio):
        target_byte_value = 1 << target_gpio
        status = self.get_all_gpio_status()
        #check if the gpio is set high
        if(status & target_byte_value != 0):
            self.set_gpio_low(target_gpio, status)
        else:
            self.set_gpio_high(target_gpio, status)
    
#pseudo method
    def toggle_relay(self, target_relay):
        self.toggle_gpio(target_relay)
    
    def get_single_gpio_status(self, target_gpio):
        status = self.get_all_gpio_status
        target_byte_value = 1 << target_gpio
        return status & target_byte_value != 0
        
    def get_all_gpio_status(self):
        return bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPIO)
    
    def get_all_gpio_resistor_settings(self):
        return bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPPU)
    
    def pull_up_gpio(self, target_gpio):
        target_byte_value = 1 << target_gpio
#         print target_byte_value
        status = self.get_all_gpio_resistor_settings()
#         print status
        new_status_byte = status | target_byte_value
#         print new_status_byte
        bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPPU, new_status_byte)

    
    