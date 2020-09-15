"""This is the worker class, it is responsible for handling all the tiring and difficult work. It is also the base of the application"""

#Imported modules
import shutil
import os
from datetime import datetime as dt
import subprocess
#Loading of Icons

#File extensions
PICTURES = ['.jpg','.jpe', '.png', '.ico', '.jpeg','.gif', '.tiff','.tif','.icns','.webp', '.ppm', '.pnm', '.pbm', '.tga', '.pcx', '.jp2','j2k', 'jpf','jpx','jpm','mj2', 'raw', 'bmp', 'xpm']
AUDIOS = ['.mp3', '.wav', '.pcm','.aiff', '.aac', '.ogg', '.wma', '.flac', '.alac', '.3ga', '.aa','.act', '.al','.bap','.cda','.dac','.mp2','.mpa','.oga']
VIDEOS = ['.mp4', '.avi', '.mov','.wmv','.flv','.avchd','.webm','.mkv','.ogv','.dirac', '.mpg', '.mpeg','.3gp','.nsv','.3g2','.svi','.m4v']
DOCUMENTS = ['.txt', '.pdf', '.doc', '.docx','.odt','.ftf','.tex','.wpd','.md', '.rtf']
#Main work

valid_paths = []


class Worker:
    """The class which does all the work"""
    def __init__(self,number,  file_types, source, from_directory, to_directory, mode):
        self.number = number
        self.file_types = file_types
        self.source = source
        self.from_directory = from_directory
        self.to_directory = to_directory
        self.mode = mode

        #This then changes the file types into a list of extensions for the method 'valid' to use to check
        #if a file extension is valid or not
        if self.file_types == 'Pictures':
            self.file_types = PICTURES
        elif self.file_types == 'Audios':
            self.file_types = AUDIOS
        elif self.file_types == 'Vidoes':
            self.file_types = VIDEOS
        elif self.file_types == 'Documents':
            self.file_types = DOCUMENTS

    def valid(self, path):
        #This is the method which checks to see if a generated file path is valid
        #It compares the extension of the generated file to self.source.
        #If the file extension is in self.soucre, the valid will return True. Else False
        if os.path.splitext(path)[1] in self.file_types:
            return True
        else:
            return False


    def move(self):
        if self.source == 'Directory':
            for root, folder, file in os.walk(self.from_directory):
                for filename in file:
                    path = os.path.join(root, filename)
                    if Worker.valid(self, path) == True:
                        valid_paths.append(path) #This list contains a number of paths which are valid
                for i in valid_paths: #Then this iterates through the valid paths and move them
                    try:
                        print(i)
                        shutil.move(i, self.to_directory)
                    except Exception as message:
                        file = open("logs.txt", "a")
                        print('Error: ',message)
                        time = str(dt.now())[:-7]
                        file.write(time+"\n"+str(message)+'\n')
                        file.close()
        elif self.source == 'Zip' or self.source == '7z': #7z makes everything easier so we just use the same alogorithmn for both
            #If the user's choice is a zip file...
            #The subprocess module is used to decompress the file into a tempoary place
            opening = subprocess.Popen(['7z', 'e', '-y', self.from_directory, '-otemp'], shell= True, stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin = subprocess.PIPE) 
            output = opening.stdout.read().decode().lower() #This is the output read from stdout
            if 'everything is ok' in output: #7z always include 'Everything is Ok' when the process is successful, so i use that to see if everything really went well
                print('Sucessfull')
                print(output)
                for root, folder, file in os.walk('temp'):
                    for filename in file:
                        path = os.path.join(root, filename)
                        if Worker.valid(self, path) == True:
                            valid_paths.append(path) #This list contains a number of paths which are valid
                    for i in valid_paths: #Then this iterates through the valid paths and move them
                        try:
                            print(i)
                            shutil.move(i, self.to_directory)
                        except Exception as message:
                            file = open("logs.txt", "a")
                            print('Error: ',message)
                os.remove(self.from_directory) #This will remove the tempoary file used to decompress the files
                if self.source == 'Zip':
                    process = subprocess.Popen(['7z', 'e'])
                shutil.move('temp', self.from_directory)

                            

    def copy(self):
        if self.source == 'Directory':
            for root, folder, file in os.walk(self.from_directory):
                for filename in file:
                    path = os.path.join(root, filename)
                    if Worker.valid(self, path) == True:
                        valid_paths.append(path) #This list contains a number of paths which are valid
                for i in valid_paths: #Then this iterates through the valid paths and move them
                    try:
                        print(i)
                        shutil.copy(i, self.to_directory)
                    except Exception as message:
                        file = open("logs.txt", "a")
                        print('Error: ',message)
                        time = str(dt.now())[:-7]
                        file.write(time+"\n"+str(message)+'\n')
                        file.close()

        elif self.source == 'Zip' or self.source == '7z': #7z makes everything easier so we just use the same alogorithmn for both
            #If the user's choice is a zip file...
            #The subprocess module is used to decompress the file into a tempoary place
            opening = subprocess.Popen(['7z', 'e', '-y', self.from_directory, '-otemp'], shell= True, stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin = subprocess.PIPE) 
            output = opening.stdout.read().decode().lower() #This is the output read from stdout
            if 'everything is ok' in output: #7z always include 'Everything is Ok' when the process is successful, so i use that to see if everything really went well
                print('Sucessfull')
                print(output)
                for root, folder, file in os.walk('temp'):
                    for filename in file:
                        path = os.path.join(root, filename)
                        if Worker.valid(self, path) == True:
                            valid_paths.append(path) #This list contains a number of paths which are valid
                    for i in valid_paths: #Then this iterates through the valid paths and move them
                        try:
                            print(i)
                            shutil.copy(i, self.to_directory)
                        except Exception as message:
                            file = open("logs.txt", "a")
                            print('Error: ',message)
                shutil.rmtree('temp') #This will remove the tempoary file used to decompress the files


    def start(self):
        #This is the method which starts everything
        if self.mode == 'move':      
            Worker.move(self)
            return True


        elif self.mode == 'copy':
            Worker.copy(self)
            return True
            













process = Worker('1', 'Vidoes', '7z', r'C:\Users\Lucretius\Desktop\Music.7z', r'C:\Users\Lucretius\Desktop\pics', 'move')
process.start()