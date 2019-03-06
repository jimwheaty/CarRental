from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from api.models import Observation, Amenities, Company, Email, Volunteer, Price, Admin
from werkzeug import generate_password_hash
import json, random, string, bcrypt, demjson
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

        
def funcLogin(request):

    method = request.method
    if method == "POST":    

        body = json.loads(request.body)
        username = "NULL"
        given_password = "NULL" 
        # Read the json
        try:
            username = body['username']
            print(username)
        except:
            return HttpResponseBadRequest("400 Bad Request: No username given")
        try:
            given_password = body['password']
            print('given password',given_password)
        except:
            return HttpResponseBadRequest("400 Bad Request: No password given")
        
        hashed_given_password = generate_password_hash(given_password)
        
        query_un = Volunteer.objects.raw("SELECT Volunteer_id  FROM Volunteer WHERE Username = \"" + username + "\" ;") 
        stored_un = 0
        for it in query_un:
            stored_un = stored_un + 1
        if stored_un == 0: 
            return HttpResponseBadRequest("400 Bad Request: Invalid Username")
            
        query_pwd = Volunteer.objects.raw("SELECT Volunteer_id, Password FROM Volunteer WHERE Username = "+"\"" + username + "\";") 
        stored_hash = None
        for it in query_pwd:
            stored_hash = it.password
        isSamePassword = bcrypt.checkpw(given_password, stored_hash)
        if (stored_hash == None) or (isSamePassword == False):
            return HttpResponseBadRequest("400 Bad Request: Wrong password")
        
        
        token=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        cursor = connection.cursor()
        cursor.execute("UPDATE Volunteer SET Token = \"" + str(token) + "\" WHERE Username = \"" + username + "\";")
        response = JsonResponse({'X-OBSERVATORY-AUTH' : token})
        response.__setitem__("Access-Control-Allow-Origin", "*")
        return response
    return HttpResponseBadRequest("400 Bad Request: Unknown command")   
        
def funcLogout(request):
    method = request.method
    if method == "POST" or method == "OPTIONS":    
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        print(request.META)
        print(str(token))
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + str(token) + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            print(1)
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")
        cursor = connection.cursor()
        cursor.execute("UPDATE Volunteer SET Token = NULL WHERE Token = \"" + str(token) + "\";")
        response = JsonResponse({ "message" : "OK" })
        response.__setitem__("Access-Control-Allow-Origin", "*")
        return response        
        #an apotyxei to query ti kanw???
    return HttpResponseBadRequest("400 Bad Request: Unknown command")              
        
def funcSignup(request):

    method = request.method
    if method == "POST":    
        body = json.loads(request.body)
        username = "NULL"
        given_password = "NULL" 
        # Read the json
        try:
            username = body['username']
            username.encode('utf-8')
        except:
            return HttpResponseBadRequest("400 Bad Request: No username given")
        try:
            given_password = body['password']
            given_password.encode('utf-8')
        except:
            return HttpResponseBadRequest("400 Bad Request: No password given")
        salt = bcrypt.gensalt()
        hashed_given_password = bcrypt.hashpw(given_password.encode('utf8'), salt)
        
        hashed_given_password.startswith(salt)
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Username = \"" + username + "\";") 
        stored_un = 0
        for it in query_un:
            stored_un = stored_un + 1
        if stored_un != 0:
            return HttpResponseBadRequest("400 Bad Request: Username already in use")
                
        
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Volunteer(Volunteer_id, Username, Password, Token) VALUES (NULL, \"" + username + "\"" + ", \"" + str(hashed_given_password) + "\", \"" + token + "\");")
        response = JsonResponse({'X-OBSERVATORY-AUTH' : token})
        response.__setitem__("Access-Control-Allow-Origin", "*")
        return response
    return HttpResponseBadRequest("400 Bad Request: Unknown command") 


