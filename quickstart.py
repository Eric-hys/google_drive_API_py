import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


#from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

class Gdrive():
    def __init__ (self):
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
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # store = file.Storage('token.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    # service = build('drive', 'v3', http=creds.authorize(Http()))
    #
    # # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=100, fields="nextPageToken, files(id, name)", q="'1RqrUDMy9M07R8db496bVNnRqlB3YqgLj' in parents and trashed = false").execute()
    # items = results.get('files', [])

    google_drive = Gdrive()

    items = google_drive.get_file('1RqrUDMy9M07R8db496bVNnRqlB3YqgLj')

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            # school_dir = service.files().list(
            #     pageSize=100, fields="nextPageToken, files(id, name)", q="'" + item['id'] + "' in parents and trashed = false").execute()
            # doc_list = school_dir.get('files', [])
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
