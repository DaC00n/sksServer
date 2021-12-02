Instructions to launch the SKS Server

Install the dependencies :
sudo pip install flask
sudo apt install gnupg
sudo apt install python3

Download postman here and extract the content in the directory of your choice:
https://dl.pstmn.io/download/latest/linux64

Create a user dedicated named serversks :
sudo adduser serversks
sudo usermod -aG sudo serversks

Connect to the serversks session and paste the content of all the repo :
su - serversks
cp <PreviousDirectoryLocation> /home/serversks/

Launch the server (The server keys will be generated once at the first launch):
sudo ./app.py

Time to play with Postman.
Launch Postamn and click on "import", selecting the "CryptoAPI_Python.postman_collection"

The Get List will list all the keys you got.

The Post upload will allow you to import a public key to the server.
You will need to change the value of the "file" into the body request to add the public key file that you want.

The Get search will find a key link to the keyword in parameter.
You can try to look for "server" into the get request to see your server public key informations.

The Get exportMaster will allow you to export your public key, usefull if you want to transmit it to another server.

NEED TO IMPROVE
You can add your trusted key ids' into the file trustedKeyId. 
It will automatically sign imported keys which are signed by these key ids'.

Tips to export a public key :
gpg --output <keyName> --armor --export <keyIdentifier>
