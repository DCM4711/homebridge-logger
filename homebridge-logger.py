##############################
# HOMEBRIDGE-LOGGER          #
# AUTHOR: DCM4711            #
# VERSION: 0.1               #
# DATE: 2024-JUL-21          #
# LICENSE: GPLv3             #
##############################

import os
import time
import re
import mysql.connector
from datetime import datetime

debugmode = False # Provide additional console logging info
logfile_path = "/var/lib/homebridge/homebridge.log"
reconnectLogAfterLogCount = 1000 # Reconnect to the logfile after this number of written logfile lines

dbuser = "root"             # Change to MYSQL user
dbpassword = "password"     # Change to password of MYSQL user
dbname = 'homekitdb'
dbhost = '127.0.0.1'        # Leave '127.0.0.1' if the MYSQL server runs on the same machine as Homebridge

dbconnection = mysql.connector.connect(host=dbhost,
                                    database=dbname,
                                    user=dbuser,
                                    password=dbpassword,
                                    auth_plugin='mysql_native_password')


# Function to execute an SQL command with authentication
def execute_sql(sqlquery):

    try:
        cursor = dbconnection.cursor()
        cursor.execute(sqlquery)
        dbconnection.commit()
        if (debugmode): print(f"SQL: {sqlquery}")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into table {}".format(error))

    finally:
        if dbconnection.is_connected():
            pass
            #dbconnection.close()
            #print("MySQL connection is closed")

# Look for specific device logs
devices = ["[HS100]","[Shelly]","zigbee2mqtt/","[homebridge-webos-tv]"]
devicesprettyname = ["HS100","Shelly","MQTT","TV"]
devicetables = ["HS100_tbl","Shelly_tbl","Zibee2MQTT_tbl","WebOSTV_tbl"]

# The 'deviceproperties' variable contains a string unique to messages from a specific device type (Homepridge Plugin)
# Put messages that can be filtered most precisely at the beginning of the array (and filter array)
deviceproperties = ["","","","","","","",""]
# The propertyfilter is a regex string that matches all needed values within one string for a specific message type
devicepropertiesfilters = ["","","","","","","",""]
devicepropertiesnames = ["","","","","","","",""]
mostrecentmessage = ["","","","","","","",""]

#  Codes for propertynames are used to define the property types of the values matched by the regex filter:
#  These codes also determine the database column names
#   D = Devicename;
#   B = Battery (%);
#   E = Energy (W);
#   S = Switch
#   I = Illuminance
#   P = Pressure
#   H = Humidity
#   T = Temperature
#   O = Occupancy
#   C = Contact
#   V = Vibration (true)
#   L = Water leak (true)
#   C# = TV Channel Number
#   CN = TV Channel Name



# ************************************
# ***** DEVICE DEFINITIONS START *****
# ************************************

# ****************************** HS100 ******************************
#   [1/9/2024, 3:19:46 PM] [HS100] [Living Room Light] Updating [Outlet.On] false
#   [1/9/2024, 11:53:10 PM] [HS100] [Living Room Light] Updating [Outlet.On] true

properties = ['Updating [Outlet.On]']
propertyfilter = ['.*\[(.*)\].*Updating \[Outlet\.On\] (.*e)']
propertynames = ['D|S']

deviceproperties[0] = properties
devicepropertiesfilters[0] = propertyfilter
devicepropertiesnames[0] = propertynames
mostrecentmessage[0] = ""

# ****************************** Shelly ******************************
#   [1/9/2024, 3:14:11 PM] [Shelly] power0 of device SHPLG-S 0206F3 changed to 2.47
#   [1/9/2024, 9:16:23 PM] [Shelly] relay0 of device SHPLG-S 51C803 changed to false
properties = ['power0 of device',
              'relay0 of device']

propertyfilter = ['power0 of device (.*) changed to (.*)',
                  'relay0 of device (.*) changed to (.*e)'] # Need to match for the 'e' in truE/falsE as last character, otherwise the string will contain ANSI color codes

propertynames = ['D|E',
                 'D|S']

deviceproperties[1] = properties
devicepropertiesfilters[1] = propertyfilter
devicepropertiesnames[1] = propertynames
mostrecentmessage[1] = ""

