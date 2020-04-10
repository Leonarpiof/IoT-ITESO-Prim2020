#include <MKRGSM.h>
#include <MQTT.h>
#include <I2CSoilMoistureSensor.h>
#include <Wire.h>
#include <String.h>

/** Use Telcel's APN*/
#define TELCEL		(1)
/** Use AT&T's APN (Mexico)*/
#define AT_T		(0)
/** Use Movistar's APN*/
#define MOVISTAR	(0)

/** Use Mosquitto test broker DO NOT PUBLISH SENSITIVE DATA*/
/** Mosquitto test broker is public, so anyone may be listening,
do not publish any sensitive data.*/
#define MOSQUITTO_BRK	(1)
/** Use AWS broker*/
#define AWS_BRK			(0)
/** Max message size*/
#define MSG_SIZE		(100)
/** IMEI size*/
#define IMEI_SIZE		(16)

/** Serial port baud rate*/
#define SER_PORT_BR		(115200)

/** Defines the time between two messages*/
#define DELAY_TIME		(60000000)

/** Object for the I2C sensor*/
I2CSoilMoistureSensor sensor;

/** Analog pin for the light sensor*/
int light_pin = A1;
/** Variable for the light sensor reading*/
int light_read = 0;

/** Variable for the humidity*/
int humidity = 0;
/** Variable for the temperature*/
int temperature = 0;

/** SIM pin*/
const char pin[]  = "1111";

#if(TELCEL)
/** Telcel APN*/
const char apn[]  = "internet.itelcel.com";
const char login[] = "webgprs";
const char password[] = "webgprs2002";
#elif(AT_T)
/** AT&T APN*/
const char apn[]  = "modem.nexteldata.com.mx";
/** AT&T no tiene usuario ni contraseña para la APN
    utilizar NULL para ambos parámetros*/
#else
/** Movistar APN*/
const char apn[] = "internet.movistar.mx";
const char login[] = "movistar";
const char password[] = "movistar";
#endif

#if(MOSQUITTO_BRK)
/** Mosquitto server address*/
const char mqtt_server[] = "test.mosquitto.org"
#else
/** AWS server address*/
const char mqtt_server[] = ""
#endif

/** Variables to store the device's IMEI*/
String imei_str;
char IMEI[IMEI_SIZE] = {0};

/** Array to store the message to be sent*/
char msg_to_be_sent[MSG_SIZE] = {0};

/** Network object*/
GSMClient net;
/** Object to access IMEI*/
GSMModem modem;
/** Object to attach to a network*/
GPRS gprs;
/** Object to acces the SIM*/
GSM gsmAccess;
/** Object for the MQTT client*/
MQTTClient client;

/** Variable to keep count of time*/
unsigned long lastMillis = 0;

/** Connects to both cellular network, and MQTT server*/
void connect()
{
	/** Connection state*/
	bool connected = false;

	Serial.print("connecting to cellular network ...");

	/** After starting the modem with gsmAccess.begin()
	attach to the GPRS network with the APN, login and password */
	while (!connected)
	{
	    if ((gsmAccess.begin(pin) == GSM_READY) &&
			(gprs.attachGPRS(apn, login, password) == GPRS_READY))
		{
			connected = true;
	  	}

		else
		{
			Serial.print(".");
			delay(1000);
		}

		/** Repeats process until connected to network*/
	}

	Serial.print("\nconnecting...");

	/** Connects to the MQTT server*/
	while (!client.connect(IMEI, false))
	{
		Serial.print(".");
		delay(1000);
	}

	Serial.println("\nconnected!");
}

/** Setup functions*/
void setup()
{
	/** Initializes serial communication through USB*/
	Serial.begin(SER_PORT_BR);
	Serial.println("Initialized");

	/** Connects to MQTT broker*/
	client.begin(mqtt_server, net);
	/** Initializes modem functions*/
	modem.begin();

	/** Gets the device's IMEI, and sets it to a char variable*/
	imei_str = (modem.getIMEI());
	imei_str.toCharArray(IMEI, sizeof(IMEI));

	/** Connects to cellular network and MQTT broker*/
	connect();
}

/** Loop forever*/
void loop()
{
	/** MQTT loop*/
	client.loop();

	/** If the device is disconnected, tries to connect
	again */
	if (!client.connected())
	{
		connect();
	}

	/** Publish a message roughly every minute*/
	if(DELAY_TIME < (millis() - lastMillis))
	{
		/** Gets current time*/
		lastMillis = millis();
		/** Publishes a message*/
		client.publish("/hello", "world");
	}
}