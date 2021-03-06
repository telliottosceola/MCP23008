#include "spark_wiring_i2c.h"
#include "spark_wiring_usbserial.h"
#include "spark_wiring_constants.h"
#include "Particle.h"

class MCP23008{
public:
    //Constructor
    MCP23008();
    virtual ~MCP23008();
    //Set Address.  Indicate status of jumpers on board.  Send 0 for not installed, send 1 for installed
    void setAddress(int a0, int a1, int a2);
    void setAddress(int a);
    //Set number or outputs, for relay boards they wills start at 0, if you need outputs at specific locations
    //use the setAsOutput method for each
    void setOutputs(int num);
    void setOutput(int num);

    void setIoDir();
    //Turn on Relay
    void turnOnRelay(int relay);
    //Turn off Relay
    void turnOffRelay(int relay);
    //Toggle Relay
    void toggleRelay(int relay);
    //momentary relay
    void momentaryRelay(int relay);
    void momentaryRelay(int relay, int duration);
    void momentaryOff();
    
    //Turn On all Relays
    void turnOnAllRelays();
    //Turn Off All Relays
    void turnOffAllRelays();
    
    byte bankStatus;
    //Set status of all relays in bank
    void setBankStatus(int status);
    //Read status of relay. Valid return 0 for off 1 for on.  256 returned if there is an error
    int readRelayStatus(int relay);
    //Read status of all relays in bank.  0-255 valid.  256 returned on error
    int readRelayBankStatus();
    //Read status of input
    int readInputStatus(int input);
    //Read status of all inputs
    int readAllInputs();
    int relayTalk(String command);
    //User Accessible Variables
    //Whether or not the controller is ready to accept commands
    bool initialized;
    bool publishInputEvents;
    int sendCommand(int reg, int cmd);
    int sendCommand(int reg);
private:
    bool firstInput = true;

    byte bitop(byte b1, byte b2, int op);
    void relayOp(int relay, int op);
    //internal use method for refreshing bank status variables
    void readStatus();
    //Status of relays in bank 1
    
    byte inputStatus;
    byte ioset = 255;
    bool iosetCustom = false;
    int relayCount = 0;

    int _momentaryRelay;

    int address = 0x20;
    int address2 = 0x21;
    int retrys = 0;
    byte outputRegister = 0x0A;
    Timer timer;
};
