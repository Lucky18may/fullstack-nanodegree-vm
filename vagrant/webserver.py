from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/delete"):
            	restaurantid = self.path.split('/')[2]
            	rest = session.query(Restaurant).filter_by(id = restaurantid).one()
            	if rest:
            		self.send_response(200)
            		self.send_header('Content-type', 'text/html')
            		self.end_headers()
            		output = ""
            		output += "<html><body>"
            		output += "<h1>Are you sure you want to delete this %s</h1>" % rest.name
            		output += "<form method = 'POST' enctype = 'multipart/form-data' action = 'restaurant/%s/delete'>" % rest.id
            		output += "<input type = 'submit' value = 'Delete'>"
            		output += "</form>"
            		output += "</body></html>"
            		self.wfile.write(output)

            if self.path.endswith("/edit"):
            	restaurantid = self.path.split('/')[2]
            	rest = session.query(Restaurant).filter_by(id = restaurantid).one()
            	if rest:
            		self.send_response(200)
            		self.send_header('Content-type','text/html')
            		self.end_headers()
            		output = ""
            		output += "<html> <body>"
            		output += "<h1>%s</h1>" % rest.name
            		output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurant/%s/edit'>"%rest.id
            		output += "<input name = 'newrestaurant' type = 'text' placeholder = %s>"% rest.name
            		output += "<input type = 'submit' value = 'Rename'>"
            		output += "</form>"
            		output += "</body></html>"

            		self.wfile.write(output)
            		return

       	    if self.path.endswith("/restaurants/new"):
       	    	self.send_response(200)
       	    	self.send_header('Content-type', 'text/html')
       	    	self.end_headers()
       	    	output = ""
       	    	output += "<html><body>"
       	    	output += "<h1>Add new restaurant</h1>"
       	    	output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newrestaurant" type="text" placeholder = "newRestaurant" ><input type="submit" value="Create"> </form>'''
       	    	output += "</body></html>"
       	    	self.wfile.write(output)
       	    	print output
       	    	return


       	    if self.path.endswith("/restaurants"):
       	    	self.send_response(200)
       	    	self.send_header('Content-type', 'text/html')
       	    	self.end_headers()
       	    	
       	    	restaurants = session.query(Restaurant).all()
       	    	output = ""
       	    	output += "<html><body>"
       	    	output += "<h1> List of all Restaurants </h1>"
       	    	output += "</br> <a href=/restaurants/new>Add new restaurant</a></br></br>"
       	    	for rests in restaurants:
       	    		output += rests.name
       	    		output += "</br>"
       	    		output += "<a href= '/restaurant/%s/edit'> Edit </a>" % rests.id
       	    		output += "</br>"
       	    		output += "<a href= '/restaurant/%s/delete'> Delete </a>" % rest.id
       	    		output += "</br> </br> </br>"

       	    	output += "</body></html>"
       	    	self.wfile.write(output)
       	    	print output
       	    	return	

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):

        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newrestaurant')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
            	restaurantid = self.path.split('/')[2]
            	ctype,pdict = cgi.parse_header(
            		self.headers.getheader('Content-type'))
            	if ctype == 'multipart/form-data':
            		fields = cgi.parse_multipart(self.rfile, pdict)
            		messagecontent = fields.get('newrestaurant')
            		rest = session.query(Restaurant).filter_by(id = restaurantid).one()
            		if rest != []:
            		    rest.name = messagecontent[0]
            		    session.commit()
            		    self.send_response(301)
            		    self.send_header('Content-type', 'text/html')
            		    self.send_header('Location', '/restaurants')
            		    self.end_headers()

            if self.path.endswith("/delete"):
            	restaurantid = self.path.split('/')[2]
            	ctype, pdict = cgi.parse_header(
            		self.headers.getheader('Content-type'))
            	if ctype == 'multipart/form-data':
            		fields = cgi.parse_multipart(self.rfile,pdict)
            		messagecontent = fields.get('newrestaurant')
            		rest = session.query(Restaurant).filter_by(id = restaurantid).one()
            		if rest != []:
            			session.delete(rest)
            			session.commit()
            			self.send_response(301)
            		    self.send_header('Content-type', 'text/html')
            		    self.send_header('Location', '/restaurants')
            		    self.end_headers()

             		    



        except:
            pass       


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()