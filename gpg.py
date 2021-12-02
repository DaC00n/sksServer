#!/usr/bin/python3
# Coded the 05-11-2021 By Mathieu L And Kevin D
##### SKS Server #####
import os
import sys
import gnupg
from pprint import pprint


# Defining two global variables to include into functions, the master generate key and the gpg directory


class GPG:
    PATH = '/home/serversks/.gnupg'

    def __init__(self, path='/home/serversks/.gnupg'):
        self.PATH = path
        if not os.path.isdir(self.PATH):
            self.masterKeyGeneration()
        self.key = 0
        self.GPG = gnupg.GPG(gnupghome=self.PATH)

    # Function to generate the keys of the server
    def masterKeyGeneration(self):
        os.system('if [ -d /home/serversks/.gnupg ]; then rm -drvf /home/serversks/.gnupg; fi')
        os.system('mkdir ' + self.PATH)
        self.GPG = gnupg.GPG(gnupghome=self.PATH)
        input = self.GPG.gen_key_input(
            name_email='serversks@masterkey.com',
            passphrase='letmyserverskspasswordbestrong',
            key_type='RSA',
            key_length=2048,
            subkey_type='RSA',
            subkey_length=2048)
        self.key = self.GPG.gen_key(input)
        self.key = str(self.key)
        print(self.key)
        return self.key

    # Function to export the server public key
    def exportKey(self):
        public_keys = self.GPG.list_keys(keys='server', sigs='TRUE')
        return self.GPG.export_keys(public_keys[0].get('fingerprint'))

    # Function to import new key to the server with a parameter
    def importKeyToServ(self, newKey):
        newKey = open(newKey).read()
        result = self.GPG.import_keys(newKey)
        pprint(result.results)
        public_key = self.GPG.list_keys(keys=result.fingerprints, sigs='TRUE')
        print(public_key)
        return result.results

    # Function to list all keys imported in the server
    def listKeys(self):
        public_keys = self.GPG.list_keys(sigs='TRUE')
        pprint(public_keys)
        return public_keys

    # Function to list keys with a specific keyword in parameter
    def searchKeys(self, keyword):
        result = self.GPG.list_keys(keys=keyword)
        pprint(result)
        return result
        
## Autosign try
##        mail = public_key[0].get('uids')
##        print(mail)
##        keyid = public_key[0].get('keyid')
##        print(keyid)
##        try:
##            with open("trustedKeyId", "r") as a_file:
##                for line in a_file:
##                    stripped_line = line.strip()
##                    if stripped_line == keyid:
##                        os.system('gpg -v --sign-key ' + mail)
##                        print("The key was signed !")
##        except:
##            print('An error occured')       