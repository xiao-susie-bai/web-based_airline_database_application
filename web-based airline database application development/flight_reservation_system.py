#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Import Flask Library
import json
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib
from random import randint
from datetime import datetime
import ast
from decimal import *
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def last_month(this_year, this_month):
  if this_month == 1: 
    return (this_year - 1, 12)
  else:
    return (this_year, this_month - 1)

def is_date(date):
    
    if len(date) == 10 and len(date.split("-")) == 3:
        return True

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE flight_search_result'       #***(?)pending understanding
        cursor_cleaning.execute(query_cleaning)
        #CLEAN search result table every time 
        data = None
        staff = None
        customer = None
        agent = None
        try:
                username = session['username']
                if session['user_type'] == "customer":
                        customer = "customer"
                if session['user_type'] == "staff":
                        staff = "staff"
                if session['user_type'] == "agent":
                        agent = "agent"
                        
        except:
                username = None
        return render_template('page1.html', username = username, customer=customer, agent = agent, staff = staff)

#####################Flight_Search_Public##############################               


@app.route('/flight_search', methods = ['GET', 'POST'])
def flight_search():
        staff = None
        customer = None
        agent = None
        search_result_past = None
        search_result_future = None
        any_result = None
        try:
                username = session['username']
                if session['user_type'] == "customer":
                        customer = "customer"
                if session['user_type'] == "staff":
                        staff = "staff"
                if session['user_type'] == "agent":
                        agent = "agent"
                
        except:
                username = None
        cursor = conn.cursor()
        query = 'SELECT * FROM flight_search_result WHERE departure_time > CURRENT_TIMESTAMP()'        #***obtain the results from the "flight_search_result" table previously prepared in "/flight_search_process"
        cursor.execute(query)
        data_future = cursor.fetchall()

        cursor = conn.cursor()
        query = 'SELECT * FROM flight_search_result WHERE departure_time <= CURRENT_TIMESTAMP()'        #***obtain the results from the "flight_search_result" table previously prepared in "/flight_search_process"
        cursor.execute(query)
        data_past = cursor.fetchall()
        
        try:
            error = request.args["error"]
        except:
            error = None

        if len(data_future) != 0:
            search_result_future = "Data Available"
            any_result = "Yes"
        if len(data_past) != 0:
            search_result_past = "Data Available"
            any_result = "Yes"
        
    
        if len(data_future) != 0:
                for flight in data_future:
                        flight["flight_index"] = data_future.index(flight)   #*SPECIAL NOTICE: "indexing each data entry"(used later also)!!!
                print(data_future)
        print(search_result_past, search_result_future, len(data_future),data_past, any_result)
        try:
            arr_error = request.args["arr_error"]
            if arr_error == "No Error":
                arr_error = None
            else:
                arr_error = "Sorry, back trip date should be after departure date"
        except:
            arr_error = None
            
        return render_template('flight_search.html', arr_error = arr_error, error = error,customer = customer, staff = staff, agent = agent, search_result_past = search_result_past, search_result_future = search_result_future, data_future = data_future, data_past = data_past, any_result = any_result,  username = username)
        #no matter whether client has logged in or not, the same "No Result"! -> no use to pass in "username" variable!!!

@app.route('/flight_search_process', methods = ['GET', 'POST'])
def flight_search_process():
        arr_error = "No Error"
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE flight_search_result'    #******NECESSARY TO CLEAN RESULT_VIEW FIRST!!! IMPORTANT!!!
        cursor_cleaning.execute(query_cleaning)
        #CLEAN search result table every time 

        #request by departure and arrival airport
        departure_city = request.form["Departure"]
        arrival_city = request.form["Arrival"]
        dept_date = request.form["DepartureDate"]
        arr_date = request.form["BackDate"]
        #request by flight id
        airline = request.form["airline"]
        flight_id = request.form["flight_id"]
        dept_date_by_id = request.form["dept_date_by_ID"]


        if departure_city != "" and arrival_city!="":
            if dept_date:
            
                cursor = conn.cursor()
                
                if len(departure_city) == 3: 
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, price,flight_status FROM flight_with_city_with_price WHERE (departure_airport, arrival_airport, DATE(departure_time)) = (%s, %s,%s)'
                else: 
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, price,flight_status FROM flight_with_city_with_price WHERE (departure_city, arrival_city, DATE(departure_time)) = (%s, %s,%s)'
                cursor.execute(query, (departure_city, arrival_city, dept_date))
                data = cursor.fetchall()
                
            else:
                cursor = conn.cursor()
                
                if len(departure_city) == 3: 
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID,price,flight_status FROM flight_with_city_with_price WHERE (departure_airport, arrival_airport) = (%s, %s)'
                else: 
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID,price,flight_status FROM flight_with_city_with_price WHERE (departure_city, arrival_city) = (%s, %s)'
                cursor.execute(query, (departure_city, arrival_city))
                data = cursor.fetchall()
         
        elif airline != "" and flight_id != "":
                cursor = conn.cursor()
                query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, price, flight_status FROM flight_with_city_with_price WHERE (airline, flight_ID, DATE(departure_time)) = (%s, %s,%s)'
                cursor.execute(query, (airline, flight_id, dept_date_by_id))
                data = cursor.fetchall()
        else: data = ""         #??Question: so if the user didn't input "departure city" OR "arrival city" here, he will get NO RESULT instead of all probably matching results?

        for each in data:
                cursorx = conn.cursor()
                queryx = 'INSERT INTO flight_search_result (airline,flight_ID,departure_time, arrival_time,departure_airport, arrival_airport,flight_status, price) values (%s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(queryx, (each['airline'],each['flight_ID'],each['departure_time'], each['arrival_time'],each['departure_airport'], each['arrival_airport'],each['flight_status'],each['price']))
                conn.commit()
                
        # for return trip
        if arr_date != "":             #brilliant logic(reversal of "depart_city" and "arr_city"!!!)
            if is_date(arr_date) and is_date(dept_date) and arr_date < dept_date:
                arr_error = "Sorry, back trip date should be after departure date"
            else:
                cursor = conn.cursor()
                if len(departure_city) == 3: 
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, price FROM flight_with_city_with_price WHERE (departure_airport, arrival_airport, DATE(departure_time)) = (%s, %s,%s) '
                else:
                        query = 'SELECT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, price FROM flight_with_city_with_price WHERE (departure_city, arrival_city, DATE(departure_time)) = (%s, %s,%s) '
                cursor.execute(query, (arrival_city, departure_city, arr_date))
                data = cursor.fetchall()
                for each in data:
                        cursorx = conn.cursor()
                        queryx = 'INSERT INTO flight_search_result (airline,flight_ID,departure_time, arrival_time,departure_airport, arrival_airport,flight_status,price) values (%s, %s, %s, %s, %s, %s, %s,%s)'
                        cursor.execute(queryx, (each['airline'],each['flight_ID'],each['departure_time'], each['arrival_time'],each['departure_airport'], each['arrival_airport'],each['flight_status'],each['price']))
                        conn.commit()
                        
        return redirect(url_for('flight_search', arr_error = arr_error))

#####################Register##############################               

#Define route for register
@app.route('/register')
def register():          #*first need to determine which user type(, and then redirect user to different types of register page)!!!
        #print(request.form['user_type'])
        #user_type = request.form['user_type']
        #if user_type == "customer":
        return render_template('register_select_page.html')
        #if user_type == "booking_agent":
                #return render_template('user_register.html', booking_agent = "booking_agent")
        #if user_type == "airline_staff":
                #return render_template('user_register.html', airline_staff = "airline_staff")

@app.route('/registerRedirect', methods=['GET', 'POST'])
def registerRedirect():
        user_type = request.form['user_type']          #after knowing the user type, redirect the user to different types of register page!!!
        if user_type == "customer":
                return render_template('customer_register.html')
        if user_type == "booking_agent":
                return render_template('agent_register.html')
        if user_type == "airline_staff":
                 return render_template('staff_register.html')

#Authenticates the register
@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():             #get data from "customer" register page
        #grabs information from the forms
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        phone_number = request.form['phone_number']
        address_building_number = request.form['address_building_number']
        address_street = request.form['address_street']
        address_city = request.form['address_city']
        address_state = request.form['address_state']
        passport_number = request.form['passport_number']
        passport_expiration = request.form['passport_expiration']
        passport_country = request.form['passport_country']
        birthdate = request.form['birthdate']

        #Now: query the database to check whether the user has already registered before
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM retail_customer WHERE email = %s'
        cursor.execute(query, (email))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
                #If the previous query returns data, then user exists
                error = "This user already exists"
                return render_template('customer_register.html', error = error)
        else:
                ins = 'INSERT INTO retail_customer VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)'
                cursor.execute(ins, (email, hashlib.md5(password.encode("utf-8")).hexdigest(), name, phone_number, address_building_number, address_street, address_city,address_state, passport_number, passport_expiration, passport_country, birthdate))
                #***[Detail above:] Notice and remember the hashing of "password" string above!!!
                conn.commit()
                cursor.close()
                return render_template('page1.html')       #return to("render" here) index/welcome page (at this point, still not logged in yet -> so no additional parameter passed in)!

@app.route('/registerAuth_agent', methods=['GET', 'POST'])
def registerAuth_agent():
        #grabs information from the forms
        email = request.form['agent_email']
        password = request.form['agent_password']
        booking_agent_ID = request.form['booking_agent_ID']
                
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM booking_agency WHERE email = %s'
        cursor.execute(query, (email))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
                #If the previous query returns data, then user exists
                error = "This user already exists"
                return render_template('agent_register.html', error = error)
        else:
                ins = 'INSERT INTO booking_agency VALUES(%s,%s,%s)'
                cursor.execute(ins, (email, hashlib.md5(password.encode("utf-8")).hexdigest(), booking_agent_ID))
                conn.commit()
                cursor.close()
                return render_template('page1.html')

@app.route('/registerAuth_staff', methods=['GET', 'POST'])
def registerAuth_staff():
        #grabs information from the forms
        username = request.form['staff_username']
        password = request.form['staff_password']
        first_name = request.form['staff_first_name']
        last_name = request.form['staff_last_name']
        birthdate = request.form['staff_birthdate']
        airline = request.form['staff_airline']
        phone_number = request.form['phone_number']
        
       
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
                #If the previous query returns data, then user exists
                error = "This user already exists"
                return render_template('staff_register.html', error = error)
        else:
                cursor_airline = conn.cursor()
                #*****IMPORTANT: NOTICE FOREIGN KEY CONSTRAINT in the "Airline Staff" table!!!
                query_airline = 'SELECT * FROM airline WHERE name = %s'        #***IMPORTANT: Don't forget to deal with the situation when staff works for a NEW airline(check whether Airline exists first)!!!
                cursor_airline.execute(query_airline, (airline))
                data_airline = cursor_airline.fetchone()
                if (not data_airline):        #*****If "airline" does not exist before(violates foreign key constraint), insert this "airline" first!!!
                        ins_airline = 'INSERT INTO airline VALUES(%s)'
                        cursor_airline.execute(ins_airline, (airline))
                ins = 'INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s)'
                cursor.execute(ins, (username, hashlib.md5(password.encode("utf-8")).hexdigest(), first_name,last_name,birthdate,airline))
                conn.commit()
                cursor.close()
                if "," in phone_number:
                    phone_numer_list = phone_number.split(",")
                else:
                    phone_numer_list = []
                    phone_numer_list.append(phone_number)
                for num in phone_numer_list:
                    cursor_num = conn.cursor()
                    ins_num = "INSERT INTO phone_number VALUES(%s,%s)"
                    cursor_num.execute(ins_num, (username, num))
                    conn.commit()
                    cursor_num.close()
                        
                return render_template('page1.html')                        

