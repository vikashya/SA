/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */



/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */
SELECT *
FROM `Facilities`
WHERE membercost <>0

Tennis Court 1
Tennis Court 2
Massage Room 1
Massage Room 2
Squash Court

/* Q2: How many facilities do not charge a fee to members? */

SELECT count(facid)
FROM `Facilities`
WHERE membercost = 0

4

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

SELECT facid, name as 'facility name' , membercost as 'member cost', monthlymaintenance as 'monthly maintenance'
FROM `Facilities`
WHERE membercost < (monthlymaintenance*0.2)

Tennis Court 1	5	200
Tennis Court 2	5	200
Badminton Court	0	50
Table Tennis	0	10
Massage Room 1	9.9	3000
Massage Room 2	9.9	3000
Squash Court	3.5	80
Snooker Table	0	15
Pool Table		0	15


/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */
SELECT * FROM `Facilities` WHERE facid in (1,5)

1	Tennis Court 2	5	25	8000	200
5	Massage Room 2	9.9	80	4000	3000


/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */
SELECT name,
		monthlymaintenance,
		case
			when monthlymaintenance > 100 THEN 'expensive'
			else 'cheap'
		END as fac_type
FROM `Facilities`

Tennis Court 1	200	expensive
Tennis Court 2	200	expensive
Badminton Court	50	cheap
Table Tennis	10	cheap
Massage Room 1	3000	expensive
Massage Room 2	3000	expensive
Squash Court	80	cheap
Snooker Table	15	cheap
Pool Table	15	cheap


/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */
SELECT firstname,surname FROM `Members` WHERE memid in (SELECT max(memid) FROM `Members`)

Darren 	Smith

/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

SELECT distinct concat(m.firstname ,' ',  m.surname) as membername, f.name as facilityname
FROM Bookings b, Facilities f, Members m
WHERE b.facid = f.facid
AND b.memid = m.memid
AND f.name LIKE 'Tennis Court%'
order by membername 


/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

SELECT concat(m.firstname ,' ',  m.surname) as membername,f.name as facilityname ,
case  
	when b.memid > 0 then f.membercost*b.slots
	else f.guestcost *slots
	end as cost 
FROM `Bookings` b, Facilities f, Members m
WHERE STR_TO_DATE( starttime, '%Y-%m-%d' ) = '2012-09-14'
AND b.facid = f.facid
and (case  
	when b.memid > 0 then f.membercost*b.slots
	else f.guestcost *slots
	end > 30)
and b.memid = m.memid
order by cost desc



/* Q9: This time, produce the same result as in Q8, but using a subquery. */

select * from (SELECT concat(m.firstname ,' ',  m.surname) as membername,f.name as facilityname ,
case  
	when b.memid > 0 then f.membercost*b.slots
	else f.guestcost *slots
	end as cost 
FROM `Bookings` b, Facilities f, Members m
WHERE STR_TO_DATE( starttime, '%Y-%m-%d' ) = '2012-09-14'
AND b.facid = f.facid
and b.memid = m.memid) x 
where x.cost > 30
order by cost desc

/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */
select facilityname , sum(cost) as tot_rev from ( SELECT f.name as facilityname ,
case  
	when b.memid > 0 then f.membercost*b.slots
	else f.guestcost *slots
	end as cost 
FROM `Bookings` b, Facilities f 
WHERE b.facid = f.facid ) x 
group by facilityname
having sum(cost) < 1000
order by tot_rev desc