def funcProducts(request):
    cursor = connection.cursor()
    method = request.method
    # GET Products
    if method == "GET":	

        start = request.GET.get('start')
        if int(start) < 0:
            return HttpResponseBadRequest("400 Bad Request")
        if start is None:
            start = 0
        count = request.GET.get('count')
        if count is None:
            count = 0
        if int(count) < 0:
            return HttpResponseBadRequest("400 Bad Request")
        status = request.GET.get('status')
        if (status != "ACTIVE") and (status != "ALL") and (status != "WITHDRAWN") and (status != None):
            return HttpResponseBadRequest("400 Bad Request")
        if (status is None) or (status == "ACTIVE"):
            status = "false"
        elif status == "WITHDRAWN":
            status = "true"
        sort = request.GET.get('sort')
        if sort is None:
            sort = "id|DESC"
       
        spl = sort.split("|")
        name_id = spl[0]
        if name_id == "id":
            name_id = "Observation_id"
        order = spl[1]
        products = []
        total = 0

        if status != "ALL":
            products = Observation.objects.raw("SELECT * FROM Observation WHERE Withdrawn = \"" + status + "\" ORDER BY " + str(name_id) + " " + str(order) + " LIMIT " + str(count) + " OFFSET " + str(start) + ";")
            tot = Observation.objects.raw("SELECT * FROM Observation WHERE Withdrawn = \"" + status + "\";")
            total = 0
            for t in tot:
                total = total + 1
        else:
            products = Observation.objects.raw("SELECT * FROM Observation" + 
                                                    " ORDER BY " + str(name_id) + " " + str(order) +
                                                    " LIMIT " + str(count) + 
                                                    " OFFSET " + str(start) + ";")
            tot = Observation.objects.raw("SELECT * FROM Observation;")
            total = 0
            for t in tot:
                total = total + 1

        i = 0
        for p in products:
            i = i + 1

        # Check for 404 NOT FOUND
        if i == 0:
            return HttpResponseNotFound("404 Not Found")  

        # Create json
        js = {} 
        js["start"] = int(start)
        js["count"] = min(int(count), int(total))
        js["total"] = total
        i = 0
        d = []
        for p in products:
            i = i + 1
            dd = {}
            dd["id"] = p.observation_id
            dd["name"] = p.name
            if p.name == None:
                return HttpResponseBadRequest("400-Bad Request")
            if p.description != None:
                dd["description"] = p.description
            dd["category"] = p.category

            # Get tags (amenities)
            amenities = Amenities.objects.raw("SELECT 1 as id, Amenity FROM Amenities WHERE Amenities.Observation_id = " + str(p.observation_id) + ";")
            j = 0
            for a in amenities:
                j = j + 1

            if j != 0:
                amen = []  
                for a in amenities:
                    amen.append(a.amenity)    
                dd["tags"] = amen

            if p.withdrawn == "false":
                dd["withdrawn"] = False
            else:
                dd["withdrawn"] = True

            # ExtraData
            ddd = {}
            if p.location != None:
                ddd["location"] = p.location
            if p.company_name != None:
                ddd["company_name"] = p.company_name
            if p.ranking != None:
                ddd["ranking"] = p.ranking
            if p.x != None:
                ddd["x"] = p.x
            if p.y != None:
                ddd["y"] = p.y
            if p.validation != None:
                ddd["validation"] = p.validation
            if p.stars != None:
                ddd["stars"] = p.stars

            dd["extraData"] = ddd
            
            d.append(dd)

        js["products"] = d

        return JsonResponse(js)

    # POST Products
    elif method == "POST":
        print(request.Meta)
        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        print("takis in Post " ,token)
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        body = json.loads(request.body)
        description = "NULL"
        category = "NULL" 
        amenities = "NULL"
        withdrawn = "DEFAULT" 
        extraData = "NULL"
        # Read the json
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
 
            # Check for duplicate name
            query = Company.objects.raw("SELECT Company_id FROM Company WHERE Name = \"" + name + "\";")
            counter = 0
            for n in query:
                counter = counter + 1
                if counter != 0:
                    return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 
        except:
            return HttpResponseBadRequest("400 Bad Request: No name given")
        try:
            description = body['description']
            description = "\"" + description + "\""
        except:
            print()
        try:
            category = body['category']
        except:
            return HttpResponseBadRequest("400 Bad Request: No category given")
        try:
            amenities = body['tags']
            if isinstance(amenities, list) == False:
                return HttpResponseBadRequest("400 Bad Request, Invalid Amenities(Tags)")
        except:
            print()
        try:
            extraData = body['extraData']
            if isinstance(extraData, dict) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            print()

        # Do the post         
        # τρεχουμε for πανω στο tags το οποιο ειναι [...] και φτιαχνουμε τα amenities 
        # και υστερα για το extraData το οποιο ειναι dictionary {...}

        location = "NULL"
        stars = "NULL"
        validation = "NULL"
        x = "NULL"
        y = "NULL"
        ranking = "DEFAULT"
        cheer_count = "DEFAULT"
        company_name = "NULL"
        company_id = "NULL"
        volunteer_id = "NULL"
       
        try:
            location = extraData['location']
            location = "\"" + location + "\""
        except:
            print()
        try:
            stars = extraData['stars']
            stars = str(stars)
        except:
            print()
        try:
            x = str(extraData['x'])
        except:
            print()
        try:
            y = str(extraData['y'])
        except:
            print()
        try:
            company_name = extraData['company_name']
            company_name = "\"" + company_name + "\""
        except:
            print()
        try:
            volunteer_id = str(extraData['volunteer_id'])
        except: 
            print()
        
        company_id = "NULL"      
        if company_name != "NULL":   
            query_cid = Observation.objects.raw("SELECT Company_id FROM Company WHERE Company_name = " + company_name + ";")
            for q_cid in query_cid:
                company_id = q_cid.company_id
        
        cursor.execute("INSERT INTO Observation (Observation_id, Name, X, Y, Stars, Location, Description, Company_name, Volunteer_id, Company_id, Category, Withdrawn, Cheer_count, Ranking) VALUES (NULL" + ", \"" + name + "\", " + str(x) + ", " + str(y) + ", " + str(stars) + ", " + location + ", " + description + ", " + company_name + ", " + volunteer_id + ", " + str(company_id) + ", \"" + str(category) + "\", DEFAULT, DEFAULT, DEFAULT);")

        query_oid = Observation.objects.raw("SELECT Observation_id, MAX(Observation_id) AS MaxID FROM Observation GROUP BY Observation_id;") 
        maxid = None
        for it in query_oid:
            maxid = it.MaxID
        if maxid != None:
            for amen in amenities:
                cursor.execute("INSERT INTO Amenities (Observation_id, Amenity) VALUES (" + str(maxid) + ", \"" + str(amen) + "\");")
        else:
            return HttpResponseServerError("Http Response Server Error")
       
        return JsonResponse({ "message": "OK" })

    else:
        return HttpResponseBadRequest("400 Bad Request")        