##############################Login##############################               

#Define route for login
@app.route('/login')
def login():
        return render_template('user_login.html')                  

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
        #grabs information from the forms
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()
        if user_type == "customer":       #first judge which user type this is
                query = 'SELECT * FROM retail_customer WHERE (email, password) = (%s, %s)'
                cursor.execute(query, (username, hashlib.md5(password.encode("utf-8")).hexdigest()))       
        if user_type == "booking_agent":
                query = 'SELECT * FROM booking_agency WHERE (email, password) = (%s, %s)'
                cursor.execute(query, (username, hashlib.md5(password.encode("utf-8")).hexdigest()))     
        if user_type == "airline_staff":
                query = 'SELECT * FROM airline_staff WHERE (username, password) = (%s, %s)'
                cursor.execute(query, (username, hashlib.md5(password.encode("utf-8")).hexdigest()))     

        
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if(data):
                print("login success", user_type, username)
                #creates a session for the the user
                #session is a built in
                session['username'] = username
                if user_type == "customer":
                        session['user_type'] = "customer"
                        return redirect(url_for('customer_home'))    #Important: redirect the user to different HTML home page according to the user type!!!
                if user_type == "booking_agent":
                        session['user_type'] = "agent"
                        return redirect(url_for('agent_home'))
                if user_type == "airline_staff":
                        session["user_type"] = "staff"
                        return redirect(url_for('staff_home'))
        else:
                #returns an error message to the html page
                error = 'Invalid login or username or user type'
                return render_template('user_login.html', error=error)    #return to("render" here) the login page and DON'T FORGET TO SEND THE "ERROR" PARAMETER!

########################HOMES#############################
@app.route('/customer_home')
def customer_home():
    cursor_cleaning = conn.cursor()
    query_cleaning = 'TRUNCATE TABLE flight_search_result'    #******NECESSARY TO CLEAN RESULT_VIEW FIRST!!! IMPORTANT!!!
    cursor_cleaning.execute(query_cleaning)

    username = session['username']     #the session's "username" key is already contained in the previous step(redirection from "/loginAuth")!!!
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status FROM ticket join purchases using (ticket_ID) join flight using (airline, flight_ID, departure_time) WHERE email_customer = %s and departure_time > CURRENT_TIMESTAMP()'
    cursor.execute(query, (username))
    data = cursor.fetchall()    
    return render_template('customer_home.html', username=username, user_type = session['user_type'], upcoming_flight = data)

@app.route('/agent_home')
def agent_home():
    cursor_cleaning = conn.cursor()
    query_cleaning = 'TRUNCATE TABLE flight_search_result'    #******NECESSARY TO CLEAN RESULT_VIEW FIRST!!! IMPORTANT!!!
    cursor_cleaning.execute(query_cleaning)


    username = session['username']
    cursor = conn.cursor();
    #query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    #cursor.execute(query, (username))
    #data1 = cursor.fetchall() 
    #for each in data1:
        #print(each['blog_post'])
    #cursor.close()

    #default: show the upcoming flights
    query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status,ticket_ID, email_customer FROM ticket JOIN purchase_for USING (ticket_ID) JOIN flight USING (airline, flight_ID, departure_time) WHERE email_agent = %s AND departure_time > CURRENT_TIMESTAMP()'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    return render_template('agent_home.html', username=username, user_type = session['user_type'], upcoming_flight = data)

@app.route('/staff_home')       #IMPORTNAT PENDING CHECKING AND TESTING!!!
def staff_home():

    username = session['username']
    #query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    #cursor.execute(query, (username))
    #data1 = cursor.fetchall() 
    #for each in data1:
        #print(each['blog_post'])
    #cursor.close()

    #fetch the airline where the staff is working
    cursor = conn.cursor()
    query_pre = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query_pre, (username))
    airline = cursor.fetchall()     #reminder "fetchall()" used here
    airline = airline[0]['airline_name']     #get the result in the correct format
    session['airline'] = airline        #still considering recording "airline" company the staff is working for as a session variable
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT DISTINCT departure_time, arrival_time, airline, flight_ID, departure_airport, arrival_airport, flight_status FROM flight WHERE airline = %s AND departure_time > NOW() AND departure_time <= DATE_ADD(NOW(), INTERVAL 30 DAY)'
    cursor.execute(query, (airline))
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('staff_home.html', username=username, user_type = session['user_type'], airline = airline, upcoming_flight = data)

@app.route('/logout')
def logout():
	session.pop('username')        #***pop out these only two keys for any logged in user
	session.pop('user_type')
	return redirect('/')



@app.route('/flight_purchase_process', methods=['GET', 'POST'])
def flight_purchase_process():
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE flight_to_purchase'     #remember to first clear the "flight_to_purchase" storage table!!!
        cursor_cleaning.execute(query_cleaning)
        cursor = conn.cursor()
        query = 'SELECT * FROM flight_search_result WHERE departure_time > CURRENT_TIMESTAMP()'
        cursor.execute(query)
        data = cursor.fetchall()

        for item in data:
                item["flight_index"] = str(data.index(item))      #***Brilliant: "indexing" each data entry from DATABASE QUERY RESULT again(*in order to match the "flight_index" labelled checkbox form data received previously from "flight_search.html")!!!
        chosen_index = []
        for item in data:
            try: 
                print(request.form[item["flight_index"]])      #important preparation for debugging (by displaying in the terminal)!
                if request.form[item["flight_index"]] == "on":       #***IMPORTANT: IF THE CHECKBOX RECEIVING A "TICK", THEN THE RESULT HERE IS "on"; OTHERWISE, THE RESULT IS "None"(pending??)!!!
                        chosen_index.append(item["flight_index"])
            except:
                pass
     
        if len(chosen_index) == 0:
            error = "No flight was selected. Please re-select!"
            return redirect(url_for('flight_search', error = error))
        else:
            for item in data:
                    if item["flight_index"] in chosen_index:         #IMPORTANT: insert the list of flights the user wants to purchase into the "flight_to_purchase" storage table!!!
                            cursorx = conn.cursor()
                            queryx = 'INSERT INTO flight_to_purchase (airline, flight_ID,departure_airport, arrival_airport,departure_time,arrival_time,price,flight_status) values (%s, %s,%s, %s,%s, %s,%s, %s)'
                            cursorx.execute(queryx,(item["airline"],item["flight_ID"],item["departure_airport"],item["arrival_airport"],item["departure_time"],item["arrival_time"],item["price"],item["flight_status"]))
                            conn.commit()              #*NEVER FORGET TO "COMMIT" AFTER EACH CHANGE TO THE DATABASE!!!
            return redirect(url_for('flight_purchase'))
                

@app.route('/flight_purchase', methods=['GET', 'POST'])
def flight_purchase():
        username = session['username']
        cursork = conn.cursor()
        queryk = 'SELECT * FROM flight_to_purchase'
        cursork.execute(queryk)
        flight_info = cursork.fetchall()

        cursor = conn.cursor()
        query = 'SELECT name,phone_number,passport_number FROM retail_customer WHERE email = %s'
        cursor.execute(query, (username))
        customer_info = cursor.fetchall()
        
        return render_template('flight_purchase.html',username = username, flight_info = flight_info, customer_info = customer_info)

@app.route('/paying_process', methods=['GET', 'POST'])
def paying_process():
        cursor = conn.cursor()
        query = 'SELECT * FROM flight_to_purchase'
        cursor.execute(query)
        data = cursor.fetchall()
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE flight_to_purchase'
        cursor_cleaning.execute(query_cleaning)
        
        username = session['username']

        credit_or_debit = request.form['card_type']
        card_number = request.form['card_number']
        card_holder = request.form['card_holder']
        card_expiration = request.form['card_expiration']
        security_code = request.form['security_code']
        ticket_IDs = []
        for item in data:          #? each flight to purchase has a separate ticket_ID?
                same_ticket_ID = 0
                new_ticket_ID = random_with_N_digits(13)
                while same_ticket_ID:      #???This validation loop's logic needs further consideration and adjustments?
                        cursor = conn.cursor()      #open a new cursor to check whether this ticket_ID has existed!!
                        query = 'SELECT * FROM ticket WHERE ticket_ID = %s'
                        cursor.execute(query,(new_ticket_ID))
                        same_ticket_ID = cursor.fetchall()
                        new_ticket_ID = random_with_N_digits(13)
                ticket_IDs.append(new_ticket_ID)
        
        #*Notice Detail: indexing/searching the elements in the fetched form data(list of dictionaries)!
        for i in range(len(data)):
                cursorx = conn.cursor()         #Insert each ticket's information one by one
                queryx = 'INSERT INTO ticket values (%s,%s,%s,%s,%s) '
                print(ticket_IDs[i], data[i]["price"], data[i]["airline"], data[i]["flight_ID"], data[i]["departure_time"])
                cursorx.execute(queryx, (ticket_IDs[i], data[i]["price"], data[i]["airline"], data[i]["flight_ID"], data[i]["departure_time"]))
                #******IMPORTANT FURTHER REVISION/IMPLEMENTATION ABOVE: "TICKET PRICE" issue(whether "sold_price" is just "base_price" or more)!!!
                conn.commit()
                
        for i in range(len(data)):
                cursorx = conn.cursor()
                queryx = 'INSERT INTO purchases values (%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURRENT_TIME()) '         #***IMPORTANT: learn the two CURRENT DATE/TIME functions: "CURDATE(), CURRENT_TIME()"!!!
                print(username, ticket_IDs[i],credit_or_debit,card_number, card_holder,security_code,card_expiration)
                cursorx.execute(queryx, (username, ticket_IDs[i],credit_or_debit,card_number, card_holder,security_code,card_expiration))
                conn.commit()
        for i in range(len(data)):
                cursorx = conn.cursor()
                queryx = 'INSERT INTO latest_flight_purchased (airline, flight_ID,departure_airport, arrival_airport,departure_time,arrival_time,flight_status, ticket_ID) values (%s, %s,%s, %s,%s, %s,%s, %s)'
                cursorx.execute(queryx,(data[i]["airline"],data[i]["flight_ID"],data[i]["departure_airport"],data[i]["arrival_airport"],data[i]["departure_time"],data[i]["arrival_time"],data[i]["flight_status"], ticket_IDs[i]))
                conn.commit()

        return redirect(url_for('purchase_success'))


@app.route('/purchase_success', methods=['GET', 'POST'])
def purchase_success():
        customer = None      #initialization
        staff = None
        agent = None
        
        if session['user_type'] == "customer":
                customer = "customer"
        if session['user_type'] == "staff":
                staff = "staff"
        if session['user_type'] == "agent":
                agent = "agent"
        cursor_cleaning1 = conn.cursor()
        query_cleaning1 = 'TRUNCATE TABLE flight_search_result'
        cursor_cleaning1.execute(query_cleaning1)
        
        cursor = conn.cursor()
        query = 'SELECT * FROM latest_flight_purchased'
        cursor.execute(query)
        data = cursor.fetchall()
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE latest_flight_purchased'
        cursor_cleaning.execute(query_cleaning)

        return render_template('purchase_success.html', customer = customer, agent = agent, staff = staff, data = data)

