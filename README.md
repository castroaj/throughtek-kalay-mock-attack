# Throughtek-Kalay-Mock-Attack

## OVERVIEW
    TEAM MEMBERS: Alexander Castro, Nicolas Lorenzo, Nongnapat Adchariyavivit, AlReheeq AlMaktum Al Rawas
    DESCRIPTION: Mock Implementaion of the Vulnerable ThroughTek-Kalay MiTM Attack
    PURPOSE: CYSE-580 Technical Demonstration

---

## REFERENCES

    NEWS: 
     - https://thehackernews.com/2021/06/critical-throughtek-flaw-opens-millions.html 
     - https://aws.plainenglish.io/the-throughtek-kalay-vulnerability-is-absolutely-absurd-heres-why-it-should-worry-you-fe222549dd0d  
     - https://industrialcyber.co/news/critical-vulnerability-found-in-throughtek-kalay-p2p-sdk-can-remotely-exploit-millions-of-iot-devices/ 
     - https://techxplore.com/news/2021-08-vulnerability-iot-devices-throughtek-kalay.html 
     - https://www.mandiant.com/resources/blog/mandiant-discloses-critical-vulnerability-affecting-iot-devices 

    MODELS: 
     - https://threatpost.com/bug-iot-millions-devices-attackers-eavesdrop/168729/ 

    CVE:  
     - https://unit42.paloaltonetworks.com/iot-supply-chain-cve-2021-28372/  

    CISA Report: 
     - https://www.cisa.gov/news-events/ics-advisories/icsa-21-229-01 

---

## REQUIREMENTS (UBUNTU/DEBIAN LINUX SERVER WAS TESTED)

### python3 & pip3 (Tested with 3.8)

```bash
apt install python3
apt install python3-pip
```

### sqlite3

```bash
apt install sqlite3
```

### flask

```bash
pip3 install flask
```

## COMPONENTS

    NOTE: START PROCESSES IN THE ORDER THAT FOLLOWS
    
    Registation-Server 
        - Mock implementation of a Kalay cloud server that tracks the registration of IoT devices
          using a stateful datastore (sqlite3). 
        - Camera devices can register themselves with this server and they will recieve back their
          registration creds
        - Clients will need to request for camera device creds using the secrect UUID, before
          they're able to request for camera footage. 

        HOW TO START (1):
        =============
        cd registration-server;
        python3 registration_server.py;
    
    Camera
        - Mock implementation of a registered IoT device that captures audio/video footage and 
          serves it up to authenticated users. 
        - Requires (device-UUID, device-username, device-password) for proper authentication

        HOW TO START (2):
        =============
        cd camera;
        // Configure the camera_config.yaml
        python3 camera.py;
    
    Client
        - Mock implementation of a authenticated mobile application that would be used to remotely
          view the camera footage
        - Requests for the camera device creds from the registration server and provides those 
          creds to the camera to start recieving a stream of camera footage

        HOW TO START (3):
        =============
        cd client;
        // Configure the client_config.yaml
        python3 client.py;
    
    Attacker
        - Spoofed camera that can act as a middle man in the communication between the client and the camera
        - This is done by registering itself with the same UUID as the target camera, so that whenever a client
          goes to request device creds, it will be directed at the attacker
        - The attack will then forward the creds given to it by the client to the camera in order to spy on the 
          camera footage. The attack will also fork a copy of the camera feed and forward it back to the client 
          in order to remain under the radar

        HOW TO START (4):
        =============
        cd attacker;
        // Configure the attacker_config.yaml
        python3 attacker.py;
---

## Normal Transaction
![Screenshot](documentation/ThroughTekNormalTransaction.drawio.png)

---

## Attacker Interception
![Screenshot](documentation/ThroughTek-Kalay-Diagrams-Attacker-Intercept.drawio.png)

---

## Technical Demo
https://github.com/castroaj/throughtek-kalay-mock-attack/assets/49505648/5cbc9f03-4c28-4041-b8ca-3c61ce844e06

