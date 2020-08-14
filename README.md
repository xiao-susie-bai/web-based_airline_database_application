# Web-based Air Ticket Reservation & Management Relational Database Application 
### (SQL, Python Flask, HTML/JS/CSS)

The main objective of this comprehensive project is to design and implement a relational database and to develop a full-stack web-based application system on top of the database, for airline companies to allow their customers to book their air tickets and to make management of air ticket reservations convenient for staff. The project focuses on conceptual design, logical design, implementation, operation and maintenance of a relational database; the associated web-based application communicates with the database through server and performs functional use cases (e.g. retrieve, store, manage and visualize information) for different types of database users.

In this project, firstly, the database is framed through the design of an E-R diagram, translated to the relational schema on which the actual implementation is based. Essential information about **airlines, customers, staff, airplanes, airports, flights and air tickets** is added to initialize the database. The web-based application is developed under the Flask framework, using Python, MySQL and HTML/JS/CSS. The use cases of the application can be conveniently tested on a Apache/MySQL/PHP (xampp, wamp, lamp, mamp etc. depending on the OS) package, which includes MySQL and phpMyAdmin GUI (free download e.g.: https://www.apachefriends.org/download.html; (Windows) http://www.wampserver.com/en/download.php; (Mac) https://www.mamp.info/en/mamp/mac/).


### More about how the project works!:

In this project, there are several airports, each consisting of a unique name and a city; and several airlines, each with a unique name. Each airline owns several airplanes, where each airplane has a unique ID number within that airline and the number of seats on it. Each airline operates flights, which consist of the airline, a unique flight number within that airline, departure airport, departure time, arrival airport, arrival time, base price, and the ID number of the airplane for the flight.

Anyone (including users not signed in) can see flights (future flights) based on the source airport, destination airport, source city, or destination city, or depart date (for one way) (departure and arrival dates for round trip). Anyone can also see the status (e.g. delayed) of the flight.

A ticket can be purchased for a flight either by a customer or a booking agent (on behalf of customer), and will contain information about the customer's email address, the airline name, the flight number, sold price (possibly different from base price of the flight), payment information (credit/debit, card number, name on card, expiration dat etc.), purchase date time, and a booking agent ID (if available). Each ticket has a unique generated ticket ID number in the system.

Customers can purchase a flight ticket as long as there is still room on the plane, which is determined by the number of tickets already booked and the seating capacity of the airplane. Ticket price of a flight depends on two factors -- minimum/base price as set by the airline and additional price which depends on demand of the flight; if 70% of the capacity is already booked for the flight, extra 20% will be added with the minimum/base price.

When a booking agent purchases a ticket on behalf of a customer, he/she receives a 10% commission from the ticket price.

An airline staff has the authority to create new flights for the particular airline they work for, set the ticket base price, add new airplanes, set flight statuses, and more.

### Use Cases Specification:

#### Public (any users whether logged in or not logged in):

1.**View Public Info**: a). search for future flights; b). see the flights statuses

2.**Register**: 3 types of user registration -- Customer, Booking agent, Airline staff

3.**Login**: 3 types of user login. Enter username (email address) and password; if login is successful, a session is initiated; if unsuccessful, the user will be notified.

#### Customer:

1.**View My Flights**: The default is showing for the future flights. The user can also search for his/her puchased flights based on date ranges, departure location etc..

2.**Search for flights**: Search for future flights.

3.**Purchase tickets**: Choose a flight and purchase its ticket.

4.**Track My Spending**: Default view is total amount of money spent in the past year and a bar chart showing monthly money spent for the last 6 months. The user can also view the info based on date range specified.

5.**Logout**

#### Booking agent:

1.**View My Flights**: View future flights information for which the agent purchased on behalf of customers.

2.**Search for flights**

3.**Purchase tickets**

4.**View My Commission**: Default view is total amount of commission received in the past 30 days, the average commission received per ticket booked in the past 30 days, and total number of tickets sold by the agent in the past 30 days. The user can also view the info based on date range specified.

5.**View Top Customers**: View top 5 customers based on number of tickets bought from the agent in the past 6 months and top 5 customers based on amount of commission received in the past year. Also display bar charts showing each of these top customers and the values of the corresponding criteria.

6.**Logout**

#### Airline staff:

1.**View The Airline Flights**: By Default it shows all the future flights in the next 30 days operated by the airline company the staff works for. The staff can also see all the current/past/future flights operated by the airline based on date ranges, departure/destination location etc. specified. All the customers of a particular flight can be seen as well.

2.**Create New Flights**

3.**Change Status of Flights** (e.g. change from "on-time" to "delayed" or vice versa)

4.**Add Airplane in the System** (the staff can see all the airplanes owned by the airline he/she works for by default.)

5.**Add New Airport in the System**

6.**View Top Booking Agents**: View the top 5 booking agents based on number of ticket sold during past month & year, and based on amount of commission received during the past year, for the specific airline the staff works for.

7.**View Frequent Customers**: View the most frequent retail customer (not booking agent) during the past year, as well as a list of all flights a particular customer has taken on the particular airline the staff works for.

8.**View Reports**: View total number of tickets sold during the past year & the past month by default, as well as based on date range specified. A bar chart shows monthly tickets sold accordingly as well.

9.**Comparison of Revenue Earned**: Display a pie chart about total amount of revenue eared from direct sales (retail customers without using a book agent) compared with total amount of revenue earned from indirect sales (customers using a book agent) during the past month and past year.

10.**View Top Destinations**: View the 3 most popular destinations for the past 3 months and the past year.

11.**Logout**