@app.route('/allflight', methods=['GET', 'POST'])
def allflight():
        username = session["username"]
        user_type = session["user_type"]
        
        
        customer = None      #initialization
        staff = None
        agent = None
        all_flight_by_date = None
        all_flight_by_source_destination = None
        
        if session['user_type'] == "customer":
                customer = "customer"
        if session['user_type'] == "staff":
                staff = "staff"
        if session['user_type'] == "agent":
                agent = "agent"

        try:            #**THERE'S POSSIBILITY THAT USER DIDN'T ENTER ANYTHING PREVIOUSLY IN THE FORMS(so no request grabbed data)
                try:
                        start_date = request.args['start_date']     #*****Important: Learn an alternative method(continued): DIRECTLY use the additional parameters passed in with the redirected route from "all_flight_filter" here!!!
                except:
                        start_date = None
                try:
                        end_date = request.args['end_date']
                except:
                        end_date = None
                try:
                        source = request.args['source']
                except:
                        source = None
                try:
                        destination = request.args['destination']
                except:
                        destination = None
                print(start_date,end_date)
                #[**]NOTICE: both "start_date" and "end_date" here: "YYYY-MM"(actually "month" range!!!)
                
                #***IMPORTANT: consider all kinds of user input scenarios("start_date" or "end_date" omitted, "source" or "destination" omitted etc.)!!!
                if start_date and end_date:         #both "start_date" and "end_date" search item are not empty
                        start_date_left_boundary = str(start_date)+"-01"      #*****IMPORTANT DETAIL: string representing dates must conform to "YYYY-MM-DD" format which is used in the general case(convenient to conform with MySQL current date/time return norms especially) ALL THE TIME!!!
                        end_date_right_boundary = (str(end_date)).split("-")[0]+"-"+str(int((str(end_date)).split("-")[1])+1)+"-01"
                        cursor = conn.cursor()
                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight using (departure_time, airline, flight_ID) WHERE email_customer = %s and DATE(departure_time) > %s and DATE(departure_time) < %s'
                        cursor.execute(query,(username,start_date_left_boundary,end_date_right_boundary))    #***DETAIL NOTICE(?pending) ABOVE: "strictly" bigger than and smaller than or not(including start and end)??
                        all_flight_by_date = cursor.fetchall()
                else:        #"start_date" or "end_date" not complete: not using Date Range Searching, but Location-based Searching instead!!
                        cursor = conn.cursor()
                        if source and not destination:     #contains only source location
                                if len(source) == 3:       #[**]e.g.: "PVG"
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_airport = %s'
                                        cursor.execute(query,(username,source))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:             #[**]city name
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_city = %s'
                                        cursor.execute(query,(username,source))
                                        all_flight_by_source_destination = cursor.fetchall()
                        if destination and not source:     #contains only destination location
                                if len(destination) == 3:
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and arrival_airport = %s'
                                        cursor.execute(query,(username,destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and arrival_city = %s'
                                        cursor.execute(query,(username,destination))
                                        all_flight_by_source_destination = cursor.fetchall()

                        if destination and source:        #contains both source location and destination location
                                if len(destination) == 3:
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_airport = %s and arrival_airport = %s'
                                        cursor.execute(query,(username, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_city = %s and arrival_city = %s'
                                        cursor.execute(query,(username, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                        
                                
                        
        except:
                pass
        cursor = conn.cursor()
        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_time > CURRENT_TIMESTAMP()'
        cursor.execute(query,(username))
        upcoming_flight = cursor.fetchall()    #all flights to happen after the current timestamp!

        cursor = conn.cursor()
        query = 'SELECT * FROM ticket join purchases using (ticket_ID) join flight using (departure_time, airline, flight_ID) WHERE email_customer = %s and departure_time < CURRENT_TIMESTAMP()'
        cursor.execute(query,(username))
        historical_flight = cursor.fetchall()      #all flights to happend before the current timestamp!
        return render_template('allflight.html',all_flight_by_date= all_flight_by_date, all_flight_by_source_destination=all_flight_by_source_destination,customer = customer, staff = staff, agent = agent, upcoming_flight = upcoming_flight, historical_flight = historical_flight, username = username, user_type = user_type)

#"/allflight_filter" route usage is shared by three types of users!!!
@app.route('/allflight_filter', methods=['GET', 'POST'])
def allflight_filter():
        user_type = session["user_type"]
        start_date = request.form['start_date']      #grab data from user search form in "allfight.html"
        end_date = request.form['end_date']
        source = request.form['source']
        destination = request.form['destination']
        if str(user_type) == "customer":
            return redirect(url_for('allflight',start_date=start_date,end_date=end_date,source=source,destination=destination))
        #*****Important above: Learn an alternative method--pass the grabbed data as additional parameters into the redirected route DIRECTLY!!! 
        if str(user_type) == "agent":
            return redirect(url_for('agent_all_flight', start_date=start_date, end_date=end_date, source=source, destination=destination))
        if str(user_type) == "staff":
            return redirect(url_for('staff_all_flight', start_date=start_date, end_date=end_date, source=source, destination=destination))

        
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
        username = session["username"]
        user_type = session["user_type"]
        message = None
        try:        #*in this case, the user entered the complete search date range(starting, ending) to specify
                start_date = request.args['start_date']     #still, only month search is allowed here
                end_date = request.args['end_date']
                print("start_date request args:", start_date)
                start_date_left_boundary = str(start_date)+"-01"
                end_date_right_boundary = (str(end_date)).split("-")[0]+"-"+str(int((str(end_date)).split("-")[1])+1)+"-01"   #ending date: first day of the next month of the user input search month
                by_month_data = [item for item in [request.args['by_month_data']]]     #[***print result exploration]"by_month_data": ["{'month': 201904, 'expense': Decimal('11002')}"]
                print(by_month_data)
                print(len(by_month_data))     #"how many records"
                monthlist = []        #"monthlist": list of months from starting to ending
                valuelist = []
                end_month = int(str(end_date).split("-")[1])
                end_year = int(str(end_date).split("-")[0])
                #for item in total_data:
                        #item = eval(item)
                #print(total_data, type(total_data))
                if len(str(end_month)) == 1:       #single-digit month(like: '9')
                        end_month_string = str(end_year)+"0" + str(end_month)    #(like: "201809")
                else:            #double-digit month(like: '10')
                        end_month_string = str(end_year) +str(end_month)
                                
                #(similar handling to "end_month_string" above)
                start_month = int(str(start_date).split("-")[1])
                start_year = int(str(start_date).split("-")[0])
                if len(str(start_month)) == 1:
                        start_month_string = str(start_year)+"0"+ str(start_month)
                else:
                        start_month_string = str(start_year) +str(start_month)
                this_month = end_month      #initialization of "this_month" to be the ending month the user has input
                this_year = end_year
                #"end_month", "end_year" are integers
             
                while True:     #continue looping until reach the "break" statement in the body
                        if len(str(this_month)) == 1:         #single-digit month(like: '9')
                                this_month_string = "0" + str(this_month)
                        else:
                                this_month_string = str(this_month)
                        monthdata = str(this_year)+ this_month_string        #*e.g.:"201903"
                        monthlist.append(monthdata)
                        for item in by_month_data:
                                item = eval(item)       #*****"eval" function evaluate the string passed in as a Python expression(the passed in "item": a string here)
                                #*****and after the above line: "item" becomes the dictionary(originally contained in the string passed in)?
                                #[kind of understood]IMPORTANT: ???Logic question below: only use "append"(and add all "0"s in the end) would make the order inconsistent?
                                if str(item["month"]) == monthdata:       #*"monthdata": "user month range requested for search"(continuous); "str(item["month"])": result of actual query from database(might have "0" expense in certain month)
                                        valuelist.append(int(item["expense"]))
                        if len(valuelist) < len(monthlist):      #for every month backward, if the query result does not provide value, append "0"(*check for every step(month)!)
                                valuelist.append(int(0))
                        if this_year == start_year and this_month == start_month:    #check whether already finished the job(reached the end)
                                break
                        this_year, this_month = last_month(this_year, this_month)      #IMPORTANT: see the self-defined function at the top of this file!!!!!
                valuelist = list(reversed(valuelist))
                monthlist = list(reversed(monthlist))
                #print(valuelist,monthlist)
                print("monthlist:", monthlist)
                print("valuelist:", valuelist)
                cursorx = conn.cursor()
                #***"total_data": total sum of all dates within the search range(starting from "start_date_left_boundary" and ending at "end_date_right_boundary")
                total_query = "SELECT sum(sold_price) as expense FROM ticket join purchases using (ticket_ID) WHERE email_customer = %s and date_purchase <= %s and date_purchase >= %s"
                cursorx.execute(total_query,(username, end_date_right_boundary, start_date_left_boundary))
                total_data = cursorx.fetchall()
                staff = None
                customer = None
                agent = None
                if session['user_type'] == "customer":
                        customer = "customer"
                if session['user_type'] == "staff":
                        staff = "staff"
                if session['user_type'] == "agent":
                        agent = "agent"

                #? "by_month_data" passed below actually not used in the html webpage?
                return render_template('track_spending.html', customer = customer, staff = staff, agent = agent, monthlist =json.dumps(monthlist), valuelist = json.dumps(valuelist),user_type = user_type, username = username, start_date = start_month_string, end_date = end_month_string, by_month_data = by_month_data, total_data = total_data)
        except:       #in this case, the user didn't enter the complete search date range(e.g.: no "ending date")
                try:        #only "start_date" search is input but without "end_date"
                        start_date = request.args['start_date']
                        message = "Invalid input or no expense occurred in the entered date range."
                        print(message)
                except:     #no search date range is input
                        pass
                cursor = conn.cursor()       #so in this case, default will play the stats for past 6 months and past year
                recent_6_month_query = "SELECT EXTRACT(YEAR_MONTH From date_purchase) as month, sum(sold_price) as expense FROM ticket join purchases using (ticket_ID) WHERE email_customer = %s and date_purchase <= CURDATE() and date_purchase >= Date_SUB(CURDATE(),interval 6 month)  GROUP BY EXTRACT(YEAR_MONTH From date_purchase) "
                cursor.execute(recent_6_month_query,(username))
                recent_6_month_data = cursor.fetchall()
                recent_6_month_data = [item for item in recent_6_month_data]      #5.13 Susie try
                monthlist = []
                valuelist = []
                this_month = int(datetime.now().month)    #get the current datetime's "month" value(and similar below)
                this_year = int(datetime.now().year)
                
                for m in range(0, 6):     #can be sure there's 6 month
                        if len(str(this_month)) == 1:
                                this_month_string = "0" + str(this_month)
                        else:
                                this_month_string = str(this_month)
                        monthdata = str(this_year)+this_month_string
                        monthlist.append(monthdata)
                        for item in recent_6_month_data:
                                if str(item["month"]) == monthdata:
                                        valuelist.append(int(item["expense"]))
                        if len(valuelist) < len(monthlist):
                                valuelist.append(int(0))
                        #??? Why do we need to fix the "recent_6_month_data" here?(does the actual graph-making need this, or just "valuelist" & "monthlist" are enough?)
                        for i in range(len(monthlist)):
                                monthinlist = False
                                for item in recent_6_month_data:
                                        if str(item["month"]) == monthdata:
                                                monthinlist = True
                                if monthinlist == False:
                                        recent_6_month_data.append({"month":monthdata, "expense": 0})
                                
                        this_year, this_month = last_month(this_year, this_month)
                valuelist = list(reversed(valuelist))
                monthlist = list(reversed(monthlist))
                #print(valuelist,monthlist,recent_6_month_data)
                print("monthlist:", monthlist)
                print("valuelist:", valuelist)
                        
                cursorx = conn.cursor()
                recent_1_year_query = "SELECT sum(sold_price) as expense FROM ticket join purchases using (ticket_ID) WHERE email_customer = %s and date_purchase <= CURDATE() and date_purchase >= Date_SUB(CURDATE(),interval 12 month)"
                cursorx.execute(recent_1_year_query,(username))
                recent_12_month_data = cursorx.fetchall()
                staff = None
                customer = None
                agent = None
                if session['user_type'] == "customer":
                        customer = "customer"
                if session['user_type'] == "staff":
                        staff = "staff"
                if session['user_type'] == "agent":
                        agent = "agent"

                
                return render_template('track_spending.html',customer = customer, staff = staff, agent = agent, message = message, monthlist =json.dumps(monthlist), valuelist = json.dumps(valuelist), username = username, user_type = user_type,recent_6_month_data = recent_6_month_data, recent_12_month_data = recent_12_month_data)


@app.route('/track_spending_process', methods=['GET', 'POST'])
def track_spending_process():
        username = session["username"]
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        try:
            start_date_left_boundary = str(start_date)+"-01"
            end_date_right_boundary = (str(end_date)).split("-")[0]+"-"+str(int((str(end_date)).split("-")[1])+1)+"-01"
        except:
            start_date_left_boundary = None
            end_date_right_boundary = None
        by_month_data = None        #initialization before querying the database
        total_data = None         #??not used here??
        cursor = conn.cursor()
        by_month_query = 'SELECT EXTRACT(YEAR_MONTH From date_purchase) as month, sum(sold_price) as expense FROM ticket join purchases using (ticket_ID) WHERE email_customer = %s and date_purchase <= %s and date_purchase >= %s  GROUP BY EXTRACT(YEAR_MONTH From date_purchase)'
        cursor.execute(by_month_query,(username, end_date_right_boundary, start_date_left_boundary))
        by_month_data = cursor.fetchall()     #**"by_month_data": month range and the corresponding total sold_price for each month results 
        print("by_month_data: ", by_month_data)
        return redirect(url_for('track_spending', start_date = start_date, end_date = end_date, by_month_data = by_month_data))


#--------------------more by Susie-------------------
#-----###Booking agent: -----

@app.route('/agent_flight_purchase_process', methods=['GET','POST'])
def agent_flight_purchase_process():
        try:
            customer_represented = request.form['for_customer']       #f***********firstly, from "flight_search.html": need to initially record and keep the flight choice information etc.
            cursor_cleaning = conn.cursor()
            query_cleaning = 'TRUNCATE TABLE flight_to_purchase'     #remember to first clear the "flight_to_purchase" storage table!!!
            cursor_cleaning.execute(query_cleaning)

            cursor_cleaning2 = conn.cursor()
            query_cleaning2 = 'TRUNCATE TABLE customer_to_purchase'     #remember to first clear the "flight_to_purchase" storage table!!!
            cursor_cleaning2.execute(query_cleaning2)

            cursor = conn.cursor()
            query = 'SELECT * FROM flight_search_result WHERE departure_time > CURRENT_TIMESTAMP()'
            cursor.execute(query)
            data = cursor.fetchall()

            
            for item in data:
                    item["flight_index"] = str(data.index(item))      #***Brilliant: "indexing" each data entry from DATABASE QUERY RESULT again(*in order to match the "flight_index" labelled checkbox form data received previously from "flight_search.html")!!!
            chosen_index = []
            print(customer_represented)
            for item in data:
                try:
                    print(request.form[item["flight_index"]])      #important preparation for debugging (by displaying in the terminal)!
                    if request.form[item["flight_index"]] == "on":       #***IMPORTANT: IF THE CHECKBOX RECEIVING A "TICK", THEN THE RESULT HERE IS "on"; OTHERWISE, THE RESULT IS "None"(pending??)!!!
                            chosen_index.append(item["flight_index"])
                except:
                    pass
            print(customer_represented)
            if len(chosen_index) == 0:
                error = "No flight was selected. Please re-select!"
                return redirect(url_for('flight_search', error = error))
            else:

                for item in data:
                        if item["flight_index"] in chosen_index:         #IMPORTANT: insert the list of flights the user wants to purchase into the "flight_to_purchase" storage table!!!
                                cursorx = conn.cursor()
                                queryx = 'INSERT INTO flight_to_purchase (airline, flight_ID,departure_airport, arrival_airport,departure_time,arrival_time,price,flight_status) values (%s, %s,%s, %s,%s, %s,%s, %s)'
                                cursorx.execute(queryx,(item["airline"],item["flight_ID"],item["departure_airport"],item["arrival_airport"],item["departure_time"],item["arrival_time"],item["price"],item["flight_status"]))
                                conn.commit()              #*NEVER FORGET TO "COMMIT" AFTER EACH CHANGE TO THE DATABASE!!!                                     
        except:
            customer_represented = request.form['customer_represented']        #**************subsequently, from "agent_flight_purchase.html"
        print(customer_represented)
        #validate whether the customer exists in the database
        cursor = conn.cursor()
        query_customer = "SELECT * FROM retail_customer WHERE email = %s"
        cursor.execute(query_customer, (customer_represented))
        customer = cursor.fetchone()
        cursor.close()
        customer_error = None
        if (not customer):         #this customer doesn't exist
            customer_error = "This customer does not exist. Try again."
            return redirect(url_for("agent_flight_purchase", customer_error = customer_error))        #this case pass the error message to next rendering template
        else:
            cursor = conn.cursor()
            query = "INSERT INTO customer_to_purchase values (%s)"
            cursor.execute(query, (customer_represented))
            conn.commit()
            print(customer_represented)
            return redirect(url_for('agent_flight_purchase', customer=customer_represented))          #this case demonstrates the user is valid

@app.route('/agent_flight_purchase', methods=['GET','POST'])
def agent_flight_purchase():
        username = session['username']
        customer_error = None      #(default no error, unless error is passed in)
               
        try:         #there is customer error
            customer_error = request.args["customer_error"]
            return render_template('agent_flight_purchase.html',username = username, customer_error = customer_error)
        except:      #there is no customer error, "customer" parameter is passed in
    
            cursor = conn.cursor()
            query_customer = "SELECT email FROM customer_to_purchase"
            cursor.execute(query_customer)
            customer_represented = cursor.fetchone()["email"]
            cursor.close()
            print("yes",customer_represented)
            #flight info display
            cursork = conn.cursor()
            queryk = 'SELECT * FROM flight_to_purchase'
            cursork.execute(queryk)
            flight_info = cursork.fetchall()
            #customer represented info
            cursor = conn.cursor()
            query = 'SELECT name,phone_number,passport_number FROM retail_customer WHERE email = %s'
            cursor.execute(query, (customer_represented))
            customer_info_rep = cursor.fetchall()
            
            return render_template('agent_flight_purchase.html',username = username, customer_represented = customer_represented, flight_info = flight_info, customer_info_rep = customer_info_rep)

@app.route('/agent_paying_process', methods=['GET','POST'])
def agent_paying_process():
        cursor = conn.cursor()
        query = 'SELECT * FROM flight_to_purchase'
        cursor.execute(query)
        data = cursor.fetchall()
        
        cursor_cleaning = conn.cursor()
        query_cleaning = 'TRUNCATE TABLE flight_to_purchase'
        cursor_cleaning.execute(query_cleaning)

        cursor = conn.cursor()
        query_customer = "SELECT email FROM customer_to_purchase"
        cursor.execute(query_customer)
        client_rep = cursor.fetchone()["email"]
        cursor.close()

        cursor_cleaning2 = conn.cursor()
        query_cleaning2 = 'TRUNCATE TABLE customer_to_purchase'
        cursor_cleaning2.execute(query_cleaning2)


        
        username = session['username']

        credit_or_debit = request.form['card_type']
        card_number = request.form['card_number']
        card_holder = request.form['card_holder']
        card_expiration = request.form['card_expiration']
        security_code = request.form['security_code']

        
        ticket_IDs = []
        for item in data:          #? each flight to purchase has a separate ticket_ID?
                same_ticket_ID = 0
                new_ticket_ID = random_with_N_digits(13)
                while same_ticket_ID:      #???This validation loop's logic needs further consideration and adjustments?
                        cursor = conn.cursor()      #open a new cursor to check whether this ticket_ID has existed!!
                        query = 'SELECT * FROM ticket WHERE ticket_ID = %s'
                        cursor.execute(query,(new_ticket_ID))
                        same_ticket_ID = cursor.fetchall()
                        new_ticket_ID = random_with_N_digits(13)
                ticket_IDs.append(new_ticket_ID)
        
        #*Notice Detail: indexing/searching the elements in the fetched form data(list of dictionaries)!
        for i in range(len(data)):
                cursorx = conn.cursor()         #Insert each ticket's information one by one
                queryx = 'INSERT INTO ticket values (%s,%s,%s,%s,%s) '
                print(ticket_IDs[i], data[i]["price"], data[i]["airline"], data[i]["flight_ID"], data[i]["departure_time"])
                cursorx.execute(queryx, (ticket_IDs[i], data[i]["price"], data[i]["airline"], data[i]["flight_ID"], data[i]["departure_time"]))
                #******IMPORTANT FURTHER REVISION/IMPLEMENTATION ABOVE: "TICKET PRICE" issue(whether "sold_price" is just "base_price" or more)!!!
                conn.commit()
                
        #IMPORTANT: insert the "purchase" info for the retail customer represented               
        for i in range(len(data)):
                cursorx = conn.cursor()
                queryx = 'INSERT INTO purchases values (%s,%s,%s,%s,%s,%s,%s,CURDATE(),CURRENT_TIME()) '         #***IMPORTANT: learn the two CURRENT DATE/TIME functions: "CURDATE(), CURRENT_TIME()"!!!
                print(client_rep, ticket_IDs[i],credit_or_debit,card_number, card_holder,security_code,card_expiration)
                cursorx.execute(queryx, (client_rep, ticket_IDs[i],credit_or_debit,card_number, card_holder,security_code,card_expiration))
                conn.commit()

        #IMPORTANT: insert the info to "purchase_for" table!!!
        for i in range(len(data)):
                cursorx = conn.cursor()
                queryx = 'INSERT INTO purchase_for VALUES(%s, %s, %s)'
                cursorx.execute(queryx, (ticket_IDs[i], client_rep, username))
                conn.commit()

                
        for i in range(len(data)):
                cursorx = conn.cursor()
                queryx = 'INSERT INTO latest_flight_purchased (airline, flight_ID,departure_airport, arrival_airport,departure_time,arrival_time,flight_status, ticket_ID) values (%s, %s,%s, %s,%s, %s,%s, %s)'
                cursorx.execute(queryx,(data[i]["airline"],data[i]["flight_ID"],data[i]["departure_airport"],data[i]["arrival_airport"],data[i]["departure_time"],data[i]["arrival_time"],data[i]["flight_status"], ticket_IDs[i]))
                conn.commit()

        return redirect(url_for('purchase_success'))

@app.route('/agent_all_flight', methods=['GET','POST'])
def agent_all_flight():
        username = session["username"]
        user_type = session["user_type"]
        
        
        customer = None      #initialization
        staff = None
        agent = None
        all_flight_by_date = None
        all_flight_by_source_destination = None
        
        if session['user_type'] == "customer":
                customer = "customer"
        if session['user_type'] == "staff":
                staff = "staff"
        if session['user_type'] == "agent":
                agent = "agent"

        try:            #**THERE'S POSSIBILITY THAT USER DIDN'T ENTER ANYTHING PREVIOUSLY IN THE FORMS(so no request grabbed data)
                try:
                        start_date = request.args['start_date']     #*****Important: Learn an alternative method(continued): DIRECTLY use the additional parameters passed in with the redirected route from "all_flight_filter" here!!!
                except:
                        start_date = None
                try:
                        end_date = request.args['end_date']
                except:
                        end_date = None
                try:
                        source = request.args['source']
                except:
                        source = None
                try:
                        destination = request.args['destination']
                except:
                        destination = None
                print(start_date,end_date)
                #[**]NOTICE: both "start_date" and "end_date" here: "YYYY-MM"(actually "month" range!!!)
                
                #***IMPORTANT: consider all kinds of user input scenarios("start_date" or "end_date" omitted, "source" or "destination" omitted etc.)!!!
                if start_date and end_date:         #both "start_date" and "end_date" search item are not empty
                        start_date_left_boundary = str(start_date)+"-01"      #*****IMPORTANT DETAIL: string representing dates must conform to "YYYY-MM-DD" format which is used in the general case(convenient to conform with MySQL current date/time return norms especially) ALL THE TIME!!!
                        end_date_right_boundary = (str(end_date)).split("-")[0]+"-"+str(int((str(end_date)).split("-")[1])+1)+"-01"
                        cursor = conn.cursor()
                        #IMPORTANT: agent using "purchase_for" table here!!!
                        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight using (departure_time, airline, flight_ID) WHERE email_agent = %s and DATE(departure_time) > %s and DATE(departure_time) < %s'
                        cursor.execute(query,(username,start_date_left_boundary,end_date_right_boundary))    #***DETAIL NOTICE(?pending) ABOVE: "strictly" bigger than and smaller than or not(including start and end)??
                        all_flight_by_date = cursor.fetchall()
                else:        #"start_date" or "end_date" not complete: not using Date Range Searching, but Location-based Searching instead!!
                        cursor = conn.cursor()
                        if source and not destination:     #contains only source location
                                if len(source) == 3:       #[**]e.g.: "PVG"
                                        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and departure_airport = %s'
                                        cursor.execute(query,(username,source))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:             #[**]city name
                                        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and departure_city = %s'
                                        cursor.execute(query,(username,source))
                                        all_flight_by_source_destination = cursor.fetchall()
                        if destination and not source:     #contains only destination location
                                if len(destination) == 3:
                                        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and arrival_airport = %s'
                                        cursor.execute(query,(username,destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT DISTINCT  departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and arrival_city = %s'
                                        cursor.execute(query,(username,destination))
                                        all_flight_by_source_destination = cursor.fetchall()

                        if destination and source:        #contains both source location and destination location
                                if len(destination) == 3:
                                        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and departure_airport = %s and arrival_airport = %s'
                                        cursor.execute(query,(username, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT DISTINCT  departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket join purchase_for using (ticket_ID) join flight_with_city using (departure_time, airline, flight_ID) WHERE email_agent = %s and departure_city = %s and arrival_city = %s'
                                        cursor.execute(query,(username, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()                       
        except:
                pass
        cursor = conn.cursor()
        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status, ticket_ID,email_customer FROM ticket JOIN purchase_for USING (ticket_ID) JOIN flight USING (airline, flight_ID, departure_time) WHERE email_agent = %s AND departure_time > CURRENT_TIMESTAMP()'
        cursor.execute(query,(username))
        upcoming_flight = cursor.fetchall()    #all flights to happen after the current timestamp!

        cursor = conn.cursor()
        query = 'SELECT DISTINCT departure_time, arrival_time, airline, departure_airport, arrival_airport, flight_ID, flight_status,ticket_ID,email_customer FROM ticket JOIN purchase_for USING (ticket_ID) JOIN flight USING (airline, flight_ID, departure_time) WHERE email_agent = %s AND departure_time < CURRENT_TIMESTAMP()'
        cursor.execute(query,(username))
        historical_flight = cursor.fetchall()      #all flights to happend before the current timestamp!
        return render_template('allflight.html',all_flight_by_date= all_flight_by_date, all_flight_by_source_destination=all_flight_by_source_destination,customer = customer, staff = staff, agent = agent, upcoming_flight = upcoming_flight, historical_flight = historical_flight, username = username, user_type = user_type)

@app.route('/allcommission_filter', methods=['GET', 'POST'])
def allcommission_filter():
        #user_type = session["user_type"]
        start_date = request.form['start_date']      #grab data from user search form in "view_commission.html"
        end_date = request.form['end_date']
        return redirect(url_for('view_my_commission', start_date=start_date, end_date=end_date))

@app.route('/view_my_commission', methods=['GET','POST'])
def view_my_commission():
        username = session["username"]
        user_type = session["user_type"]

        total_commission_amount_past30 = None
        total_ticket_number_past30 = None      #[not used]alternative "0"
        average_commission_past30 = None

        total_commission_by_date = None
        total_ticket_number_by_date = None      #[not used]alternative "0"

        #to see if the user has entered date range to search
        try:
            start_date = request.args['start_date']
        except:
            start_date = None

        try:
            end_date = request.args['end_date']
        except:
            end_date = None

        if start_date and end_date:      #[p]the logic here: only when both "start_date" and "end_date" have been entered in the form, the search is considered valid
            cursor = conn.cursor()
            query = "SELECT SUM(sold_price * 0.1) AS total_commission FROM purchase_for JOIN ticket USING (ticket_ID) JOIN purchases USING (ticket_ID) WHERE email_agent = %s AND date_purchase <= %s AND date_purchase >= %s"
            cursor.execute(query, (username, end_date, start_date))
            total_commission_by_date = cursor.fetchone()    #******RETURN A SINGLE DICTIONARY(with "total_commission" as the key)!!!
            if total_commission_by_date['total_commission'] == None:       #***indicating the query result from database is NULL
                total_commission_by_date['total_commission'] = 0    #a small trick for nicer result display
            #print("total_commission_by_date: ", total_commission_by_date)    #debug
            #print("type: ", type(total_commission_by_date))     #debug
            cursor.close()

            cursor1 = conn.cursor()
            query1 = "SELECT COUNT(ticket_ID) AS total_ticket FROM purchase_for JOIN ticket USING (ticket_ID) JOIN purchases USING (ticket_ID) WHERE email_agent = %s AND date_purchase <= %s AND date_purchase >= %s"
            cursor1.execute(query1, (username, end_date, start_date))
            total_ticket_number_by_date = cursor1.fetchone()
            cursor1.close()

        #*****IMPORTANT DETAIL NOTICE: "SUM" would result NULL(SQL)/None(Python) for "fetchone()" if no result!!!
        cursor = conn.cursor()
        query_a = "SELECT SUM(sold_price * 0.1) AS total_commission FROM purchase_for JOIN ticket USING (ticket_ID) JOIN purchases USING (ticket_ID) WHERE email_agent = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), interval 1 month)"
        cursor.execute(query_a, (username))
        total_commission_amount_past30 = cursor.fetchone()
        if total_commission_amount_past30['total_commission'] == None:
            total_commission_amount_past30['total_commission'] = 0
        print("total_commission_amount_past30:", total_commission_amount_past30)     #debug
        cursor.close()

        #*****IMPORTANT DETAIL NOTICE: "COUNT" would result 0(SQL) for "fetchone()" if no result!!!
        cursor = conn.cursor()
        query_b = "SELECT COUNT(ticket_ID) AS total_ticket FROM purchase_for JOIN ticket USING (ticket_ID) JOIN purchases USING (ticket_ID) WHERE email_agent = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), interval 1 month)"
        cursor.execute(query_b, (username))
        total_ticket_number_past30 = cursor.fetchone()
        cursor.close()

        cursor = conn.cursor()
        query_c = "SELECT SUM(sold_price*0.1)/COUNT(ticket_ID) AS average_commission FROM purchase_for JOIN ticket USING (ticket_ID) JOIN purchases USING (ticket_ID) WHERE email_agent = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), interval 1 month)"
        cursor.execute(query_c, (username))
        average_commission_past30 = cursor.fetchone()
        if average_commission_past30['average_commission'] == None:
            average_commission_past30['average_commission'] = 0
        cursor.close()

        return render_template("view_commission.html", username = username, user_type = user_type, start_date = start_date, end_date = end_date, total_commission_amount_past30 = total_commission_amount_past30, total_ticket_number_past30 = total_ticket_number_past30, average_commission_past30 = average_commission_past30, total_commission_by_date = total_commission_by_date, total_ticket_number_by_date = total_ticket_number_by_date)

        
@app.route('/view_top_customers', methods=['GET','POST'])
def view_top_customers():
        username = session['username']
        user_type = session['user_type']
        
        #top 5 clients based on ticket sales for the agent during the past 6 months
        cursor = conn.cursor()
        query = 'SELECT email, name, phone_number, birth_date, passport_country, city, COUNT(DISTINCT ticket_ID) AS ticket_number FROM purchases JOIN purchase_for USING (ticket_ID, email_customer) JOIN retail_customer ON (email_customer = email) WHERE email_agent = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) GROUP BY email ORDER BY ticket_number DESC LIMIT 5'
        cursor.execute(query, (username))
        top5_client_ticket_sales_past6months = cursor.fetchall()
        cursor.close()

        #top 5 clients based on commission for the agent during the past year
        cursor = conn.cursor()
        query = 'SELECT email, name, phone_number, birth_date, passport_country, city, SUM(sold_price*0.1) AS commission FROM purchases JOIN purchase_for USING (ticket_ID, email_customer) JOIN ticket USING (ticket_ID) JOIN retail_customer ON (email_customer = email) WHERE email_agent = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY email ORDER BY commission DESC LIMIT 5'
        cursor.execute(query, (username))
        top5_client_commission_pastyear = cursor.fetchall()
        cursor.close()

        peoplelist1 = []       #initialization
        ticketlist = []
        peoplelist2 = []
        commissionlist = []

        #####IMPORTANT: DRAWING TWO GRAPHS!!!!!
        #First graph: top 5 clients based on ticket sales during the past 6 months
        if top5_client_ticket_sales_past6months:
            #peoplelist1 = []        #*prepare for x-axis data
            #ticketlist = []        #*prepare for y-axis data
            for line in top5_client_ticket_sales_past6months:
                peoplelist1.append(line['email'])
                ticketlist.append(int(line['ticket_number']))
            print("peoplelist1:", peoplelist1)     #ready for debugging
            print("ticketlist:", ticketlist)       #ready for debugging

        if top5_client_commission_pastyear:
            #peoplelist2 = []
            #commissionlist = []
            for line in top5_client_commission_pastyear:
                peoplelist2.append(line['email'])
                commissionlist.append(int(line['commission']))
            print("peoplelist2:", peoplelist2)         #ready for debugging
            print("commissionlist:", commissionlist)       #ready for debugging


        return render_template("view_top_customers.html", username=username, user_type=user_type, top5_client_ticket_sales_past6months=top5_client_ticket_sales_past6months, top5_client_commission_pastyear=top5_client_commission_pastyear, peoplelist1=json.dumps(peoplelist1), ticketlist=json.dumps(ticketlist), peoplelist2=json.dumps(peoplelist2), commissionlist=json.dumps(commissionlist))
    


#-----###Airline Staff: -----

@app.route('/view_flight_all_customer', methods=['GET', 'POST'])
def grab_flight_search():
    flightID = request.form['flightID_for_allcustomer']      #***Question: what if the form data is empty(user didn't enter): return "None"?
    departure_time = request.form['departure_time_for_allcustomer']
    return redirect(url_for('staff_all_flight', flightID_for_search = flightID, departure_time_for_search = departure_time))


### "/staff_all_flight" route here receives args from TWO "form date grab" routes!!
@app.route('/staff_all_flight', methods=['GET', 'POST'])
def staff_all_flight():
        username = session["username"]
        user_type = session["user_type"]
        airline = session["airline"]      #*fetch the session recorded "airline"
 
        all_flight_by_date = None
        all_previous_flight_by_date = None
        all_future_flight_by_date = None
        all_flight_by_source_destination = None

        flight_all_customer = None        #default result "None"
        
        #staff search for flights based on date/place
        
        try:            #**THERE'S POSSIBILITY THAT USER DIDN'T ENTER ANYTHING PREVIOUSLY IN THE FORMS(so no request grabbed data)
                try:
                        start_date = request.args['start_date']     #*****Important: Learn an alternative method(continued): DIRECTLY use the additional parameters passed in with the redirected route from "all_flight_filter" here!!!
                except:
                        start_date = None
                try:
                        end_date = request.args['end_date']
                except:
                        end_date = None
                try:
                        source = request.args['source']
                except:
                        source = None
                try:
                        destination = request.args['destination']
                except:
                        destination = None
                print(start_date,end_date)
                #[**]NOTICE: both "start_date" and "end_date" here: "YYYY-MM"(actually "month" range!!!)
                
                #***IMPORTANT: consider all kinds of user input scenarios("start_date" or "end_date" omitted, "source" or "destination" omitted etc.)!!!
                if start_date and end_date:         #both "start_date" and "end_date" search item are not empty
                        start_date_left_boundary = str(start_date)+"-01"      #*****IMPORTANT DETAIL: string representing dates must conform to "YYYY-MM-DD" format which is used in the general case(convenient to conform with MySQL current date/time return norms especially) ALL THE TIME!!!
                        end_date_right_boundary = (str(end_date)).split("-")[0]+"-"+str(int((str(end_date)).split("-")[1])+1)+"-01"
                        cursor = conn.cursor()
                        query = 'SELECT * FROM flight WHERE airline = %s and DATE(departure_time) >= %s and DATE(departure_time) < %s'      #SMALL REVISION: date "LEFT BOUNDARY" "larger than or EQUAL TO" (instead of strictly largher than)!
                        cursor.execute(query,(airline,start_date_left_boundary,end_date_right_boundary))    #***DETAIL NOTICE(?pending) ABOVE: "strictly" bigger than and smaller than or not(including start and end)??
                        all_flight_by_date = cursor.fetchall()
                        cursor.close()
                        
                        cursor = conn.cursor()
                        query_past = 'SELECT * FROM flight WHERE airline = %s and DATE(departure_time) < %s'
                        cursor.execute(query_past, (airline, start_date_left_boundary))
                        all_previous_flight_by_date = cursor.fetchall()
                        print("all_previous_flight_by_date:", all_previous_flight_by_date)
                        cursor.close()
                        
                        cursor = conn.cursor()
                        query_future = 'SELECT * FROM flight WHERE airline = %s and DATE(departure_time) >= %s'
                        cursor.execute(query_future, (airline, end_date_right_boundary))
                        all_future_flight_by_date = cursor.fetchall()
                        print("all_future_flight_by_date:", all_future_flight_by_date)
                        cursor.close()
                        
                else:        #"start_date" or "end_date" not complete: not using Date Range Searching, but Location-based Searching instead!!
                        cursor = conn.cursor()
                        if source and not destination:     #contains only source location
                                if len(source) == 3:       #[**]e.g.: "PVG"
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and departure_airport = %s'
                                        cursor.execute(query, (airline, source))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:             #[**]city name
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and departure_city = %s'
                                        cursor.execute(query, (airline, source))
                                        all_flight_by_source_destination = cursor.fetchall()
                        if destination and not source:     #contains only destination location
                                if len(destination) == 3:
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and arrival_airport = %s'
                                        cursor.execute(query, (airline, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and arrival_city = %s'
                                        cursor.execute(query,(airline, destination))
                                        all_flight_by_source_destination = cursor.fetchall()

                        if destination and source:        #contains both source location and destination location
                                if len(destination) == 3:
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and departure_airport = %s and arrival_airport = %s'
                                        cursor.execute(query,(airline, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                else:
                                        query = 'SELECT * FROM flight_with_city WHERE airline = %s and departure_city = %s and arrival_city = %s'
                                        cursor.execute(query,(airline, source, destination))
                                        all_flight_by_source_destination = cursor.fetchall()
                                        
                                
                        
        except:
                pass
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline = %s AND departure_time >= NOW() AND departure_time <= DATE_ADD(NOW(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline))
        upcoming_flight = cursor.fetchall()    #all flights to happen after the current timestamp in 30 days!
        cursor.close()

        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline = %s AND departure_time <= NOW() AND departure_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline))
        historical_flight = cursor.fetchall()      #all (historical) flights to happen before the current timestamp in 30 days!
        cursor.close()

        #view all customers for a particular flight
        #receive variables "flightID_for_search" and "departure_time_for_search" from "/view_flight_all_customer" route!
        try:
            flightID_for_search = request.args['flightID_for_search']
        except:
            flightID_for_search = None
        try:
            departure_time_for_search = request.args['departure_time_for_search']
        except:
            departure_time_for_search = None

        if flightID_for_search and departure_time_for_search:        #***Important: only when user entered both "flightID" and "departure_time" for search(both are NOT "None"), the search input is valid; otherwise, NO RESULT
            cursor = conn.cursor()
            query = 'SELECT email_customer, name FROM ticket JOIN purchases USING (ticket_ID) JOIN retail_customer ON (email_customer = email) WHERE airline = %s AND flight_ID = %s AND departure_time = %s'
            cursor.execute(query, (airline, flightID_for_search, departure_time_for_search))
            flight_all_customer = cursor.fetchall()
            cursor.close()
        
        return render_template('staff_allflight.html',all_flight_by_date= all_flight_by_date, all_previous_flight_by_date = all_previous_flight_by_date, all_future_flight_by_date = all_future_flight_by_date, all_flight_by_source_destination=all_flight_by_source_destination, upcoming_flight = upcoming_flight, historical_flight = historical_flight, flight_all_customer = flight_all_customer, username = username, user_type = user_type)



@app.route('/flight_creating_process', methods=['GET', 'POST'])
def flight_creating_process():
        airline = session['airline']
        
        flightID = request.form['flightID']      #grab data from user search form in "allfight.html"
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        base_price = request.form['base_price']
        airplaneID = request.form['airplane_ID']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        flight_status = request.form['flight_status']

        #validate and insert
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline = %s AND flight_ID = %s AND departure_time = %s'
        cursor.execute(query, (airline, flightID, departure_time))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if (data):
                #If the previous query returns data, then user exists
                error = "This flight already exists."
                return redirect(url_for('create_new_flight', error=error))
        else:
                #*****Important: Foreign Key Constraints Check
                cursor_airplane = conn.cursor()
                query_airplane = 'SELECT * FROM airplane WHERE airline = %s and airplane_ID = %s'        #***IMPORTANT: Don't forget to deal with the situation when staff works for a NEW airline(check whether Airline exists first)!!!
                cursor_airplane.execute(query_airplane, (airline, airplaneID))
                data_airplane = cursor_airplane.fetchone()

                cursor_depart_airport = conn.cursor()
                query_depart_airport = 'SELECT * FROM airport WHERE name = %s'
                cursor_depart_airport.execute(query_depart_airport, (departure_airport))
                data_depart_airport = cursor_depart_airport.fetchone()

                cursor_arrival_airport = conn.cursor()
                query_arrival_airport = 'SELECT * FROM airport WHERE name = %s'
                cursor_arrival_airport.execute(query_arrival_airport, (arrival_airport))
                data_arrival_airport = cursor_arrival_airport.fetchone()
                
                if (not data_airplane) or (not data_depart_airport) or (not data_arrival_airport):        #*****If "airplane_ID" or airport-related name does not exist before(violates foreign key constraint), invalid input!
                    invalid = "Invalid Input. No such a plane/airport stored."
                    return redirect(url_for('create_new_flight', invalid=invalid))
                else:
                    cursor = conn.cursor()
                    ins = 'INSERT INTO flight VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'     #Notice Must Have 9 Columns to Insert Into the "flight" table!!!
                    cursor.execute(ins, (airline, flightID, base_price, departure_time, arrival_time, airplaneID, departure_airport, arrival_airport, flight_status))
                    #***Important above: Must Follow the EXACT ORDER of columns in the database!!!
                    conn.commit()        #***Important: DON'T FORGET AFTER UPDATES TO THE DATABASE!!!
                    cursor.close()
                    confirmation_message = "Your Flight Has Been Created!"
                    return redirect(url_for('create_new_flight', confirmation_message=confirmation_message))
       
        #return redirect(url_for('create_new_flight', flightID=flightID, departure_time=departure_time, arrival_time=arrival_time, base_price=base_price, airplane_ID=airplaneID, departure_airport=departure_airport, arrival_airport=arrival_airport, flight_status=flight_status))


@app.route('/create_new_flight', methods=['GET', 'POST'])
def create_new_flight():

        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        #display the default upcoming flights in 30 days
        cursor = conn.cursor()
        query = 'SELECT departure_time, arrival_time, airline, flight_ID, departure_airport, arrival_airport, flight_status FROM flight WHERE airline = %s AND departure_time > NOW() AND departure_time <= DATE_ADD(NOW(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline))
        upcoming_flight = cursor.fetchall()
        cursor.close()

        try:
            error=request.args['error']
        except:
            error=None

        try:
            invalid=request.args['invalid']
        except:
            invalid=None

        try:
            confirmation_message=request.args['confirmation_message']
        except:
            confirmation_message=None

        
        return render_template('create_new_flight.html', username=username, user_type=user_type, upcoming_flight=upcoming_flight, confirmation_message=confirmation_message, error=error, invalid=invalid)    


@app.route('/airplane_creating_process', methods=['GET', 'POST'])
def airplane_creating_process():
        airline = session['airline']
        
        airplane_ID = request.form['airplane_ID']      #grab data from user search form in "allfight.html"
        seat_capacity = request.form['seat_capacity']

        #validate and insert
        cursor = conn.cursor()
        query = 'SELECT * FROM airplane WHERE airline = %s AND airplane_ID = %s'
        cursor.execute(query, (airline, airplane_ID))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if (data):
                #If the previous query returns data, then user exists
                error = "This airplane already exists."
                return redirect(url_for('add_airplane', error=error))
        else:
            try:
                seat_capacity = int(seat_capacity)
                if seat_capacity <= 0:
                    error = "Please enter correct number for seat capacity"
                    return redirect(url_for('add_airplane', error=error))
                cursor = conn.cursor()
                ins = 'INSERT INTO airplane VALUES(%s,%s,%s)'
                cursor.execute(ins, (airline, airplane_ID, seat_capacity))
                #***Important above: Must Follow the EXACT ORDER of columns in the database!!!
                conn.commit()        #***Important: DON'T FORGET AFTER UPDATES TO THE DATABASE!!!
                cursor.close()
                confirmation_message = "Your Airplane Has Been Created!"
                return redirect(url_for('add_airplane', confirmation_message=confirmation_message))
            except:
                error = "Please enter correct number for seat capacity"
                return redirect(url_for('add_airplane', error=error))
                
        #return redirect(url_for('create_new_flight', flightID=flightID, departure_time=departure_time, arrival_time=arrival_time, base_price=base_price, airplane_ID=airplaneID, departure_airport=departure_airport, arrival_airport=arrival_airport, flight_status=flight_status))    


@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    
        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        #display the all airplanes owned by the airline
        cursor = conn.cursor()
        query = 'SELECT * FROM airplane WHERE airline = %s'
        cursor.execute(query, (airline))
        all_airplane = cursor.fetchall()
        cursor.close()

        try:
            error=request.args['error']
        except:
            error=None

        try:
            confirmation_message=request.args['confirmation_message']
        except:
            confirmation_message=None

        
        return render_template('create_new_airplane.html', username=username, user_type=user_type,all_airplane=all_airplane, confirmation_message=confirmation_message, error=error)    



@app.route('/airport_creating_process', methods = ['GET', 'POST'])
def airport_creating_process():
        
        airport_name = request.form['airport_name']      #grab data from user search form in "allfight.html"
        airport_city = request.form['airport_city']

        #validate and insert
        cursor = conn.cursor()
        query = 'SELECT * FROM airport WHERE name = %s'
        cursor.execute(query, (airport_name))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if (data):
                #If the previous query returns data, then user exists
                error = "This airport already exists."
                return redirect(url_for('add_airport', error=error))
        else:
                cursor = conn.cursor()
                ins = 'INSERT INTO airport VALUES(%s,%s)'
                cursor.execute(ins, (airport_name, airport_city))
                #***Important above: Must Follow the EXACT ORDER of columns in the database!!!
                conn.commit()        #***Important: DON'T FORGET AFTER UPDATES TO THE DATABASE!!!
                cursor.close()
                confirmation_message = "Your Airport Has Been Created!"
                return redirect(url_for('add_airport', confirmation_message=confirmation_message))
       
        #return redirect(url_for('create_new_flight', flightID=flightID, departure_time=departure_time, arrival_time=arrival_time, base_price=base_price, airplane_ID=airplaneID, departure_airport=departure_airport, arrival_airport=arrival_airport, flight_status=flight_status))


@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():

        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        try:
            error=request.args['error']
        except:
            error=None
        
        try:
            confirmation_message=request.args['confirmation_message']
        except:
            confirmation_message=None

        
        return render_template('create_new_airport.html', username=username, user_type=user_type, confirmation_message=confirmation_message, error=error)    


@app.route('/flight_status_change_processing', methods=['GET', 'POST'])
def flight_status_change_processing():
        airline = session['airline']
        
        flight_ID = request.form['flight_ID_for_status']      #grab data from user search form in "allfight.html"
        departure_time = request.form['departure_time']
        status_now = request.form['status_now']

        #validate and insert
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline = %s AND flight_ID = %s AND departure_time = %s'
        cursor.execute(query, (airline, flight_ID, departure_time))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if (not data):
                error = "This flight does not exist."
                return redirect(url_for('change_flight_status', error=error))
        else:
                cursor = conn.cursor()
                ins = 'UPDATE flight SET flight_status = %s WHERE airline = %s AND flight_ID = %s AND departure_time = %s'
                cursor.execute(ins, (status_now, airline, flight_ID, departure_time))
                #***Important above: Must Follow the EXACT ORDER of columns in the database!!!
                conn.commit()        #***Important: DON'T FORGET AFTER UPDATES TO THE DATABASE!!!
                cursor.close()
                confirmation_message = "Your Flight Status Has Been Changed!"
                return redirect(url_for('change_flight_status', confirmation_message=confirmation_message))


@app.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():

        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        #display all flight status in the airline
        cursor = conn.cursor()
        query = 'SELECT * FROM flight WHERE airline = %s'
        cursor.execute(query, (airline))
        all_flight_status = cursor.fetchall()
        cursor.close()

        try:
            error=request.args['error']
        except:
            error=None

        try:
            confirmation_message=request.args['confirmation_message']
        except:
            confirmation_message=None

        
        return render_template('change_flight_status.html', username=username, user_type=user_type,all_flight_status=all_flight_status, confirmation_message=confirmation_message, error=error)    


@app.route('/view_top5_agent', methods=['GET', 'POST'])
def view_top5_agent():
    
        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        #top 5 agent based on number of ticket (in this airline) during past month
        cursor = conn.cursor()
        query = 'SELECT email_agent, COUNT(DISTINCT ticket_ID) AS ticket_sales FROM purchase_for JOIN purchases USING (ticket_ID) JOIN ticket USING (ticket_ID) WHERE airline = %s AND date_purchase <= NOW() AND date_purchase >= DATE_SUB(NOW(), INTERVAL 1 MONTH) GROUP BY email_agent ORDER BY ticket_sales DESC LIMIT 5'
        cursor.execute(query, (airline))
        top5_agent_on_ticket_number_past_month = cursor.fetchall()
        cursor.close()

        #top 5 agent based on number of ticket (in this airline) during past year
        cursor = conn.cursor()
        query = 'SELECT email_agent, COUNT(DISTINCT ticket_ID) AS ticket_sales FROM purchase_for JOIN purchases USING (ticket_ID) JOIN ticket USING (ticket_ID) WHERE airline = %s AND date_purchase <= NOW() AND date_purchase >= DATE_SUB(NOW(), INTERVAL 1 YEAR) GROUP BY email_agent ORDER BY ticket_sales DESC LIMIT 5'
        cursor.execute(query, (airline))
        top5_agent_on_ticket_number_past_year = cursor.fetchall()
        cursor.close()

        #top 5 agent based on total commission (in this airline) during past year
        cursor = conn.cursor()
        query = 'SELECT email_agent, SUM(sold_price * 0.1) AS total_commission FROM purchase_for JOIN purchases USING (ticket_ID) JOIN ticket USING (ticket_ID) WHERE airline = %s AND date_purchase <= NOW() AND date_purchase >= DATE_SUB(NOW(), INTERVAL 1 YEAR) GROUP BY email_agent ORDER BY total_commission DESC LIMIT 5'
        cursor.execute(query, (airline))
        top5_agent_on_total_commission_past_year = cursor.fetchall()
        cursor.close()

        return render_template("view_top_agents.html", username=username, user_type= user_type, top5_agent_on_ticket_number_past_month=top5_agent_on_ticket_number_past_month, top5_agent_on_ticket_number_past_year=top5_agent_on_ticket_number_past_year, top5_agent_on_total_commission_past_year=top5_agent_on_total_commission_past_year)



@app.route('/view_customer_all_flight_processing', methods=['GET', 'POST'])
def view_customer_all_flight_processing():
        airline = session['airline']
        
        customer_email = request.form['customer_email']

        return redirect(url_for('view_frequent_customer', customer_email = customer_email))
    
    
@app.route('/view_frequent_customer', methods=['GET', 'POST'])
def view_frequent_customer():
        username = session['username']
        user_type = session['user_type']
        airline = session['airline']
        #*****Important notice: creating a "customer_ticket_count_last_year" VIEW based on airline and departure_time!!!

        cursor = conn.cursor()
        query = 'CREATE VIEW customer_ticket_count_last_year as (SELECT airline,email, name,phone_number, birth_date,passport_country,city,count(ticket_ID) as total_ticket_purchased from ticket_with_purchase_customer_info Where airline = %s and date(departure_time) <= CURDATE() and date(departure_time)>= Date_SUB(CURDATE(),interval 12 month) group by email)'
        cursor.execute(query, (airline))
        cursor.close()
        #most frequent customer FOR THIS AIRLINE during the past year
        cursor = conn.cursor()
        query = 'SELECT email, name, phone_number, birth_date, passport_country, city, total_ticket_purchased FROM customer_ticket_count_last_year WHERE total_ticket_purchased = (SELECT MAX(total_ticket_purchased) FROM customer_ticket_count_last_year)'
        cursor.execute(query)
        most_frequent_customer = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = 'DROP VIEW customer_ticket_count_last_year'
        cursor.execute(query)
        cursor.close()

        


        customer_all_flight = None     #initialization of result
        #*****when the user enter the form, it's already guaranteed that "customer_email" could not be empty(not input) as it's "required" in HTML!
        try:
            customer_email = request.args['customer_email']   #*****IMPORTANT DETAIL NOTICE: the outcome of "request.args[]" would be of type STRING!!!(so if you want to extract the exact thing within the string(""), probably have to use "eval()"!)
        except:
            customer_email = None

        if customer_email:
        #query the result for all flights taken by the customer in this airline
            cursor = conn.cursor()
            query = 'SELECT * FROM ticket JOIN purchases USING (ticket_ID) JOIN flight USING (airline, flight_ID, departure_time) WHERE email_customer = %s AND airline = %s AND date(departure_time) <= CURDATE()'
            cursor.execute(query, (customer_email, airline))
            customer_all_flight = cursor.fetchall()
            cursor.close()
            #print(customer_all_flight)    #debug
            
        return render_template("view_frequent_customer.html", username=username, user_type= user_type, most_frequent_customer=most_frequent_customer, customer_all_flight=customer_all_flight)



@app.route('/view_top_destination', methods=['GET', 'POST'])
def view_top_destination():
        username = session['username']
        user_type = session['user_type']
        airline = session['airline']

        cursor = conn.cursor()
        query = 'create view airline_destination_traffic_past3months as (SELECT arrival_airport, arrival_city as city, count(ticket_ID) as total_travellers FROM ticket_with_city WHERE airline = %s and date(departure_time) <= CURDATE() and date(departure_time)>= Date_SUB(CURDATE(),interval 3 month) group by arrival_airport ORDER BY `total_travellers` DESC LIMIT 3) '
        cursor.execute(query, (airline))
        cursor.close()

        cursor = conn.cursor()
        query = 'create view airline_destination_traffic_pastyear as (SELECT arrival_airport, arrival_city as city, count(ticket_ID) as total_travellers FROM ticket_with_city WHERE airline = %s and date(departure_time) <= CURDATE() and date(departure_time)>= Date_SUB(CURDATE(),interval 12 month) group by arrival_airport ORDER BY `total_travellers` DESC LIMIT 3)'
        cursor.execute(query, (airline))
        cursor.close()

        #top 3 destinations within the airline for the past 3 months
        cursor = conn.cursor()
        query = 'SELECT arrival_airport, city, total_travellers FROM airline_destination_traffic_past3months'
        cursor.execute(query)
        top3_destinations_past3months = cursor.fetchall()
        cursor.close()

        #top 3 destinations within the airline for the past year
        #*****Important notice: already created a "airline_destination_traffic_pastyear" VIEW in the database!!!(***another "destination_traffic_pastyear" not distinguishing airlines is NOT CORRECT!)
        cursor = conn.cursor()
        query = 'SELECT arrival_airport, city, total_travellers FROM airline_destination_traffic_pastyear'
        cursor.execute(query)
        top3_destinations_pastyear = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = 'drop view airline_destination_traffic_past3months'
        cursor.execute(query)
        cursor.close()

        cursor = conn.cursor()
        query = 'drop view airline_destination_traffic_pastyear'
        cursor.execute(query)
        cursor.close()

        return render_template("view_top_destination.html", username=username, user_type=user_type, top3_destinations_past3months=top3_destinations_past3months, top3_destinations_pastyear=top3_destinations_pastyear)


@app.route('/total_ticket_sales_filter', methods=['GET', 'POST'])
def total_ticket_sales_filter():
    
        start_date_spec = request.form['start_date']
        end_date_spec = request.form['end_date']

        return redirect(url_for('view_ticket_report', start_date_spec = start_date_spec, end_date_spec = end_date_spec))

@app.route('/view_ticket_report', methods=['GET', 'POST'])
def view_ticket_report():
        username = session["username"]
        user_type = session["user_type"]
        airline = session["airline"]

        ticket_sales_past30days = None
        ticket_sales_pastyear = None

        ticket_sales_by_date = None
        
        #to see if the user has entered date range to search
        try:
            start_date_spec = request.args['start_date_spec']
            if len(start_date_spec.split("-")) != 3 and len(start_date_spec) != 10:
                start_date_spec = None
        except:
            start_date_spec = None
        
        
        try:
            end_date_spec = request.args['end_date_spec']
            if len(end_date_spec.split("-")) != 3 and len(end_date_spec) != 10:
                end_date_spec = None
        except:
            end_date_spec = None

        #textual number display(not graph)
        if start_date_spec and end_date_spec:      #[p]the logic here: only when both "start_date" and "end_date" have been entered in the form, the search is considered valid
            cursor1 = conn.cursor()
            query1 = "SELECT COUNT(DISTINCT ticket_ID) AS ticket_sales FROM ticket JOIN purchases USING (ticket_ID) WHERE airline = %s AND date_purchase <= %s AND date_purchase >= %s"
            cursor1.execute(query1, (airline, end_date_spec, start_date_spec))
            ticket_sales_by_date = cursor1.fetchone()      #*****IMPORTANT DETAIL NOTICE: "COUNT" would just result "0"(SQL) for "fetchone()" if no result!!!
            cursor1.close()
       
            

        #default view: "past month" & "past year"
        #*****IMPORTANT DETAIL NOTICE: "COUNT" would result 0(SQL) for "fetchone()" if no result!!!
        cursor2 = conn.cursor()
        query2 = "SELECT COUNT(DISTINCT ticket_ID) AS ticket_sales FROM ticket JOIN purchases USING (ticket_ID) WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
        cursor2.execute(query2, (airline))
        ticket_sales_past30days = cursor2.fetchone()
        cursor2.close()

        cursor3 = conn.cursor()
        query3 = "SELECT COUNT(DISTINCT ticket_ID) AS ticket_sales FROM ticket JOIN purchases USING (ticket_ID) WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)"
        cursor3.execute(query3, (airline))
        ticket_sales_pastyear = cursor3.fetchone()
        cursor3.close()

        #######IMPORTANT PENDING: DRAWING GRAPH!!!!
        if  start_date_spec and end_date_spec:
            print("start_date_spec input:", start_date_spec)     #ready for debugging
            print("end_date_spec input:", end_date_spec)
                #query database for the Month-wise range covered by the user's search inputs
            cursor = conn.cursor()
            by_month_query = "SELECT EXTRACT(YEAR_MONTH From date_purchase) AS month, COUNT(DISTINCT ticket_ID) AS ticket_sales FROM ticket JOIN purchases USING (ticket_ID) WHERE airline = %s AND date_purchase <= %s AND date_purchase >= %s GROUP BY EXTRACT(YEAR_MONTH From date_purchase)"
            cursor.execute(by_month_query, (airline, end_date_spec, start_date_spec))
            by_month_data = cursor.fetchall()      #*****IMPORTANT DETAIL NOTICE: here if there's no query row then AN EMPTY SET would be returned!!
                #***NOTICE: HERE "by_month_data" IS IN A NORMAL FORMAT OF "A LIST OF DICTIONARY"("fetchall()" result)!!!
            print(by_month_data)       #ready for debugging
            print(len(by_month_data))    #ready for debugging
            monthlist = []          #*prepare for x-axis data
            valuelist = []          #*prepare for y-axis data
                
            end_month = int(str(end_date_spec).split("-")[1])     #***"int" type
            end_year = int(str(end_date_spec).split("-")[0])
            if len(str(end_month)) == 1:       #single_digit month format: need to append "0" on the top for nice visual effect
                end_month_string = str(end_year)+"0"+str(end_month)      #now result: complete year-month display: e.g. "201905"
            else:
                end_month_string = str(end_year)+str(end_month)

            start_month = int(str(start_date_spec).split("-")[1])
            start_year = int(str(start_date_spec).split("-")[0])
            if len(str(start_month)) == 1:
                start_month_string = str(start_year)+"0"+str(start_month)
            else:
                start_month_string = str(start_year)+str(start_month)

            this_month = end_month       #***"int" type
            this_year = end_year
            while True:
                    #do the same detail format pre-processing to the "this_month"
                if len(str(this_month)) == 1:
                    this_month_string = str(this_year)+"0"+str(this_month)     #make "this_month_string" also in the format like "201905"
                else:
                    this_month_string = str(this_year)+str(this_month)
                monthlist.append(this_month_string)     #***add the "this_month_string" into the "monthlist"(x-axis)
                for item in by_month_data:          #*****Remember that by_month_data is already normal format of "fetchall()" here!
                    if str(item["month"]) == this_month_string:      #match: e.g. "201904"
                        valuelist.append(int(item["ticket_sales"]))      #add the value data from the query result into the "valuelist"(y-axis)
                if len(valuelist) < len(monthlist):
                    valuelist.append(int(0))
                if this_year == start_year and this_month == start_month:
                    break      #stop here!
                this_year, this_month = last_month(this_year, this_month)     #use the pre-pared self-defined function "last_month()" at the beginning of the code!!!
            monthlist = list(reversed(monthlist))       #turn to the normal order
            valuelist = list(reversed(valuelist))
            print("monthlist:", monthlist)     #ready for debugging
            print("valuelist:", valuelist)
        else:    
            #first, define which is the "starting month" covered in the "last year"
            cursor = conn.cursor()
            starting_month_pastyear_query = "SELECT EXTRACT(YEAR_MONTH From DATE_SUB(CURDATE()+1, INTERVAL 1 YEAR)) AS starting_month"     #*e.g.: if today is "2019-05-08", then starting date of this past-year graph is "2018-05-09"(so starting_month is just "201805")
            cursor.execute(starting_month_pastyear_query)
            starting_month_result = cursor.fetchone()
            starting_month_string = str(starting_month_result['starting_month'])        #*expected: in format like "201805"
            cursor.close()
            starting_month = int(starting_month_string[-2:])    #e.g.: 5 (May)
            starting_year = int(starting_month_string[:-2])       #e.g.: 2019
            print("starting month requery result:", starting_month_string)
            print("starting month int:", starting_month)
            print("starting year int:", starting_year)

            #define which is the "ending month" covered in the "last year"
            cursor = conn.cursor()
            ending_month_pastyear_query = "SELECT EXTRACT(YEAR_MONTH From CURDATE()) AS ending_month"     #*e.g.: if today is "2019-05-08", then starting date of this past-year graph is "2018-05-09"(so starting_month is just "201805")
            cursor.execute(ending_month_pastyear_query)
            ending_month_result = cursor.fetchone()
            ending_month_string = str(ending_month_result['ending_month'])        #*expected: in format like "201805"
            cursor.close()
            ending_month = int(ending_month_string[-2:])
            ending_year = int(ending_month_string[:-2])
            print("ending month requery result:", ending_month_string)
            print("ending month int:", ending_month)
            print("ending year int:", ending_year)

            #get the Month-wise query result data
            cursor = conn.cursor()
            pastyear_query = "SELECT EXTRACT(YEAR_MONTH From date_purchase) AS month, COUNT(DISTINCT ticket_ID) AS ticket_sales FROM ticket JOIN purchases USING (ticket_ID) WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase > DATE_SUB(CURDATE(), INTERVAL 1 YEAR) GROUP BY EXTRACT(YEAR_MONTH From date_purchase)"
            cursor.execute(pastyear_query, (airline))
            pastyear_monthly_data = cursor.fetchall()      #*****IMPORTANT DETAIL NOTICE: here if there's no query row then AN EMPTY SET would be returned!!
            cursor.close()
            print(pastyear_monthly_data)       #ready for debugging
            print(len(pastyear_monthly_data))    #ready for debugging
            monthlist = []          #*prepare for x-axis data
            valuelist = []          #*prepare for y-axis data
            
            this_month = ending_month       #***"int" type
            this_year = ending_year
            while True:
                #do the same detail format pre-processing to the "this_month"
                if len(str(this_month)) == 1:
                    this_month_string = str(this_year)+"0"+str(this_month)     #make "this_month_string" also in the format like "201905"
                else:
                    this_month_string = str(this_year)+str(this_month)
                print("this_month_string:", this_month_string)
                monthlist.append(this_month_string)     #***add the "this_month_string" into the "monthlist"(x-axis)
                for item in pastyear_monthly_data:          #*****Remember that by_month_data is already normal format of "fetchall()" here!
                    if str(item["month"]) == this_month_string:      #match: e.g. "201904"
                        valuelist.append(int(item["ticket_sales"]))      #add the value data from the query result into the "valuelist"(y-axis)
                if len(valuelist) < len(monthlist):
                    valuelist.append(int(0))
                if this_year == starting_year and this_month == starting_month:
                    break      #stop here!
                this_year, this_month = last_month(this_year, this_month)     #use the pre-pared self-defined function "last_month()" at the beginning of the code!!!
            monthlist = list(reversed(monthlist))       #turn to the normal order
            valuelist = list(reversed(valuelist))
            print("monthlist:", monthlist)     #ready for debugging
            print("valuelist:", valuelist)     #ready for debugging
                     
        
        return render_template("view_ticket_report.html", username = username, user_type = user_type, start_date = start_date_spec, end_date = end_date_spec, ticket_sales_past30days = ticket_sales_past30days, ticket_sales_pastyear = ticket_sales_pastyear, ticket_sales_by_date = ticket_sales_by_date, monthlist=json.dumps(monthlist), valuelist=json.dumps(valuelist))


@app.route('/revenue_comparison', methods=['GET', 'POST'])
def revenue_comparison():
    username = session["username"]
    user_type = session["user_type"]
    airline = session["airline"]

    agent_past30days = None
    direct_past30days = None
    agent_pastyear = None
    direct_pastyear = None


    cursor2 = conn.cursor()
    query2 = "SELECT SUM(sold_price) * 0.9 AS total_revenue_from_agent FROM  `purchase_for` natural left outer join ticket join purchases using (ticket_ID) WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
    cursor2.execute(query2, (airline))
    agent_past30days = cursor2.fetchone()
    cursor2.close()

    cursor3 = conn.cursor()
    query3 = "SELECT SUM(sold_price) * 0.9 AS total_revenue_from_agent FROM  `purchase_for` natural left outer join ticket join purchases using (ticket_ID) WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)"
    cursor3.execute(query3, (airline))
    agent_pastyear = cursor3.fetchone()
    cursor3.close()

    #create view for direct sales only
    cursor4 = conn.cursor()
    query4 = "create view direct_sales_list as (SELECT * FROM  `purchases` natural left outer join ticket WHERE ticket_ID not in (select  ticket_ID from purchase_for))"
    cursor4.execute(query4)
    cursor4.close()

    cursor5 = conn.cursor()
    query5 = "SELECT SUM(sold_price) AS total_revenue_from_direct FROM direct_sales_list WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
    cursor5.execute(query5, (airline))
    direct_past30days = cursor5.fetchone()
    cursor5.close()

    cursor6 = conn.cursor()
    query6 = "SELECT SUM(sold_price) AS total_revenue_from_direct FROM direct_sales_list WHERE airline = %s AND date_purchase <= CURDATE() AND date_purchase >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)"
    cursor6.execute(query6, (airline))
    direct_pastyear = cursor6.fetchone()
    cursor6.close()

    #drop view after getting all the data
    cursor7 = conn.cursor()
    query7 = "drop view direct_sales_list"
    cursor7.execute(query7)
    cursor7.close()

    #WARNING: the following "print" debugging statement would cause some error if the variable is None/empty!
    #print(int(agent_past30days["total_revenue_from_agent"]), direct_past30days["total_revenue_from_direct"], int(agent_pastyear["total_revenue_from_agent"]), direct_pastyear["total_revenue_from_direct"])

    #draw graph
        
    recent_1month = []
    recent_1year = []
    
    if agent_past30days["total_revenue_from_agent"] == None:
        recent_1month.append(0)
    else:
        recent_1month.append(int(agent_past30days["total_revenue_from_agent"]))

    if direct_past30days["total_revenue_from_direct"] == None:
        recent_1month.append(0)
    else:
        recent_1month.append(int(direct_past30days["total_revenue_from_direct"]))

    if agent_pastyear["total_revenue_from_agent"] == None:
        recent_1year.append(0)
    else:
        recent_1year.append(int(agent_pastyear["total_revenue_from_agent"]))
        
    if direct_pastyear["total_revenue_from_direct"] == None:
        recent_1year.append(0)
    else:
        recent_1year.append(int(direct_pastyear["total_revenue_from_direct"]))
                            
    print(recent_1month)
    print(recent_1year)
    
    return render_template("revenue_comparison.html", username = username, user_type = user_type, recent_1month=json.dumps(recent_1month), recent_1year=json.dumps(recent_1year))

    


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
        app.run('127.0.0.1', 5000)