# ****************************** zigbee2mqtt/ ******************************
#   [1/10/2024, 6:42:48 PM] [Wasserleck Bad] Received MQTT: zigbee2mqtt/BAD_LEAK01 = {"battery":100,"battery_low":false,"device_temperature":23,"last_seen":"2024-01-10T18:42:48+00:00","linkquality":73,"power_outage_count":21,"tamper":false,"voltage":3015,"water_leak":true}
#   [1/10/2024, 6:16:06 PM] [Eingang Gitter] Received MQTT: zigbee2mqtt/EG_GRID01 = {"action":"vibration","angle":24,"angle_x":5,"angle_x_absolute":85,"angle_y":-71,"angle_y_absolute":161,"angle_z":18,"battery":100,"device_temperature":15,"last_seen":"2024-01-10T18:16:06+00:00","linkquality":70,"power_outage_count":444,"strength":25,"vibration":true,"voltage":3155}
#   [1/9/2024, 11:17:18 PM] [Luftfeuchte Arbeitszimmer] Received MQTT: zigbee2mqtt/AZ_TEMP = {"battery":83,"humidity":76.55,"last_seen":"2024-01-09T23:17:18+00:00","linkquality":99,"power_outage_count":49943,"pressure":1008.8,"temperature":20.76,"voltage":2975}
#   [1/9/2024, 10:21:25 PM] [Schalter Arbeitszimmer] Received MQTT: zigbee2mqtt/AZ_SWITCH01 = {"action":"single_right","battery":100,"device_temperature":21,"last_seen":"2024-01-09T22:21:25+00:00","linkquality":76,"power_outage_count":283,"voltage":3055}
#   [1/10/2024, 5:42:21 PM] [Fenster Schlafzimmer] Received MQTT: zigbee2mqtt/SZ_WINDOW01 = {"battery":100,"contact":false,"device_temperature":17,"last_seen":"2024-01-10T17:42:21+00:00","linkquality":42,"power_outage_count":33,"voltage":3015}
#   [1/9/2024, 11:22:22 PM] [Bewegung Arbeitszimmer] Received MQTT: zigbee2mqtt/AZ_MOTION01 = {"battery":100,"device_temperature":21,"illuminance":21,"illuminance_lux":21,"last_seen":"2024-01-09T23:22:22+00:00","linkquality":86,"occupancy":true,"power_outage_count":90,"voltage":3025}
#   [1/9/2024, 3:19:47 PM] [Helligkeit Außen] Received MQTT: zigbee2mqtt/OUT_BRIGHTNESS01 = {"battery":100,"illuminance":21336,"illuminance_lux":136,"last_seen":"2024-01-09T15:19:47+00:00","linkquality":65,"voltage":3300}

properties = ['water_leak', # Water leak
              'angle_x_absolute', # Vibration sensor
              '= {"battery":', # Temperature sensor
              '= {"battery":', # Occupancy sensor
              '= {"battery":', # Contact switch
              ' = {"action":', # Switch
              '= {"battery":'] # Brightness sensor
propertyfilter = ['Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*water_leak":([a-zA-Z_]+)', # Water leak sensor
                  'Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*,"vibration":([a-zA-Z_]+),', # Vibration sensor
                  'Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*humidity":([0-9\.]+),.*pressure":([0-9\.]+),.*temperature":([0-9\.]+),', # Temperature sensor
                  'Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*illuminance_lux":([0-9\.]+),.*occupancy":([a-zA-Z_]+),', # Occupancy sensor
                  'Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*contact":([a-zA-Z_]+),', # Contact switch
                  'Received MQTT: zigbee2mqtt/(.*) = {"action":"([a-zA-Z_]+)".*battery":([0-9\.]+),', # Switch
                  'Received MQTT: zigbee2mqtt/(.*) =.*battery":([0-9\.]+),.*illuminance_lux":([0-9\.]+),'] # Brightness sensor
propertynames = ['D|B|L', # Water leak
                 'D|B|V', # Vibration sensor
                 'D|B|H|P|T', # Temperature sensor
                 'D|B|I|O', # Occupancy sensor
                 'D|B|C', # Contact switch
                 'D|S|B', # Switch
                 'D|B|I'] # Brightness sensor

deviceproperties[2] = properties
devicepropertiesfilters[2] = propertyfilter
devicepropertiesnames[2] = propertynames
mostrecentmessage[2] = ""

