# Throughtek-Kalay-Mock-Attack

- Alexander Castro
- Mock Implementaion of the Vulnerable ThroughTek-Kalay MiTM Attack
- Reference: https://threatpost.com/bug-iot-millions-devices-attackers-eavesdrop/168729/

---

## Components:

    Registation-Server
        - Mock implementation of a Kalay cloud server that tracks the registration of IoT devices
          using a stateful datastore (sqlite3). 
        - Camera devices can register themselves with this server and they will recieve back their
          registration creds
        - Clients will need to request for camera device creds using the secrect UUID, before
          they're able to request for camera footage. 
    
    Camera
        - Mock implementation of a registered IoT device that captures audio/video footage and 
          serves it up to authenticated users. 
        - Requires (device-UUID, device-username, device-password) for proper authentication
    
    Client
        - Mock implementation of a authenticated mobile application that would be used to remotely
          view the camera footage
        - Requests for the camera device creds from the registration server and provides those 
          creds to the camera to start recieving a stream of camera footage
    
    Attacker
        - Spoofed camera that can act as a middle man in the communication between the client and the camera
        - This is done by registering itself with the same UUID as the target camera, so that whenever a client
          goes to request device creds, it will be directed at the attacker
        - The attack will then forward the creds given to it by the client to the camera in order to spy on the 
          camera footage. The attack will also fork a copy of the camera feed and forward it back to the client 
          in order to remain under the radar

---

## Normal Transaction
![Screenshot](documentation/ThroughTekNormalTransaction.drawio.png)

---

## Attacker Interception
![Screenshot](documentation/ThroughTek-Kalay-Diagrams-Attacker-Intercept.drawio.png)