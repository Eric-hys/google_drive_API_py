import sys
import io

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class Gdrive():
    def __init__ (self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3', http = creds.authorize(Http()))

    def get_file(self, id):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize = 100, fields = "nextPageToken, files(id, name)", orderBy="folder, name",
            q = "'" + id + "' in parents and trashed = false").execute()
        items = results.get('files', [])

        return items

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    
    google_drive = Gdrive()
    # utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    items = google_drive.get_file(YOUR_DRIVE_ID)

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            model_list = google_drive.get_file(item['id'])

            if not model_list:
                print(u'{0} ({1})'.format(item['name'], item['id']))
                print("********************************************************")
            else:
                for model in model_list:
                    print(u'{0} ({1})'.format(model['name'], model['id']))
                    subject_list = google_drive.get_file(model['id'])
                    if not subject_list:
                        # print(u'{0} ({1})'.format(model['name'], model['id']))
                        print("********************************************************")
                    else:
                        for subject in subject_list:
                            print(u'    {0} ({1})'.format(subject['name'], subject['id']))
                            teaching_list = google_drive.get_file(subject['id'])
                            if not teaching_list:
                                print("    ****************************************************")
                            else:
                                for teaching in teaching_list:
                                    tdata_list = google_drive.get_file(teaching['id'])
                                    if not tdata_list:
                                        print(u'        {0} ({1})'.format(teaching['name'], teaching['id']))
                                        print("        ************************************************")
                                    else:
                                        for td in tdata_list:
                                            print(u'        {0} ({1})'.format(td['name'], td['id']))
                                            print("        ************************************************")

                # print("========================================================")

if __name__ == '__main__':
    main()
