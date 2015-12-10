'''
Created on 4 Dec 2015

@author: david
'''

from ftplib import FTP
from os import remove

class FTPExt:
    def __init__(self):
        self.pwd = [x.strip() for x in open("/home/david/Python/pwd")][0]
        self.ftp = FTP('nicmach.comxa.com')
        self.ftp.login('a8558342', self.pwd)
        self.ftp.cwd('public_html/data')
    def ListFile(self):
        self.ftp.retrlines('LIST')
    def BusyCheck(self):
        self.Download('busy.txt')
        temp = open('busy.txt')
        b = temp.read()
        temp.close()
        if b == '0':
            temp = open('busy.txt', 'w')
            temp.write('1')
            temp.close()
            self.Upload('busy.txt')
            remove('busy.txt')
            return False
        else:
            remove('busy.txt')
            return True
    def MakeAvailable(self):
        temp = open('busy.txt','w')
        temp.write('0')
        temp.close()
        self.ftp.cwd('/public_html/data')
        self.Upload('busy.txt')
        remove('busy.txt')
    def Download(self, filename, filepath=''):
        self.ftp.retrbinary('RETR %s'%filename, open(filepath + filename, 'wb').write)
    def Upload(self, filename, filepath=''):
        self.ftp.storbinary('STOR %s'%filename, open(filepath + filename))
    def UploadData(self, energy, detector):
        self.ftp.cwd(detector)
        self.Download(str(energy), '%s/'%detector)
        temp = open('%s/%s'%(detector,energy), 'a')
        for i in open('%s/%s.data'%(detector,energy)):
            temp.write(i.strip()+'\n')
        temp.close()
        self.Upload(str(energy),'%s/'%detector)
    def Exit(self):
        '''Please use before terminating script'''
        self.ftp.quit()
