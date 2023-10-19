import os
import requests

#Creating a class
class ILovePDFAPI:

    #initialising
    def __init__(self, api_key):

        self.api_key = api_key
        self.api_url = r'https://api.ilovepdf.com/v1/start'
        self.tasks = {
            'merge': 'merge',
            'split': 'split',
            'unlock': 'unlock',
            'extract_text': 'text',
            'image_to_pdf': 'imagepdf',
        }
    
    #program to vreate the task
    def create_task(self, task_name, file):

        #making the request url
        url = f'{self.api_url}/{self.tasks[task_name]}'
        headers = {
            'Authorization': f'token {self.api_key}'
        }

        data = {
            'task': 'create'
        }

        #getting response
        response = requests.post(url, headers=headers, data=data)

        #If the webpage works it will send code '200'
        if response.status_code == 200:
            task_id = response.json()['task']
            return task_id
        else:
            print(f'Error Creating task: {response.status_code}')
            return None

    #Function to upload the PDF files:
    def upload_file(self, task_id, file_path):

        #Making the upload url
        url = f'{self.api_url}/upload'
        headers = {
            'Authorization': f'token {self.api_key}'
        }

        data = {
            'task': 'create'
        }

        files = {
            'file': open(file_path, 'rb')
        }

        response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            return True
        else:
            print(f'Error Uploading file: {response.status_code}')
            return False
        
    
    #Finally performing the task
    def execute_task(self, task_id, output_path):
        url = f'{self.api_url}/process'
        headers = {
            'Authorization': f'token {self.api_key}'
        }

        data = {
            'task': task_id
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            result_url = response.json()['server']
            self.download_result(result_url, output_path)
        else:
            print(f'Error Executing task: {response.status_code}')

    #Retrieving the finished pdf file
    def download_result(self, result_url, output_path):
        response = requests.get(result_url)

        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f'Result Saved to: {output_path}')
        else:
            print(f'Error Downloading result: {response.status_code}')
#Creating the main function
def main():
    #Get a API security key from ILOVEPDF's webpage
    #Given is a free API key which allows only 250 files/month
    api_key = r'secret_key_d1dd3593e04e27c97d91795b9fe1c823_m_PPI00cd339ac1b92b91b6d417b9a704abe5'


    #Creating an object of the class while passing API key
    ilovepdf = ILovePDFAPI(api_key)

    while True:

        #MAin menu:
        print("\nChoose an action:")
        print("1. Combine two or more PDF files into one single PDF.") #To merge PDF
        print("2. Separate PDF pages or extract all pages into a PDF.") #To split PDF
        print("3. Remove PDF password security for reading and editing.") #Removing Password
        print("4. Extract all text from a PDF file to a TXT file.") #Getting data in text formate
        print("5. Convert JPG, TIFF, and PNG images to PDF.") #Image to PDf
        print("6. Exit")
        choice = input("Enter your choice: ")

        #To merge PDF
        if choice == '1':
            input_files = input("Enter the paths of the PDF files to combine (comma-separated):").split(',') #Getting the original PDFs
            output_file = input("Enter the path to save the file: ")
            task_id = ilovepdf.create_task('merge', input_files)
            for file in input_files:
                ilovepdf.upload_file(task_id, file)
            ilovepdf.execute_task(task_id, output_file)

        #To split PDF
        elif choice == '2':
            input_file = input("Enter the path of the PDF file to split: ")
            output_dir = input("Enter the directory to save the split pages: ")
            task_id = ilovepdf.create_task('split', input_file)
            ilovepdf.upload_file(task_id, input_file)
            ilovepdf.execute_task(task_id, output_dir)

        #Removing Password
        elif choice == '3':
            input_file = input("Enter the path of the PDF file to remove password security: ")
            output_file = input("Enter the path for the output PDF file: ")
            task_id = ilovepdf.create_task('unlock', input_file)
            ilovepdf.upload_file(task_id, input_file)
            ilovepdf.execute_task(task_id, output_file)

        #Getting data in text formate
        elif choice == '4':
            input_file = input("Enter the path of the PDF file to extract text: ")
            output_file = input("Enter the path for the output TXT file: ")
            task_id = ilovepdf.create_task('extract_text', [input_file])
            ilovepdf.upload_file(task_id, input_file)
            ilovepdf.execute_task(task_id, output_file)

        #Image to PDf
        elif choice == '5':
            input_images = input("Enter the paths of the images to convert (comma-separated): ").split(',')
            output_file = input("Enter the path for the output PDF file: ")
            task_id = ilovepdf.create_task('image_to_pdf', input_images)
            for image in input_images:
                ilovepdf.upload_file(task_id, image)
            ilovepdf.execute_task(task_id, output_file)

        #Exiting the program
        elif choice == '6':
            break

if __name__ == '__main__':
    main()