# ****************************** [homebridge-webos-tv] ******************************
#   [1/9/2024, 3:39:38 PM] [homebridge-webos-tv] [LG TV] TV power status changed, status:  state: Active, processing: Request Power Off,
#   [1/9/2024, 3:40:39 PM] [homebridge-webos-tv] [LG TV] TV power status changed, status:  state: Suspend, processing: Screen On,
#   [1/9/2024, 3:40:39 PM] [homebridge-webos-tv] [LG TV] Channel changed. Current channel: 24, Syfy HD, channelId: 3_32_24_0_13_13014_1537
#   [1/9/2024, 3:40:40 PM] [homebridge-webos-tv] [LG TV] TV turned on!
#   [1/9/2024, 3:43:26 PM] [homebridge-webos-tv] [LG TV] TV power status changed, status:  state: Suspend,
#   [1/9/2024, 3:43:26 PM] [homebridge-webos-tv] [LG TV] TV turned off!

#   [1/10/2024, 1:14:15 AM] [homebridge-webos-tv] [LG TV] TV power status changed, status:  state: Active, processing: Request Power Off,
#   [1/10/2024, 1:14:43 AM] [homebridge-webos-tv] [LG TV] TV power status changed, status:  state: Active Standby, processing: Prepare Power On,


properties = ["Channel changed. Current channel:",
              "state: Active, processing: Request Power Off",
              "state: Active Standby, processing: Prepare Power On"]
propertyfilter = ['.*\[homebridge-webos-tv\].*\[(.+)\].*Channel changed. Current channel: ([0-9]+), (.+),',
                  '.*\[homebridge-webos-tv\].*\[(.+)\].*state: Active, processing: Request Power ([a-zA-Z_]+)',
                  '.*\[homebridge-webos-tv\].*\[(.+)\].*state: Active Standby, processing: Prepare Power ([a-zA-Z_]+)']
propertynames = ['D|C#|CN',
                 'D|S',
                 'D|S']

deviceproperties[3] = properties
devicepropertiesfilters[3] = propertyfilter
devicepropertiesnames[3] = propertynames
mostrecentmessage[3] = ""


# ************************************
# *****       CODE START         *****
# ************************************

def file_was_replaced(logfile_path, last_inode, last_size):
    """Check if the file was replaced by comparing inodes and sizes."""
    try:
        stat = os.stat(logfile_path)
        return stat.st_ino != last_inode or stat.st_size < last_size
    except FileNotFoundError:
        return True  # File does not exist, consider it replaced

def get_file_inode(logfile_path):
    """Get the inode of the file."""
    try:
        return os.stat(logfile_path).st_ino
    except FileNotFoundError:
        return None

def follow(logfile_path):
    """ Continuously yield new lines in a log file, handling file rotation/replacement. """
    last_inode = get_file_inode(logfile_path)
    msgCount = 0
    while True:
        try:
            with open(logfile_path, "r") as log_file:
                log_file.seek(0,2)  # Move to the end of the file initially
                while True:
                    current_inode = get_file_inode(logfile_path)
                    if current_inode != last_inode:
                        # File has been rotated or replaced; break to re-open
                        print("Reopen Logfile after Logfile change")
                        last_inode = current_inode
                        break

                    line = log_file.readline()
                    msgCount = msgCount + 1
                    if (msgCount > reconnectLogAfterLogCount):
                        msgCount = 0
                        print(f"Reopen Logfile after {reconnectLogAfterLogCount} records!")
                        last_inode = current_inode
                        break
                    if not line:
                        time.sleep(0.1)  # Sleep briefly if no new line
                        continue
                    yield line
        except FileNotFoundError:
            # Handle the case where the file might temporarily disappear during rotation
            time.sleep(1)

