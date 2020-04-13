/**************** INCLUDES **************************************************/
#include <I2CSoilMoistureSensor.h>
#include <Wire.h>
#include <String.h>
#include <GSMSSLClient.h>
#include <GSMSecurity.h>
#include <GSMModem.h>
#include <GPRS.h>
#include <PubSubClient.h>
#include <MQTT.h>

#include "secrets.h"
/**************** INCLUDES **************************************************/



/**************** DEFINES ***************************************************/
/** Use Telcel's APN*/
#define TELCEL			(1)
/** Use AT&T's APN (Mexico)*/
#define AT_T			(0)
/** Use Movistar's APN*/
#define MOVISTAR		(0)

/** Sets a test message to the buffer*/
#define TEST_MSG		(1)

#define SSL_EN			(0)

/** Use Mosquitto test broker DO NOT PUBLISH SENSITIVE DATA*/
/** Mosquitto test broker is public, so anyone may be listening,
do not publish any sensitive data.*/
#define MOSQUITTO_BRK	(1)
/** Use AWS broker*/
#define AWS_BRK			(0)

/** Port to which the device will connect.
	Usually:
	1883 -> MQTT not secure
	8883 -> MQTT secure*/
#define PORT			(8883)
/** Max message size*/
#define MSG_SIZE		(100)
/** IMEI size*/
#define IMEI_SIZE		(16)

/** Serial port baud rate*/
#define SER_PORT_BR		(115200)

/** Defines the time between two messages*/
#define DELAY_TIME		(60000)
/**************** DEFINES ***************************************************/



/**************** VARIABLES *************************************************/
/** Object for the I2C sensor*/
I2CSoilMoistureSensor sensor;

/** Analog pin for the light sensor*/
int light_pin = A1;
/** Variable for the light sensor reading*/
int light_read = 0;
/** Variable to calculate the luminosity*/
int light_calc = 0;

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
const char mqtt_server[] = "test.mosquitto.org";
#else
/** AWS server address*/
const char mqtt_server[] = "a2rn7z7nyv71kk-ats.iot.us-east-2.amazonaws.com";
#endif

/** Variables to store the device's IMEI*/
String imei_str;
char IMEI[IMEI_SIZE] = {0};

/** MQTT topic into which the data will be published*/
const char topic[] = "/greenhouse1/secA";

/** Array to store the message to be sent*/
char msg_to_be_sent[MSG_SIZE] = {0};
/** Length of the message to be sent*/
int msg_to_be_sent_len = 0;
/** Password for the XOR cipher*/
const char xor_password[MSG_SIZE] =
{
	43, 137, 1, 171, 45, 180, 76, 95, 44, 88, 180,
	24, 255, 62, 157, 171, 24, 163, 154, 4, 179,
	122, 157, 33, 144, 239, 62, 63, 210, 123, 60,
	176, 108, 232, 175, 144, 250, 68, 85, 64, 138,
	182, 172, 4, 222, 11, 23, 94, 62, 83, 51, 150,
	72, 69, 211, 23, 227, 6, 50, 222, 194, 31, 225,
	164, 134, 114, 199, 219, 47, 79, 56, 35, 87,
	207, 80, 139, 8, 213, 84, 116, 140, 160, 140,
	46, 84, 151, 126, 251, 83, 128, 146, 252, 31,
	78, 197, 23, 252, 150, 227, 5
};
/** Counter for the XOR application*/
int xor_counter = 0;

#if(SSL_EN)

/** Object for the SSL client*/
GSMSSLClient net_client;
/** Secure MQTT SSL client*/
PubSubClient mqttClient(mqtt_server, PORT, net_client);

#else

/** Object for the client (Not SSL)*/
GSMClient net_client;
/** Object for the MQTT client*/
MQTTClient client;

#endif
/** Object for security*/
GSMSecurity profile;
/** Object to access IMEI*/
GSMModem modem;
/** Object to attach to a network*/
GPRS gprs;
/** Object to acces the SIM*/
GSM gsmAccess;

/** Variable to keep count of time*/
unsigned long lastMillis = 0;
/**************** VARIABLES *************************************************/



/**************** CONNECT ***************************************************/
/** Connects to both cellular network, and MQTT server*/
void connect()
{
	/** Connection state*/
	bool connected = false;

	Serial.print("\nconnecting to cellular network ...");

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
#if(SSL_EN)
	while (!mqttClient.connect(IMEI))
#else
	while (!client.connect(IMEI))
#endif
	{
		Serial.print(".");
		delay(1000);
	}

	Serial.println("\nconnected!");
}
/**************** CONNECT ***************************************************/



/**************** SETUP *****************************************************/
/** Setup functions*/
void setup()
{
	/** Initializes serial communication through USB*/
	Serial.begin(SER_PORT_BR);
	Serial.print("Initialized\n");

#if(!SSL_EN)
	/** Connects to MQTT broker*/
	client.begin(mqtt_server, PORT, net_client);
#endif
	/** Initializes modem functions*/
	modem.begin();

	/** Gets the device's IMEI, and sets it to a char variable*/
	imei_str = (modem.getIMEI());
	imei_str.toCharArray(IMEI, sizeof(IMEI));
	Serial.print(imei_str);

	/** Initializes I2C for sensor reading*/
	Wire.begin()
	/** Initializes the I2C Soil Moisture sensor*/
	sensor.begin()

	/** Connects to cellular network and MQTT broker*/
	connect();
}
/**************** SETUP *****************************************************/



/**************** LOOP ******************************************************/
/** Loop forever*/
void loop()
{
	/** MQTT loop*/
	client.loop();

	/** If the device is disconnected, tries to connect
	again */
#if(SSL_EN)
	if (!mqttClient.connected())
#else
	if (!client.connected())
#endif
	{
		connect();
	}

	/** Publish a message roughly every minute*/
	if(DELAY_TIME < (millis() - lastMillis))
	{
		/** Gets current time*/
		lastMillis = millis();

		/** Reads the temperature*/
	    temperature = sensor.getTemperature();
	    /** Gives a small delay for the I2C buffer to respond*/
	    delay(50);
	    /** Reads the humidity*/
	    humidity = sensor.getCapacitance();

		/** Reads the light sensor*/
		light_read	= analogRead(light_pin)
		/** Calculates the luminosity in Lux*/
		light_calc = (light_calc / (10 * 68000 * 0.000001 * 1.1075));
		light_calc = pow(10, light_calc);

#if(TEST_MSG)
		msg_to_be_sent[0] = 'W';
		msg_to_be_sent[1] = 'o';
		msg_to_be_sent[2] = 'r';
		msg_to_be_sent[3] = 'l';
		msg_to_be_sent[4] = 'd';
		msg_to_be_sent_len = 5;
#endif

		/** XOR between each message character, and the password*/
		for(xor_counter = 0 ; xor_counter < msg_to_be_sent_len ; xor_counter ++)
		{
			msg_to_be_sent[xor_counter]  = (msg_to_be_sent[xor_counter] ^ xor_password[xor_counter]);
		}

		/** Publishes a message*/
#if(SSL_EN)
		mqttClient.publish(topic, msg_to_be_sent, msg_to_be_sent_len);
#else
		client.publish(topic, msg_to_be_sent, msg_to_be_sent_len);
#endif

		Serial.println("\nPublish!");
	}
}
/**************** LOOP ******************************************************/
