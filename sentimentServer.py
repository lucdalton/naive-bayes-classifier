# The server that will accept post requests with the tweet that needs to be analysed
# The tweet needs to be sent as a form parameter as tweet=
# Initialise server with an instance of a classifier
# This is a shit design for the class, I couldn't get it to work the way I wanted
# so gave up and settled for something that just works.

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
from BaseHTTPServer import HTTPServer
from NBClassifier import NBClassifier
import json

print 'loading training data....'
classifier = NBClassifier('pos_tweets', 'neg_tweets')

class SentimentServer(BaseHTTPRequestHandler):

    def get_sentiment(self, tweet):
        return classifier.test_sentence_result(tweet)

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        # Begin the response
        self.send_response(200)
        self.end_headers()
        
        # Echo back information about what was posted in the form
        amountSent = len(form.keys())
        
        i = 0
        self.wfile.write('[')
        for key in form.keys():
            #print key
            sent_data = form[key].value;
            

            returnData = self.get_sentiment(sent_data)
            #returnData = self.someClassifier.test_sentence_result(sent_data)
            

            returnData['text'] = sent_data
            self.wfile.write(json.dumps(returnData))
            if (i < amountSent -1):
                self.wfile.write(',')
                i += 1
        self.wfile.write(']')
        return

    def __init(self, someClassifier):
        self.sentimentClassifier = someClassifier

#server = HTTPServer(('localhost', 8080), SentimentServer)

server = HTTPServer(('localhost', 8080), SentimentServer)

print 'Done..\nStarting server, use <Ctrl-C> to stop'
server.serve_forever()