def main():
    msgCount = 0
    for line in follow(logfile_path):

        msgCount = msgCount + 1

        if (debugmode == True): print(line, end='') # Uncomment to print every log message

        deviceindex = 0
        for matchdevice in devices:

            if line.find(matchdevice) > 0:
                #print(f"Found device: {matchdevice} ({deviceindex}) >> look for properties: {deviceproperties[deviceindex]}")

                filterindex = 0
                for matchproperty in deviceproperties[deviceindex]:
                    #print(f"Check for device: {deviceproperties[deviceindex]}")
                    #print(f"Check for property: {matchproperty}")
                    #print(f"{matchdevice} >> ",line, end='')

                    if line.find(matchproperty) > 0:

                        if (debugmode == True): print(f"{matchdevice} >>",line, end='')

                        filter = devicepropertiesfilters[deviceindex][filterindex]
                        result = re.search(rf"{filter}", line)

                        if (result):
                            if (debugmode == True): print(f"Filter({filterindex}) = {filter} ---> result = MATCH")
                        else:
                            if (debugmode == True): print(f"Filter({filterindex}) = {filter} ---> result = NO")

                        #result = re.search(r"power0 of device (.*) changed", line)
                        if (result):
                            data = result.groups()
                            resultstring = f"{devicesprettyname[deviceindex]} ({deviceindex}) >> "
                            propertynames = devicepropertiesnames[deviceindex][filterindex]
                            properties = propertynames.split('|')

                            sqlcolums = ""
                            sqlvalues = ""
                            sqldummyvalues = ""
                            sqlquery = f"INSERT INTO {devicetables[deviceindex]} (ServerTimestamp,"

                            valuearray = []
                            for x in range(len(data)):
                                resultstring += properties[x] + ":" + data[x] + "; "

                                #   D = Devicename;
                                #   B = Battery (%);
                                #   E = Energy (W);
                                #   S = Switch
                                #   I = Illuminance
                                #   P = Pressure
                                #   H = Humidity
                                #   T = Temperature
                                #   O = Occupancy
                                #   C = Contact
                                #   V = Vibration (true)
                                #   L = Water leak (true)
                                #   C# = TV Channel Number
                                #   CN = TV Channel Name
                                if (properties[x] == 'D'): sqlcolums += '`Device`'
                                if (properties[x] == 'B'): sqlcolums += '`Battery`'
                                if (properties[x] == 'E'): sqlcolums += '`Energy`'
                                if (properties[x] == 'S'): sqlcolums += '`Switch`'
                                if (properties[x] == 'I'): sqlcolums += '`Illuminance`'
                                if (properties[x] == 'P'): sqlcolums += '`AtmosphericPressure`'
                                if (properties[x] == 'H'): sqlcolums += '`Humidity`'
                                if (properties[x] == 'T'): sqlcolums += '`Temperature`'
                                if (properties[x] == 'O'): sqlcolums += '`Occupancy`'
                                if (properties[x] == 'C'): sqlcolums += '`Contact`'
                                if (properties[x] == 'V'): sqlcolums += '`Vibration`'
                                if (properties[x] == 'L'): sqlcolums += '`Leak`'
                                if (properties[x] == 'C#'): sqlcolums += '`TVChannelNumber`'
                                if (properties[x] == 'CN'): sqlcolums += '`TVChannelName`'

                                comma = ''
                                quote = ''
                                resultdata = ''

                                if (x < len(data) - 1): comma = ','
                                if (properties[x] == 'D' or properties[x] == 'S' or properties[x] == 'O' or properties[x] == 'C'  or properties[x] == 'V' or properties[x] == 'L' or properties[x] == 'CN'):
                                    quote = "'" # String values need quotes
                                    resultdata = data[x]
                                else:

                                    # Logfiles seem to contain ANSI color codes, they must be removed before buiding the SQL statement as adding data to float columns will fail otherwise
                                    cleanstring = data[x]
                                    matches = re.findall(r"[-+]?\d*\.\d+|\d+", cleanstring)

                                    if matches:
                                        # Extract the first match and convert it to float
                                        resultdata = float(matches[0])

                                    else:
                                        resultdata = 0

                                sqlcolums = (f"{sqlcolums}{comma}")
                                sqlvalues += (f"{quote}{resultdata}{quote}{comma}")

                            if (resultstring != mostrecentmessage[deviceindex]): # Avoid logging the same message twice
                                mostrecentmessage[deviceindex] = resultstring

                                timestamp = datetime.now()
                                print(f"{timestamp} (#{msgCount}) >> {resultstring}")
                                sqlquery = (f"{sqlquery}{sqlcolums}) VALUES (NOW(),{sqlvalues});")
                                execute_sql(sqlquery)

                            break # This makes sure that only the most precise filter will match

                    filterindex += 1

            deviceindex += 1


if __name__ == "__main__":
    main()
