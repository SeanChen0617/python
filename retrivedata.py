import urllib.request
import json
import csv
import datetime

class MFRetriever:
    """ to retrieve recording data from MouseFlow and save to CSV """

    def __init__(self, email, token):
        self.email = email
        self.token = token
        print('calling getwebsites:' + str(datetime.datetime.now()))
        self.website_id = self.getwebsites(self.email, self.token)
        print('calling getpagelist:' + str(datetime.datetime.now()))
        self.getpagelist(self.email, self.token, self.website_id)
        print('calling getrecordings:' + str(datetime.datetime.now()))
        self.session_id = self.getrecordings(self.email, self.token, self.website_id)
        print('calling getpageviews:' + str(datetime.datetime.now()))
        self.getpageviews(self.email, self.token, self.session_id)
        print('done:' + str(datetime.datetime.now()))

    def getwebsites(self, email, token):
        """ retrieve website list """

        website_id = []

        data = urllib.request.urlopen('http://account.o.mouseflow.com/api/getwebsites?email=' + email + '&token=' + token).read().decode('utf-8')
        json_obj = json.loads(data)


        with open('website.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['ExcludedIpAddresses', 'Width', 'Id', 'PageIdentifiers', 'Recordings',
                                'RecordingStatus', 'Alignment', 'Name', 'Domains'])

            for x in json_obj['WebsiteList']:
                website_id.append(x['Id'])
                csvwriter.writerow([x['ExcludedIpAddresses'], x['Width'], x['Id'], x['PageIdentifiers'], x['Recordings'],
                                    x['RecordingStatus'], x['Alignment'], x['Name'], x['Domains']])

        return website_id

    def getpagelist(self, email, token, website_id):
        """ retrieve page list """

        pagelist_url = 'http://account.o.mouseflow.com/api/getpagelist?email=' + email + '&token=' + token + '&website='

        for wsid in website_id:
            data = urllib.request.urlopen(pagelist_url + wsid).read().decode('utf-8')
            json_obj = json.loads(data)

            with open(wsid+'_pagelist.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(['Id', 'URL', 'Title', 'Views30Days', 'AvgVisitLengthSec', 'AvgInteractionTimeSec',
                                    'BounceRate', 'ClicksPerPageView', 'LoadTimeMS',
                                    'GrabTimeMS', 'AvgScrollPercentage', 'PageHeight', 'HtmlSizeKB'])

                for x in json_obj['PageList']:
                    csvwriter.writerow([x['Id'], x['URL'], x['Title'], x['Views30Days'], x['AvgVisitLengthSec'],
                                        x['AvgInteractionTimeSec'], x['BounceRate'], x['ClicksPerPageView'], x['LoadTimeMS'],
                                        x['GrabTimeMS'], x['AvgScrollPercentage'], x['PageHeight'], x['HtmlSizeKB']])

    def getrecordings(self, email, token, website_id):
        """ retrieve recording list """

        session_id = []

        recording_url = 'http://account.o.mouseflow.com/api/getrecordings?email=' + email + '&token=' + token + '&website='
        other_param = '&datefrom=2015-1-1'

        for wsid in website_id:
            data = urllib.request.urlopen(recording_url + wsid + other_param).read().decode('utf-8')
            json_obj = json.loads(data)

            with open(wsid+'_recording.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(['Id', 'LastUpdated', 'IP', 'Country', 'CountryCode', 'Region', 'City', 'ISP',
                                    'Language', 'EntryUrl', 'PageCount', 'VisitLength', 'Browser', 'Device', 'UserAgent', 'OS', 'Referrer'])

                for x in json_obj['RecordingList']:
                    session_id.append([wsid, x['Id']])
                    csvwriter.writerow([x['Id'], x['LastUpdated'], x['IP'], x['Country'], x['CountryCode'], x['Region'], x['City'], x['ISP'],
                                        x['Language'], x['EntryUrl'], x['PageCount'], x['VisitLength'], x['Browser'], x['Device'], x['UserAgent'], x['OS'], x['Referrer']])

        return session_id

    def getpageviews(self, email, token, session_id):
        """ retrieve pageview list """

        pageview_url = 'http://account.o.mouseflow.com/api/getpageviews?email=' + email + '&token=' + token + '&website='
        other_param = '&datefrom=2015-1-1'

        for obj in session_id:
            data = urllib.request.urlopen(pageview_url + obj[0] + '&session=' + obj[1] + other_param).read().decode('utf-8')
            json_obj = json.loads(data)

            with open(obj[0]+'_pageview.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(['Id', 'Session', 'PageId', 'StartTime', 'EndTime', 'PageTitle', 'URL', 'QueryString',
                                    'FormInteraction', 'MaxScrolledPercentage', 'IP', 'Country', 'CountryCode', 'Region', 'City', 'ISP',
                                    'Language', 'VisitLength', 'ActiveVisitLength', 'Browser', 'Device', 'UserAgent', 'OS', 'Referrer'])

                for x in json_obj['PageViewList']:
                    csvwriter.writerow([x['Id'], x['Session'], x['PageId'], x['StartTime'], x['EndTime'], x['PageTitle'], x['URL'], x['QueryString'],
                                        x['FormInteraction'], x['MaxScrolledPercentage'], x['IP'], x['Country'], x['CountryCode'], x['Region'], x['City'], x['ISP'],
                                        x['Language'], x['VisitLength'], x['ActiveVisitLength'], x['Browser'], x['Device'], x['UserAgent'], x['OS'], x['Referrer']])