def funcProductsId(request, pid):
    cursor = connection.cursor()
    method = request.method 
    # GET Products ID  
    if method == "GET":	
        if pid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")
        
        # Check if given id is valid
        query_id = Observation.objects.raw("SELECT * FROM Observation WHERE Observation_id = " + str(pid) + ";")
        tot = 0
        for product in query_id:
            tot = tot + 1
        if tot == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")

        # Create JSON
        js = {}
        js["id"] = pid
        js["name"] = product.name
        if product.description != None:
            js["description"] = product.description       
        js["category"] = product.category
        # Get tags (amenities)
        amenities = Amenities.objects.raw("SELECT 1 as id, Amenity FROM Amenities WHERE Amenities.Observation_id = " + str(pid) + ";")
        j = 0
        for a in amenities:
            j = j + 1

        if j != 0:
            amen = []  
            for a in amenities:
                amen.append(a.amenity)    
            js["tags"] = amen

        if product.withdrawn == "true":
            js["withdrawn"] = True
        else:
            js["withdrawn"] = False

        # ExtraData
        d = {}
        if product.location != None:
            d["location"] = product.location
        if product.company_name != None:
            d["company_name"] = product.company_name
        if product.ranking != None:
            d["ranking"] = product.ranking
        if product.x != None:
            d["x"] = product.x
        if product.y != None:
            d["y"] = product.y
        if product.validation != None:
            d["validation"] = product.validation
        if product.stars != None:
            d["stars"] = product.stars

        js["extraData"] = d

        return JsonResponse(js)

    # DELETE Products
    elif method == "DELETE":
        user = False
        admin = False
        # Authenticate Admin
        password = request.META.get('HTTP_X_OBSERVATORY_AUTH_ADMIN')
        if password != None:        
            query_un = Admin.objects.raw("SELECT Password, 1 as id FROM Admin;") 
            count = 0
            for it in query_un:
                stored_hash = it.password
                count = count + 1
            if count == 0:
                admin = False
            isSamePassword = bcrypt.checkpw(password, stored_hash)
            if isSamePassword == True:
                admin = True;
 
        if admin == False:
            # Authenticate User
            token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
            if token is None:
                return HttpResponseBadRequest("400 Bad Request: No Token")
            #### SQL INJECTION
            query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token =  %s ", [token]) 
            count = 0
            for it in query_un:
                count = count + 1
            if count == 0:
                return HttpResponseBadRequest("400 Bad Request: Invalid User")
            user = True

        # Check if given id is valid
        query_id = Observation.objects.raw("SELECT * FROM Observation WHERE Observation_id = " + str(pid) + ";")
        tot = 0
        for product in query_id:
            tot = tot + 1
        if tot == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")

        # Check if ID is given
        if pid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")
        
        # User
        if (admin == False) and (user == True):       
            cursor.execute("UPDATE Observation SET Withdrawn = \"true\" WHERE Observation_id = " + str(pid) + ";")

        # Admin
        if (admin == True): 
            cursor.execute("DELETE FROM Observation WHERE Observation_id = " + str(pid) + ";")
     
        return JsonResponse({ "message": "OK" })

    # PUT Products
    elif method == "PUT":
        cursor = connection.cursor()

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        if pid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Observation.objects.raw("SELECT Observation_id FROM Observation WHERE Observation_id = " + str(pid) + ";") 
        count = 0
        for it in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")        

        # Get body
        body = json.loads(request.body)
        description = "NULL"
        category = "NULL"
        amenities = "NULL"
        withdrawn = "NULL"

        # Read the json
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Name\" should be not null")
        try:
            description = body['description']
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Description\" should be not null") 
        try:
            category = body['category']
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Category\" should be not null")  
        try:
            amenities = body['tags']
            # Check for list
            if isinstance(amenities, list) == False:
                return HttpResponseBadRequest("400 Bad Request, Invalid Amenities")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Tags\" should be not null")
        try:
            withdrawn = body['withdrawn']
            withdrawn = str(withdrawn) 
            if withdrawn == "True":
                withdrawn = "true"
            elif withdrawn == "False":
                withdrawn = "false"
            if (withdrawn != "false") and (withdrawn != "true"):
                return HttpResponseBadRequest("400 Bad Request, Invalid Withdrawn")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Withdrawn\" should be not null")        

        # Check for duplicate name
        query = Observation.objects.raw("SELECT Observation_id FROM Observation WHERE Name = \"" + name + "\";")
        counter = 0
        for n in query:
            counter = counter + 1
        if counter != 0:
            return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 

        # den xreiazetai h COALESCE gt ta exw elegxei gia not null..
        #print("UPDATE Observation SET Name = COALESCE(\"" + name + "\" , Name), Description = COALESCE(\"" + description + "\", Description),  Category = COALESCE(\"" + category + "\", Category), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Observation_id = " + str(pid) + ";")

        cursor.execute("UPDATE Observation SET Name = COALESCE(\"" + name + "\" , Name), Description = COALESCE(\"" + description + "\", Description),  Category = COALESCE(\"" + category + "\", Category), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Observation_id = " + str(pid) + ";")

        # Update tags (amenities)             
        for amen in amenities:
            cursor.execute("INSERT INTO Amenities (Observation_id, Amenity) VALUES (" + str(pid) + ", \"" + str(amen) + "\");")

        return JsonResponse({ "message": "OK" })

    # PATCH Products
    elif method == "PATCH":
        cursor = connection.cursor()

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        if pid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Observation.objects.raw("SELECT Observation_id FROM Observation WHERE Observation_id = " + str(pid) + ";") 
        count = 0
        for it in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")        

        # Get body
        body = json.loads(request.body)
        name = "NULL"
        description = "NULL"
        withdrawn = "DEFAULT" 
        category = "NULL"
        amenities = "NULL"

        # Read the json
        # Number of columns = 5 + 1(ID)
        count = 5
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request, Invalid Name")

            # Check for duplicate name
            query = Observation.objects.raw("SELECT Observation_id FROM Observation WHERE Name = \"" + name + "\";")
            counter = 0
            for n in query:
                counter = counter + 1
                if counter != 0:
                    return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 
        except:
            count = count - 1
        try:
            description = body['description']
        except:
            count = count - 1
        try:
            category = body['category']
        except:
            count = count - 1 
        try:
            amenities = body['tags']
            # Check for list
            if isinstance(amenities, list) == False:
                return HttpResponseBadRequest("400 Bad Request, Invalid Amenities")
        except:
            count = count - 1
        try:
            withdrawn = body['withdrawn']
            withdrawn = str(withdrawn) 
            if withdrawn == "True":
                withdrawn = "true"
            elif withdrawn == "False":
                withdrawn = "false"
            if (withdrawn != "false") and (withdrawn != "true"):
                return HttpResponseBadRequest("400 Bad Request, Withdrawn")
        except:
            count = count - 1
        
        # Check for Invalid Patch    
        if count != 1:    
            return HttpResponseBadRequest("400 Bad Request, Invalid Patch")        

        # Execute PATCH Request Query
        if isinstance(amenities, list) == False:
            cursor.execute("UPDATE Observation SET Name = COALESCE(\"" + name + "\" , Name), Description = COALESCE(\"" + description + "\", Description), Category = COALESCE(\"" + category + "\", Category), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Observation_id = " + str(pid) + ";")

            return JsonResponse({ "message": "OK" })
        
        # Update tags (emails)             
        for amen in amenities:
            cursor.execute("INSERT INTO Amenities (Observation_id, Amenity) VALUES (" + str(pid) + ", \"" + str(amen) + "\");")

        return JsonResponse({ "message": "OK" })

    else:
        return HttpResponseBadRequest("400 Bad Request")

def funcShops(request):
    cursor = connection.cursor()
    method = request.method
    # GET Shops
    if method == "GET":
        start = request.GET.get('start')
        if start is None:
            start = 0
        if int(start) < 0:
            return HttpResponseBadRequest("400 Bad Request")
        count = request.GET.get('count')
        if count is None:
            count = 0
        if int(count) < 0:
            return HttpResponseBadRequest("400 Bad Request")
        status = request.GET.get('status')
        if (status is None) or (status == "ACTIVE"):
            status = "false"
            status = "true"
        if (status != "ACTIVE") and (status != "ALL") and (status != "WITHDRAWN") and (status != None):
            return HttpResponseBadRequest("400 Bad Request")
        sort = request.GET.get('sort')
        if sort is None:
            sort = "id|DESC"

        spl = sort.split("|")
        name_id = spl[0]
        if name_id == "id":
            name_id = "Company_id"
        order = spl[1]             
        shops = []

        if status != "ALL":
            shops = Company.objects.raw("SELECT * FROM Company WHERE Withdrawn = \"" + str(status) + "\" ORDER BY " + str(name_id) + " " + str(order) + " LIMIT " + str(count) + " OFFSET " + str(start) + ";")
            tot = Company.objects.raw("SELECT * FROM Company WHERE Withdrawn = \"" + str(status) + "\";")
            total = 0
            for t in tot:
                total = total + 1
        else:
            shops = Company.objects.raw("SELECT * FROM Company" + 
                                                    " ORDER BY " + str(name_id) + " " + str(order) +
                                                    " LIMIT " + str(count) + 
                                                    " OFFSET " + str(start) + ";")
            tot = Company.objects.raw("SELECT * FROM Company;")
            total = 0
            for t in tot:
                total = total + 1

        i = 0
        for p in shops:
            i = i + 1

        if i == 0:
            return HttpResponseNotFound("404 Not Found")

        # Create json
        js = {} 
        js["start"] = int(start)
        js["count"] = min(int(count), int(total))
        js["total"] = total
        i = 0
        d = []
        for c in shops:
            i = i + 1
            dd = {}
            dd["id"] = c.company_id
            dd["name"] = c.name
            if c.name == None:
                return HttpResponseBadRequest("400-Bad Request")
            if c.address != None:
                dd["address"] = c.address
            if c.lng == None:
                HttpResponseBadRequest("400-Bad Request")
            dd["lng"] = c.lng            
            if c.lat == None:
                HttpResponseBadRequest("400-Bad Request")
            dd["lat"] = c.lat

            # Get tags (emails)
            emails = Email.objects.raw("SELECT 1 as id, Email FROM Email WHERE Email.Company_id = " + str(p.company_id) + ";")
            j = 0
            for e in emails:
                j = j + 1

            if j != 0:
                mails = []  
                for e in emails:
                    mails.append(e.email)    
                dd["tags"] = mails

            if p.withdrawn == "true":
                dd["withdrawn"] = True
            else:
                dd["withdrawn"] = False
            
            d.append(dd)

        js["shops"] = d

        return JsonResponse(js)        

    # POST Shops
    elif method == "POST":

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        body = json.loads(request.body)
        address = "NULL"
        withdrawn = "DEFAULT" 

        # Read the json
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request: No name given")
        try:
            address = body['address']
            # First should be capital
            if address[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
            address = "\"" + address + "\""
        except:
            print()
        try:
            lng = body['lng']
            # Check for float
            if isinstance(lng, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request: No lng given")
        try:
            lat = body['lat']
            # Check for float
            if isinstance(lat, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request: No lat given")
        try:
            emails = body['tags']
            # Check for list
            if isinstance(emails, list) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            print()

        # Do the post         
#       company_id = "NULL"      
#        if company_name != "NULL":   
#           query_cid = Observation.objects.raw("SELECT Company_id FROM Company WHERE Company_name = " + company_name + ";")
#           for q_cid in query_cid:
#               company_id = q_cid.company_id
        

        # Check for duplicate name
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Name = \"" + name + "\";")
        counter = 0
        for n in query:
            counter = counter + 1
        if counter != 0:
            return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 


        cursor.execute("INSERT INTO Company (Company_id, Name, Address, Lng, Lat, Withdrawn) VALUES (NULL" + ", \"" + name + "\", " + address + ", " + str(lng) + ", " + str(lat) + ", DEFAULT);")

        query_oid = Company.objects.raw("SELECT Company_id, MAX(Company_id) AS MaxID FROM Company GROUP BY Company_id;") 
        maxid = None
        for it in query_oid:
            maxid = it.MaxID
        if maxid != None:
            for mail in emails:
                query = Email.objects.raw("SELECT Email as id FROM Email WHERE Email = \"" + str(mail) + "\";")
                counter = 0
                for em in query:
                    counter = counter + 1
                if counter != 0:
                    return HttpResponseBadRequest("400 Bad Request, Email Already Exists")
                cursor.execute("INSERT INTO Email (Company_id, Email) VALUES (" + str(maxid) + ", \"" + str(mail) + "\");")
        else:
            return HttpResponseServerError("Http Response Server Error")
       
        return JsonResponse({ "message": "OK" })
        
    else:
        return HttpResponseBadRequest("400 Bad Request")


def funcShopsId(request, sid):
    method = request.method  
    # GET Shops ID 
    if method == "GET":	
        if sid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Company_id = " + str(sid) + ";") 
        count = 0
        for s in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID") 

        # Create JSON
        js = {}
        js["id"] = sid
        js["name"] = s.name
        if s.address != None:
            js["address"] = s.address       
        js["lng"] = s.lng
        js["lat"] = s.lat
 
        # Get tags (emails)
        emails = Email.objects.raw("SELECT 1 as id, Email FROM Email WHERE Email.Company_id = " + str(sid) + ";")
        j = 0
        for e in emails:
            j = j + 1

        if j != 0:
            mails = []  
            for e in emails:
                mails.append(e.email)    
            js["tags"] = mails

        if s.withdrawn == "true":
            js["withdrawn"] = True
        else:
            js["withdrawn"] = False

        return JsonResponse(js)
    
    # DELETE Shops
    elif method == "DELETE":

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        cursor = connection.cursor()
        if sid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Company_id = " + str(sid) + ";") 
        count = 0
        for it in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID") 
        
        # Volunteer auth        
        cursor.execute("UPDATE Company SET Withdrawn = \"true\" WHERE Company_id = " + str(sid) + ";")

        # Admin auth
        #cursor.execute("DELETE FROM Company WHERE Company_id = " + str(sid) + ";")
     
        return JsonResponse({ "message": "OK" })

    # PUT Shops
    elif method == "PUT":
        cursor = connection.cursor()

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")


        if sid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Company_id = " + str(sid) + ";") 
        count = 0
        for it in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")        

        # Get body
        body = json.loads(request.body)
        address = "NULL"
        withdrawn = "DEFAULT" 
        lng = "NULL"
        lat = "NULL"
        emails = "NULL"
        withdrawn = "NULL"

        # Read the json
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Name\" should be not null")
        try:
            address = body['address']
            address = address
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Address\" should be not null") 
        try:
            lng = body['lng']
            # Check for float
            if isinstance(lng, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Lng\" should be not null") 
        try:
            lat = body['lat']
            # Check for float
            if isinstance(lat, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Lat\" should be not null") 
        try:
            emails = body['tags']
            # Check for list
            if isinstance(emails, list) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Tags\" should be not null")
        try:
            withdrawn = body['withdrawn']
            withdrawn = str(withdrawn) 
            if withdrawn == "True":
                withdrawn = "true"
            elif withdrawn == "False":
                withdrawn = "false"
            if (withdrawn != "false") and (withdrawn != "true"):
                return HttpResponseBadRequest("400 Bad Request, Withdrawn")
        except:
            return HttpResponseBadRequest("400 Bad Request, Field \"Withdrawn\" should be not null")        

        # Check for duplicate name
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Name = \"" + name + "\";")
        counter = 0
        for n in query:
            counter = counter + 1
        if counter != 0:
            return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 

        # den xreiazetai h COALESCE gt ta exw elegxei gia not null..
        print("UPDATE Company SET Name = COALESCE(\"" + name + "\" , Name), Address = COALESCE(\"" + address + "\", Address), Lng = COALESCE(" + str(lng) + ", Lng), Lat = COALESCE(" + str(lat) + ", Lat), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Company_id = " + str(sid) + ";")
        cursor.execute("UPDATE Company SET Name = COALESCE(\"" + name + "\" , Name), Address = COALESCE(\"" + address + "\", Address), Lng = COALESCE(" + str(lng) + ", Lng), Lat = COALESCE(" + str(lat) + ", Lat), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Company_id = " + str(sid) + ";")

        # Update tags (emails)             
        for mail in emails:
            query = Email.objects.raw("SELECT Email as id FROM Email WHERE Email = \"" + str(mail) + "\";")
            counter = 0
            for em in query:
                counter = counter + 1
            if counter != 0:
                return HttpResponseBadRequest("400 Bad Request, Email Already Exists")
            cursor.execute("INSERT INTO Email (Company_id, Email) VALUES (" + str(sid) + ", \"" + str(mail) + "\");")

        return JsonResponse({ "message": "OK" })

    # PATCH Shops
    elif method == "PATCH":
        cursor = connection.cursor()

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")


        if sid is None:
            return HttpResponseBadRequest("400 Bad Request: No id given")

        # Check if given id is valid
        query = Company.objects.raw("SELECT Company_id FROM Company WHERE Company_id = " + str(sid) + ";") 
        count = 0
        for it in query:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid ID")        

        # Get body
        body = json.loads(request.body)
        name = "NULL"
        address = "NULL"
        withdrawn = "DEFAULT" 
        lng = "NULL"
        lat = "NULL"
        emails = "NULL"
        withdrawn = "NULL"

        # Read the json
        # Number of columns = 6 + 1(ID)
        count = 6
        try:
            name = body['name']
            # Chech if Name is a valid name in human language
            if name[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request, Invalid Name")

            # Check for duplicate name
            query = Company.objects.raw("SELECT Company_id FROM Company WHERE Name = \"" + name + "\";")
            counter = 0
            for n in query:
                counter = counter + 1
                if counter != 0:
                    return HttpResponseBadRequest("400 Bad Request, Name Already Exists") 
        except:
            count = count - 1
        try:
            address = body['address']
            if address[0].istitle() == False:
                 return HttpResponseBadRequest("400 Bad Request")
            address = address
        except:
            count = count - 1
        try:
            lng = body['lng']
            # Check for float
            if isinstance(lng, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            count = count - 1 
        try:
            lat = body['lat']
            # Check for float
            if isinstance(lat, float) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            count = count - 1 
        try:
            emails = body['tags']
            # Check for list
            if isinstance(emails, list) == False:
                return HttpResponseBadRequest("400 Bad Request")
        except:
            count = count - 1
        try:
            withdrawn = body['withdrawn']
            withdrawn = str(withdrawn) 
            if withdrawn == "True":
                withdrawn = "true"
            elif withdrawn == "False":
                withdrawn = "false"
            if (withdrawn != "false") and (withdrawn != "true"):
                return HttpResponseBadRequest("400 Bad Request, Withdrawn")
        except:
            count = count - 1
        
        # Check for Invalid Patch    
        if count != 1:    
            return HttpResponseBadRequest("400 Bad Request, Invalid Patch")        

        # Execute PATCH Request Query
        if isinstance(emails, list) == False:
            cursor.execute("UPDATE Company SET Name = COALESCE(\"" + name + "\" , Name), Address = COALESCE(\"" + address + "\", Address), Lng = COALESCE(" + str(lng) + ", Lng), Lat = COALESCE(" + str(lat) + ", Lat), Withdrawn = COALESCE(\"" + withdrawn + "\", Withdrawn) WHERE Company_id = " + str(sid) + ";")

            return JsonResponse({ "message": "OK" })
        
        # Update tags (emails)             
        for mail in emails:
            query = Email.objects.raw("SELECT Email as id FROM Email WHERE Email = \"" + str(mail) + "\";")
            counter = 0
            for em in query:
                counter = counter + 1
            if counter != 0:
                return HttpResponseBadRequest("400 Bad Request, Email Already Exists")
            cursor.execute("INSERT INTO Email (Company_id, Email) VALUES (" + str(sid) + ", \"" + str(mail) + "\");")

        return JsonResponse({ "message": "OK" })

    else:
        return HttpResponseBadRequest("400 Bad Request")

def funcPrices(request):

    method = request.method
    if method == "POST":    
        body = json.loads(request.body)

        # Authenticate User
        token = request.META.get('HTTP_X_OBSERVATORY_AUTH')
        if token is None:
            return HttpResponseBadRequest("400 Bad Request: No Token")
        query_un = Volunteer.objects.raw("SELECT Volunteer_id FROM Volunteer WHERE Token = \"" + token + "\";") 
        count = 0
        for it in query_un:
            count = count + 1
        if count == 0:
            return HttpResponseBadRequest("400 Bad Request: Invalid Token")

        
        price = "NULL"
        dateFrom = "NULL" 
        dateTo = "NULL"
        observation_id = "DEFAULT" 
        company_id = "DEFAULT" 
        # Read the json
        try:
            price = body['price']
        except:
            return HttpResponseBadRequest("400 Bad Request: No price given")
        try:
            dateFrom= body['dateFrom']
        except:
            return HttpResponseBadRequest("400 Bad Request: No dateFrom given")
        try:
            dateTo= body['dateTo']
        except:
            return HttpResponseBadRequest("400 Bad Request: No dateTo given")
        try:
            observation_id = body['productId']
        except:
            return HttpResponseBadRequest("400 Bad Request: No productId  given")
        try:
            company_id = body['shopId']
        except:
            return HttpResponseBadRequest("400 Bad Request: No shopId  given")

        if isinstance(price, float) == False:
            return HttpResponseBadRequest("400 Bad Request: Price must be float")
        if isinstance(observation_id, int) == False:
            return HttpResponseBadRequest("400 Bad Request: ProductId must be int")
        if isinstance(company_id, int) == False:
            return HttpResponseBadRequest("400 Bad Request: ShopId must be int")

             
        query_cid = Company.objects.raw("SELECT Company_id FROM Company WHERE Company_id = " + str(company_id) + ";")
        cnt=0
        for q_cid in query_cid:
            cnt = cnt + 1
        if cnt == 0:
            return HttpResponseBadRequest("400 Bad Request: ShopId is invalid")
        
        query_oid = Observation.objects.raw("SELECT Observation_id FROM Observation WHERE Observation_id = " + str(observation_id) + ";")
        cnt = 0
        for o_cid in query_oid:
            cnt = cnt + 1
        if cnt == 0:
            return HttpResponseBadRequest("400 Bad Request: ProductId is invalid")
        
        cursor = connection.cursor()
        
        from datetime import date, timedelta
        yF=dateFrom[0:4]
        mF=dateFrom[5:7]
        dF=dateFrom[8:10]
        d1=date(int(yF), int(mF), int(dF))
        yT=dateTo[0:4]
        mT=dateTo[5:7]
        dT=dateTo[8:10]
        d2=date(int(yT), int(mT), int(dT))
        delta = d2 - d1  # timedelta
        date = "NULL"
        for i in range(delta.days + 1):
            date_temp =(d1 + timedelta(i))
            date = '-'.join(str(x) for x in (date_temp.month, date_temp.day, date_temp.year))
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Price (Price_id, Price, Date, Observation_id, Company_id) VALUES (NULL, " + str(price) + " , \"" + date + "\" , " + str(observation_id) + " , " +  str(company_id) + ");")

        return JsonResponse({ "message": "OK" })

    else:
        return HttpResponseBadRequest("400 Bad Request")   



