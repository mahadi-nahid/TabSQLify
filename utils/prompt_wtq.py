import time
import os
import openai
import tiktoken

# ---------------------------------------------------------------
API_KEY = ### 

os.environ['OPENAI_API_KEY'] = API_KEY
# openai.api_key = os.getenv("OPENAI_API_KEY")

# new
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

client = OpenAI()


p_wtq_full = """For a given question, find the answer based on the table information. 

Table: My Brother and Me (Series #,  Season #, Title, Notes, Original air date)

Series # | Season # | Title | Notes | Original air date
1 | 1 | The Charity | Alfie, Dee Dee, and Melanie are supposed to be helping | October 15, 1994
2 | 1 | The Practical Joke War | Alfie and Goo unleash harsh practical jokes on Dee Dee | October 22, 1994
3 | 1 | The Weekend Aunt Helen Came | The boy's mother, Jennifer, leaves for the weekend and she | November 1, 1994
4 | 1 | Robin Hood Play | Alfie's school is performing the play Robin Hood and Alfie | November 9, 1994
5 | 1 | Basketball Tryouts | Alfie tries out for the basketball team and doesn't make | November 30, 1994
6 | 1 | Where's the Snake? | Dee Dee gets a snake, but he doesn't want his | December 6, 1994
7 | 1 | Dee Dee's Girlfriend | A girl kisses Dee Dee in front of Harry and | December 15, 1994
8 | 1 | Dee Dee's Haircut | Dee Dee wants to get a hair cut by Cool | December 20, 1994
9 | 1 | Dee Dee Runs Away | Dee Dee has been waiting to go to a monster | December 28, 1994
10 | 1 | 'Donnell's Birthday Party | Donnell is having a birthday party and brags about all | January 5, 1995
11 | 1 | Alfie's Birthday Party | Goo and Melanie pretend they are dating and they leave | January 19, 1995
12 | 1 | Candy Sale | Alfie and Goo are selling candy to make money for | January 26, 1995
13 | 1 | The Big Bully | Dee Dee gets beat up at school and his friends | February 2, 1995

Question: alfie's birthday party aired on january 19. what was the airdate of the next episode?
A: To find the answer to this question, let’s think step by step. From the table, we can look into the ’Title’ column and find that the next episode after ‘Alfie’s Birthday Party’ is ‘Candy Sale’. The ‘Original air date’ of ‘Candy Sale’ is January 26, 1995.
Therefore, the answer is January 26, 1995.
Answer: January 26, 1995 

Table: Radhika Pandit (Year, Film, Role, Language, Notes)

Year | Film | Role | Language | Notes
2008 | Moggina Manasu | Chanchala | Kannada | Filmfare Award for Best Actress - Kannada Karnataka State Film Award
2009 | Olave Jeevana Lekkachaara | Rukmini | Kannada | Innovative Film Award for Best Actress
2009 | Love Guru | Kushi | Kannada | Filmfare Award for Best Actress - Kannada
2010 | Krishnan Love Story | Geetha | Kannada | Filmfare Award for Best Actress - Kannada Udaya Award for Best
2010 | Gaana Bajaana | Radhey | Kannada | 
2011 | Hudugaru | Gayithri | Kannada | Nominated, Filmfare Award for Best Actress – Kannada
2012 | Alemari | Neeli | Kannada | 
2012 | Breaking News | Shraddha | Kannada | 
2012 | Addhuri | Poorna | Kannada | Udaya Award for Best Actress Nominated — SIIMA Award for Best
2012 | 18th Cross | Punya | Kannada | 
2012 | Sagar | Kajal | Kannada | 
2012 | Drama | Nandini | Kannada | 
2013 | Kaddipudi | Uma | Kannada | 
2013 | Dilwala | Preethi | Kannada | 
2013 | Bahaddoor | Anjali | Kannada | Filming
2014 | Mr. & Mrs. Ramachari |  |  | Announced
2014 | Endendigu |  |  | Filming

Question: what is the total number of films with the language of kannada listed?
A: To find the answer to this question, let’s think step by step. From the table, we can see that there are several rows where the ‘Language’ column has the value ‘Kannada’. There are 15 rows with the value ‘Kannada’ in the ‘Language’ column.
Therefore, the answer is 15.
Answer: 15

"""
p_answer_wtq = """Based on the table information bellow, find the answer to the given question correctly. 

Table_title: Piotr Kędzia
Table:
Year | Venue | Position
2001 | Debrecen, Hungary | 2nd
2001 | Debrecen, Hungary | 1st
2001 | Grosseto, Italy | 1st
2003 | Tampere, Finland | 3rd
2003 | Tampere, Finland | 2nd
2005 | Erfurt, Germany | 11th (sf)
2005 | Erfurt, Germany | 1st
2005 | Izmir, Turkey | 7th
2005 | Izmir, Turkey | 1st
2006 | Moscow, Russia | 2nd (h)
2006 | Gothenburg, Sweden | 3rd
2007 | Birmingham, United Kingdom | 3rd
2007 | Bangkok, Thailand | 7th
2007 | Bangkok, Thailand | 1st
2008 | Valencia, Spain | 4th
2008 | Beijing, China | 7th
2009 | Belgrade, Serbia | 2nd

Question: in what city did piotr's last 1st place finish occur?
A: To find the answer to this question, let’s think step by step.
Based on the table, Piotr Kędzia's last 1st place finish occurred in angkok, Thailand in 2007. This is the most recent year in the table where he finished in 1st place. 
Therefore, the answer is Bangkok, Thailand.
Answer: Bangkok, Thailand

Table_title: Playa de Oro International Airport
Table:
City | Passengers
United States, Los Angeles | 14,749
United States, Houston | 5,465
Canada, Calgary | 3,761
Canada, Saskatoon | 2,282
Canada, Vancouver | 2,103
United States, Phoenix | 1,829
Canada, Toronto | 1,202
Canada, Edmonton | 110
United States, Oakland | 107

Question: how many more passengers flew to los angeles than to saskatoon from manzanillo airport in 2013?
A: To find the answer to this question, let’s think step by step.
Based on the table, in 2013, the number of passengers who flew to Los Angeles from Manzanillo Airport was 14,749, while the number of passengers who flew to Saskatoon was 2,282. 
So, the difference in the number of passengers between Los Angeles and Saskatoon is 14,749 - 2,282 = 12,467. 
Therefore, the answer is 12,467.
Answer: 12,467

"""

p_sql_answer_wtq = """Based on the table title and execution result of the sql query bellow, find the answer to the given question correctly. 

Table_title: Piotr Kędzia
SQL: select Year, Venue, Position from T

Year | Venue | Position
2001 | Debrecen, Hungary | 2nd
2001 | Debrecen, Hungary | 1st
2001 | Grosseto, Italy | 1st
2003 | Tampere, Finland | 3rd
2003 | Tampere, Finland | 2nd
2005 | Erfurt, Germany | 11th (sf)
2005 | Erfurt, Germany | 1st
2005 | Izmir, Turkey | 7th
2005 | Izmir, Turkey | 1st
2006 | Moscow, Russia | 2nd (h)
2006 | Gothenburg, Sweden | 3rd
2007 | Birmingham, United Kingdom | 3rd
2007 | Bangkok, Thailand | 7th
2007 | Bangkok, Thailand | 1st
2008 | Valencia, Spain | 4th
2008 | Beijing, China | 7th
2009 | Belgrade, Serbia | 2nd

Question: in what city did piotr's last 1st place finish occur?
A: To find the answer to this question, let’s think step by step.
Based on the table, Piotr Kędzia's last 1st place finish occurred in angkok, Thailand in 2007. This is the most recent year in the table where he finished in 1st place. 
Therefore, the answer is Bangkok, Thailand.
Answer: Bangkok, Thailand

Table_title: Playa de Oro International Airport
SQL: select City, Passengers from T;

City | Passengers
United States, Los Angeles | 14,749
United States, Houston | 5,465
Canada, Calgary | 3,761
Canada, Saskatoon | 2,282
Canada, Vancouver | 2,103
United States, Phoenix | 1,829
Canada, Toronto | 1,202
Canada, Edmonton | 110
United States, Oakland | 107

Question: how many more passengers flew to los angeles than to saskatoon from manzanillo airport in 2013?
A: To find the answer to this question, let’s think step by step.
Based on the table, in 2013, the number of passengers who flew to Los Angeles from Manzanillo Airport was 14,749, while the number of passengers who flew to Saskatoon was 2,282. 
So, the difference in the number of passengers between Los Angeles and Saskatoon is 14,749 - 2,282 = 12,467. 
Therefore, the answer is 12,467.
Answer: 12,467

"""

p_col_wtq = """Generate SQL given the question and table for selecting the required columns to answer the question correctly.

Table_title: Marek Plawgo
Table_columns: (Year, Competition, Venue, Position, Event, Notes)
Question: when was his first 1st place record?
output: Let's think step by step.
columns: ['Year',  'Position']
sql: select Year,  Position from T

Table_title: 2013\u201314 Toros Mexico season
Table_columns: (Game, Day, Date, Kickoff, Opponent, Results_Score, Results_Record, Location, Attendance)
Question: what was the number of people attending the toros mexico vs. monterrey flash game?
output: Let's think step by step.
columns: ['Attendance', 'Opponent']
sql: select Attendance, Opponent from T

Table_title: Radhika Pandit
Table_columns:  (Year, Film', Role', Language, Notes)
Question: what is the total number of films with the language of kannada listed?
output: Let's think step by step.
columns: ['Film', 'Language']
sql: select Film, Language from T

Table_title: List of storms on the Great Lakes
Table_columns:  (Ship, Type_of_Vessel, Lake, Location, Lives_lost)
Question: how many more ships were wrecked in lake huron than in erie?
output: Let's think step by step.
columns: ['Ship', 'Lake']
sql: select Ship, Lake from T

Table_title: List of hospitals in North Carolina
Table_columns:  (Name, City, Hospital_beds, Operating_rooms, Total, Trauma_designation, Affiliation, Notes)
Question: what is the only hospital to have 6 hospital beds?
output: Let's think step by step.
columns: ['Name', 'Hospital_beds']  
sql: select Name, Hospital_beds from T

Table_title:Churnet Valley Railway 
Table_columns:  (Number, Name, Type, Livery, Status, Notes)
Question: how many locomotives are currently operational?
output: Let's think step by step.
columns: ['Name', 'Status']
sql: select Name, Status from T

Table_title: List of hospitals in North Carolina
Table_columns:  (Rank, Nation, Gold, Silver, Bronze, Total)
Question: who won the most gold medals?
output: Let's think step by step.
columns: ['Nation', 'Gold'] 
sql: select Nation, Gold from T

Table_title: 2012–13 Exeter City F.C. season
Table_columns:  (name, league, fa_cup, league_cup, jp_trophy, total)
Question: does pat or john have the highest total?
output: Let's think step by step.
columns: ['name', 'total']
sql: select name, total from T

Table_title: My Brother and Me
Table_columns:  (series_, season_, title, notes, original_air_date)
Question: alfie's birthday party aired on january 19. what was the airdate of the next episode?
output: Let's think step by step.
columns: ['title', 'season_', 'original_air_date']
sql: select title, season_, original_air_date from T

Table_title: The Harvest (Boondox album)  
Table_columns:  (_, title, time, lyrics, music, producers, performers)
Question: how many song come after "rollin hard"?
output: Let's think step by step.
columns: ['title', 'time']
sql: select title, time from T

Table_title: GameStorm.org
Table_columns:  (Iteration, Dates, Location, Attendance, Notes)
Question: what's the total attendance for gamestorm 11?
output: Let's think step by step.
columns: ['Attendance', 'Iteration']
sql: select Attendance, Iteration from T

Table_title: 1981 Iowa Hawkeyes football team 
Table_columns:  (Date, Opponent, Rank, Site, TV, Result, Attendance)
Question: which date had the most attendance?
output: Let's think step by step.
columns: ['Date', 'Attendance']
sql: select Date, Attendance from T

"""

p_row_col_wtq = """Generate SQL given the question and table for selecting the required rows and columns to answer the question correctly. 

Table_title: Marek Plawgo
Table_columns: ['Year', 'Competition', 'Venue', 'Position', 'Event', 'Notes']
Question: when was his first 1st place record?
output: Let's think step by step.
columns: ['Year',  'Position']
sql: select Year, Position from T where Position like '%1st%'

Table_title: 2013\u201314 Toros Mexico season
Table_columns: ['Game', 'Day', 'Date', 'Kickoff', 'Opponent', 'Results_Score', 'Results_Record', 'Location', 'Attendance']
Question: what was the number of people attending the toros mexico vs. monterrey flash game?
output: Let's think step by step.
columns: ['Attendance’, 'Opponent']
sql: select Opponent, Attendance from T where Opponent like '%monterrey flash%'

Table_title: Radhika Pandit
Table_columns:  ['Year', 'Film', 'Role', 'Language', 'Notes']
Question: what is the total number of films with the language of kannada listed?
output: Let's think step by step.
columns: ['Film', 'Language']
sql: select Film, Language from T where Language like '%kannada%'

Table_title: List of storms on the Great Lakes
Table_columns:  ['Ship', 'Type_of_Vessel', 'Lake', 'Location', 'Lives_lost']
Question: how many more ships were wrecked in lake huron than in erie?
output: Let's think step by step.
columns: ['Ship',  'Lake']
sql: SELECT Ship, Lake FROM T WHERE Lake LIKE '%Lake Huron%' or Lake LIKE '%Lake Erie%'

Table_title: List of hospitals in North Carolina
Table_columns:  ['Name', 'City', 'Hospital_beds', 'Operating_rooms', 'Total', 'Trauma_designation', 'Affiliation', 'Notes']
Question: what is the only hospital to have 6 hospital beds?
output: Let's think step by step.
columns: ['Name', 'Hospital_beds']  
sql: select Name, Hospital_beds from T where Hospital_beds = 6

Table_title:Churnet Valley Railway 
Table_columns:  ['Number', 'Name', 'Type', 'Livery', 'Status', 'Notes']
Question: how many locomotives are currently operational?
output: Let's think step by step.
columns: ['Name',  'Status']
sql: select Name, Status from T where Status like '%operational%'

Table_title: List of hospitals in North Carolina
Table_columns:  ['Rank', 'Nation', 'Gold', 'Silver', 'Bronze', 'Total']
Question: who won the most gold medals?
output: Let's think step by step.
columns: ['Nation', 'Gold'] 
sql: select Nation, Gold from T

Table_title: 2012–13 Exeter City F.C. season
Table_columns:  ['Name', 'League', 'FA_Cup', 'League_Cup', 'JP_Trophy', 'Total']
Question: does pat or john have the highest total?
output: Let's think step by step.
columns: ['Name', 'Total']
sql: select Name, Total from T where Name like '%pat%' or Name like '%john%'

Table_title: My Brother and Me
Table_columns:  ['Series_', 'Season_', 'Title', 'Notes', 'Original_air_date']
Question: alfie's birthday party aired on january 19. what was the airdate of the next episode?
output: Let's think step by step.
columns: ['Title', 'Season_', 'Original_air_date']
sql: select Title, Season_, Original_air_date from T

Table_title: The Harvest (Boondox album)  
Table_columns:  ['_', 'Title', 'Time', 'Lyrics', 'Music', 'Producers', 'Performers']
Question: how many song come after "rollin hard"?
output: Let's think step by step.
columns: ['Title', 'Time']
sql: select Title, Time from T

Table_title: GameStorm.org
Table_columns:  ['Iteration', 'Dates', 'Location', 'Attendance', 'Notes']
Question: what's the total attendance for gamestorm 11?
output: Let's think step by step.
columns: ['Attendance', 'Iteration']
sql: select Attendance, Iteration from T where Iteration like '%gamestorm 11%'

Table_title: 1981 Iowa Hawkeyes football team 
Table_columns:  ['Date', 'Opponent', 'Rank', 'Site', 'TV', 'Result', 'Attendance']
Question: which date had the most attendance?
output: Let's think step by step.
columns: ['Date', 'Attendance']
sql: select Date, Attendance from T

"""

p_col_three_wtq = """Generate SQL for selecting the required columns, given the question and table to answer the question correctly.
Do not use any where clause in the sql, simply select the correct columns to answer the question.

SQLite SQL tables, with their properties:

Table: Marek Plawgo (row_number,year,competition,venue,position,event,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | competition | venue | position | event | notes
0 | 1999 | european junior championships | riga, latvia | 4th | 400 m hurdles | 52.17
1 | 2000 | world junior championships | santiago, chile | 1st | 400 m hurdles | 49.23
2 | 2001 | world championships | edmonton, canada | 18th (sf) | 400 m hurdles | 49.8

Q: when was his first 1st place record?
SQL: select year, position from T;

SQLite SQL tables, with their properties:

Table: 2013\u201314 Toros Mexico season(row_number,game,day,date,kickoff,opponent,results_score,results_record,location,attendance)

3 example rows: 
 select * from T limit 3;
row_number | game | day | date | kickoff | opponent | results_score | results_record | location | attendance
0 | 1 | sunday | november 10 | t15:5 | at las vegas legends | l 3–7 | 0–1 | orleans arena | 1836
1 | 2 | sunday | november 17 | t13:5 | monterrey flash | l 6–10 | 0–2 | unisantos park | 363
2 | 3 | saturday | november 23 | t19:5 | at bay area rosal | w 10–7 | 1–2 | cabernet indoor sports | 652

Q: what was the number of people attending the toros mexico vs. monterrey flash game?
SQL: select attendance, opponent from T;

SQLite SQL tables, with their properties:

Table: Radhika Pandit(row_number,year,film,role,language,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | film | role | language | notes
0 | 2008 | moggina manasu | chanchala | kannada | filmfare award for best actress - kannada; karnataka state film award for best actress
1 | 2009 | olave jeevana lekkachaara | rukmini | kannada | innovative film award for best actress
2 | 2009 | love guru | kushi | kannada | filmfare award for best actress - kannada

Q: what is the total number of films with the language of kannada listed?
SQL: select film, language from T;

SQLite SQL tables, with their properties:

Table: List of storms on the Great Lakes(row_number,ship,type_of_vessel,lake,location,lives_lost)

3 example rows: 
 select * from T limit 3;
row_number | ship | type_of_vessel | lake | location | lives_lost
0 | argus | steamer | lake huron | 25 miles off kincardine, ontario | 25 lost
1 | james carruthers | steamer | lake huron | near kincardine | 18 lost
2 | hydrus | steamer | lake huron | near lexington, michigan | 28 lost

Q: how many more ships were wrecked in lake huron than in erie?
SQL: select ship, lake from T;

SQLite SQL tables, with their properties:

Table: Vidant Bertie Hospital(row_number,name,city,hospital_beds,operating_rooms,total,trauma_designation,affiliation,notes)

3 example rows: 
 select * from T limit 3;
row_number | name | city | hospital_beds | operating_rooms | total | trauma_designation | affiliation | notes
0 | alamance regional medical center | burlington | 238 | 15 | 253 | none | cone | none
1 | albemarle hospital | elizabeth city | 182 | 13 | 195 | none | vidant | none
2 | alexander hospital | hickory | 25 | 3 | 28 | none | none | none

Q: what is the only hospital to have 6 hospital beds?
SQL: select name, hospital_beds from T;

SQLite SQL tables, with their properties:

Table: Churnet Valley Railway(row_number,number,name,type,livery,status,notes)

3 example rows: 
 select * from T limit 3;
row_number | number | name | type | livery | status | notes
0 | none | brightside | yorkshire engine company 0-4-0 | black | under repair | currently dismantled for overhaul
1 | 6 | roger h. bennett | yorkshire engine company "janus" 0-6-0 | ncb blue | operational | ~
2 | d2334 | none | class 4 | green | under repair | stopped at 2012-9 diesel gala after failure

Q: how many locomotives are currently operational?
SQL: select name, status from T;

SQLite SQL tables, with their properties:

Table: 2012\u201313 Exeter City F.C. season(row_number,name,league,fa_cup,league_cup,jp_trophy,total)

3 example rows: 
 select * from T limit 3;
row_number | name | league | fa_cup | league_cup | jp_trophy | total
0 | scot bennett | 5 | 0 | 0 | 0 | 5
1 | danny coles | 3 | 0 | 0 | 0 | 3
2 | liam sercombe | 1 | 0 | 0 | 0 | 1

Q: does pat or john have the highest total?
SQL: select name, total from T;

SQLite SQL tables, with their properties:

Table: The Harvest (Boondox album)(row_number, _, title, time, lyrics, music, producers, performers)

3 example rows: 
 select * from T limit 3;
row_number | _ | title | time | lyrics | music | producers | performers
0 | 1 | "intro" | 1:16 | none | none | none | none
1 | 2 | "7" | 3:30 | boondox | mike e. clark | boondox | boondox
2 | 3 | "out here" | 3:18 | boondox | mike e. clark; tino grosse | boondox | boondox

Q: how many song come after "rollin hard"?
SQL: select row_number, title from T;

SQLite SQL tables, with their properties:

Table: GameStorm.org(row_number, iteration, dates, location, attendance, notes)

3 example rows: 
 select * from T limit 3;
row_number | iteration | dates | location | attendance | notes
0 | gamestorm 10 | 2008-3 | red lion - vancouver, wa | 750 | none
1 | gamestorm 11 | (2009-3-262009-3-29,p3d) | hilton - vancouver, wa | 736 | debut of video games, first-ever artist guest of honor, rob alexander
2 | gamestorm 12 | (2010-3-252010-3-28,p3d) | hilton - vancouver, wa | 802 | board games guest of honor: tom lehmann

Q: what's the total attendance for gamestorm 11?
SQL: select attendance, iteration from T;


SQLite SQL tables, with their properties:

Table: 1981 Iowa Hawkeyes football team(row_number, date, opponent_, rank_, site, tv, result, attendance)

3 example rows: 
 select * from T limit 3;
row_number | date | opponent_ | rank_ | site | tv | result | attendance
0 | september 12 | #7 nebraska* | none | kinnick stadium • iowa city, ia | none | w 10-7 | 60160
1 | september 19 | at iowa state* | none | cyclone stadium • ames, ia (cy-hawk trophy) | none | l 12-23 | 53922
2 | september 26 | #6 ucla* | none | kinnick stadium • iowa city, ia | none | w 20-7 | 60004

Q: which date had the most attendance?
SQL: select date, attendance from T;


"""

p_row_three_wtq = """Generate SQL for selecting the required rows, given the question and table to answer the question correctly.

SQLite SQL tables, with their properties:

Table: Marek Plawgo (row_number,year,competition,venue,position,event,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | competition | venue | position | event | notes
0 | 1999 | european junior championships | riga, latvia | 4th | 400 m hurdles | 52.17
1 | 2000 | world junior championships | santiago, chile | 1st | 400 m hurdles | 49.23
2 | 2001 | world championships | edmonton, canada | 18th (sf) | 400 m hurdles | 49.8

Q: when was his first 1st place record?
SQL: select * from T where position = '1st' order by year asc limit 1

SQLite SQL tables, with their properties:

Table: 2013\u201314 Toros Mexico season(row_number,game,day,date,kickoff,opponent,results_score,results_record,location,attendance)

3 example rows: 
 select * from T limit 3;
row_number | game | day | date | kickoff | opponent | results_score | results_record | location | attendance
0 | 1 | sunday | november 10 | t15:5 | at las vegas legends | l 3–7 | 0–1 | orleans arena | 1836
1 | 2 | sunday | november 17 | t13:5 | monterrey flash | l 6–10 | 0–2 | unisantos park | 363
2 | 3 | saturday | november 23 | t19:5 | at bay area rosal | w 10–7 | 1–2 | cabernet indoor sports | 652

Q: what was the number of people attending the toros mexico vs. monterrey flash game?
SQL: select * from T where opponent like '%monterrey flash%'

SQLite SQL tables, with their properties:

Table: Radhika Pandit T(row_number,year,film,role,language,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | film | role | language | notes
0 | 2008 | moggina manasu | chanchala | kannada | filmfare award for best actress - kannada; karnataka state film award for best actress
1 | 2009 | olave jeevana lekkachaara | rukmini | kannada | innovative film award for best actress
2 | 2009 | love guru | kushi | kannada | filmfare award for best actress - kannada

Q: what is the total number of films with the language of kannada listed?
SQL: select * from T where language like '%kannada%'

SQLite SQL tables, with their properties:

Table: T(row_number,ship,type_of_vessel,lake,location,lives_lost)

3 example rows: 
 select * from T limit 3;
row_number | ship | type_of_vessel | lake | location | lives_lost
0 | argus | steamer | lake huron | 25 miles off kincardine, ontario | 25 lost
1 | james carruthers | steamer | lake huron | near kincardine | 18 lost
2 | hydrus | steamer | lake huron | near lexington, michigan | 28 lost

Q: how many more ships were wrecked in lake huron than in erie?
SQL: select * from T where lake like '%lake huron%' and lake like '%lake erie%'

SQLite SQL tables, with their properties:

Table: T(row_number,name,city,hospital_beds,operating_rooms,total,trauma_designation,affiliation,notes)

3 example rows: 
 select * from T limit 3;
row_number | name | city | hospital_beds | operating_rooms | total | trauma_designation | affiliation | notes
0 | alamance regional medical center | burlington | 238 | 15 | 253 | none | cone | none
1 | albemarle hospital | elizabeth city | 182 | 13 | 195 | none | vidant | none
2 | alexander hospital | hickory | 25 | 3 | 28 | none | none | none

Q: what is the only hospital to have 6 hospital beds?
SQL: select * from T where hospital_beds = 6

SQLite SQL tables, with their properties:

Table: T(row_number,number,name,type,livery,status,notes)

3 example rows: 
 select * from T limit 3;
row_number | number | name | type | livery | status | notes
0 | none | brightside | yorkshire engine company 0-4-0 | black | under repair | currently dismantled for overhaul
1 | 6 | roger h. bennett | yorkshire engine company "janus" 0-6-0 | ncb blue | operational | ~
2 | d2334 | none | class 4 | green | under repair | stopped at 2012-9 diesel gala after failure
Q: how many locomotives are currently operational?
SQL: select * from T where status = 'operational'

SQLite SQL tables, with their properties:

Table: T(row_number,name,league,fa_cup,league_cup,jp_trophy,total)

3 example rows: 
 select * from T limit 3;
row_number | name | league | fa_cup | league_cup | jp_trophy | total
0 | scot bennett | 5 | 0 | 0 | 0 | 5
1 | danny coles | 3 | 0 | 0 | 0 | 3
2 | liam sercombe | 1 | 0 | 0 | 0 | 1

Q: does pat or john have the highest total?
SQL: select * from T where name like '%pat%' or name like '%john%' order by total desc limit 1

SQLite SQL tables, with their properties:

Table: T(row_number, _, title, time, lyrics, music, producers, performers)

3 example rows: 
 select * from T limit 3;
row_number | _ | title | time | lyrics | music | producers | performers
0 | 1 | "intro" | 1:16 | none | none | none | none
1 | 2 | "7" | 3:30 | boondox | mike e. clark | boondox | boondox
2 | 3 | "out here" | 3:18 | boondox | mike e. clark; tino grosse | boondox | boondox

Q: how many song come after "rollin hard"?
SQL: select * from T where row_number > (select row_number from T where title like '%rollin hard%')

SQLite SQL tables, with their properties:

Table: T(row_number, iteration, dates, location, attendance, notes)

3 example rows: 
 select * from T limit 3;
row_number | iteration | dates | location | attendance | notes
0 | gamestorm 10 | 2008-3 | red lion - vancouver, wa | 750 | none
1 | gamestorm 11 | (2009-3-262009-3-29,p3d) | hilton - vancouver, wa | 736 | debut of video games, first-ever artist guest of honor, rob alexander
2 | gamestorm 12 | (2010-3-252010-3-28,p3d) | hilton - vancouver, wa | 802 | board games guest of honor: tom lehmann

Q: what's the total attendance for gamestorm 11?
SQL: select * from T where iteration = 'gamestorm 11'


SQLite SQL tables, with their properties:

Table: T(row_number, date, opponent_, rank_, site, tv, result, attendance)

3 example rows: 
 select * from T limit 3;
row_number | date | opponent_ | rank_ | site | tv | result | attendance
0 | september 12 | #7 nebraska* | none | kinnick stadium • iowa city, ia | none | w 10-7 | 60160
1 | september 19 | at iowa state* | none | cyclone stadium • ames, ia (cy-hawk trophy) | none | l 12-23 | 53922
2 | september 26 | #6 ucla* | none | kinnick stadium • iowa city, ia | none | w 20-7 | 60004

Q: which date had the most attendance?
SQL: select * from T order by attendance desc limit 1

"""

p_sql_three_wtq = """Generate SQL with no explanation given the question and table to answer the question correctly.

SQLite table properties:

Table: Marek Plawgo(row_number,year,competition,venue,position,event,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | competition | venue | position | event | notes
0 | 1999 | european junior championships | riga, latvia | 4th | 400 m hurdles | 52.17
1 | 2000 | world junior championships | santiago, chile | 1st | 400 m hurdles | 49.23
2 | 2001 | world championships | edmonton, canada | 18th (sf) | 400 m hurdles | 49.8

Q: when was his first 1st place record?
SQL: select year from T where position = '1st' order by year asc limit 1

SQLite table properties:

Table: 2013\u201314 Toros Mexico season(row_number,game,day,date,kickoff,opponent,results_score,results_record,location,attendance)

3 example rows: 
 select * from T limit 3;
row_number | game | day | date | kickoff | opponent | results_score | results_record | location | attendance
0 | 1 | sunday | november 10 | t15:5 | at las vegas legends | l 3–7 | 0–1 | orleans arena | 1836
1 | 2 | sunday | november 17 | t13:5 | monterrey flash | l 6–10 | 0–2 | unisantos park | 363
2 | 3 | saturday | november 23 | t19:5 | at bay area rosal | w 10–7 | 1–2 | cabernet indoor sports | 652

Q: what was the number of people attending the toros mexico vs. monterrey flash game?
SQL: select attendance from T where opponent like '%monterrey flash%'

SQLite table properties:

Table: Radhika Pandit(row_number,year,film,role,language,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | film | role | language | notes
0 | 2008 | moggina manasu | chanchala | kannada | filmfare award for best actress - kannada; karnataka state film award for best actress
1 | 2009 | olave jeevana lekkachaara | rukmini | kannada | innovative film award for best actress
2 | 2009 | love guru | kushi | kannada | filmfare award for best actress - kannada

Q: what is the total number of films with the language of kannada listed?
SQL: select count(film) from T where language like '%kannada%'

SQLite table properties:

Table: List of storms on the Great Lakes(row_number,ship,type_of_vessel,lake,location,lives_lost)

3 example rows: 
 select * from T limit 3;
row_number | ship | type_of_vessel | lake | location | lives_lost
0 | argus | steamer | lake huron | 25 miles off kincardine, ontario | 25 lost
1 | james carruthers | steamer | lake huron | near kincardine | 18 lost
2 | hydrus | steamer | lake huron | near lexington, michigan | 28 lost

Q: how many more ships were wrecked in lake huron than in erie?
SQL: select ((select count(ship) from T where lake like '%lake huron%') - (select count(ship) from T where lake like '%lake erie%'))

SQLite table properties:

Table: Vidant Bertie Hospital(row_number,name,city,hospital_beds,operating_rooms,total,trauma_designation,affiliation,notes)

3 example rows: 
 select * from T limit 3;
row_number | name | city | hospital_beds | operating_rooms | total | trauma_designation | affiliation | notes
0 | alamance regional medical center | burlington | 238 | 15 | 253 | none | cone | none
1 | albemarle hospital | elizabeth city | 182 | 13 | 195 | none | vidant | none
2 | alexander hospital | hickory | 25 | 3 | 28 | none | none | none

Q: what is the only hospital to have 6 hospital beds?
SQL: select name from T where hospital_beds = 6

SQLite table properties:

Table: Churnet Valley Railway(row_number,number,name,type,livery,status,notes)

3 example rows: 
 select * from T limit 3;
row_number | number | name | type | livery | status | notes
0 | none | brightside | yorkshire engine company 0-4-0 | black | under repair | currently dismantled for overhaul
1 | 6 | roger h. bennett | yorkshire engine company "janus" 0-6-0 | ncb blue | operational | ~
2 | d2334 | none | class 4 | green | under repair | stopped at 2012-9 diesel gala after failure

Q: how many locomotives are currently operational?
SQL: select count(*) from T where status = 'operational'

SQLite table properties:

Table: 2012\u201313 Exeter City F.C. season(row_number,name,league,fa_cup,league_cup,jp_trophy,total)

3 example rows: 
 select * from T limit 3;
row_number | name | league | fa_cup | league_cup | jp_trophy | total
0 | scot bennett | 5 | 0 | 0 | 0 | 5
1 | danny coles | 3 | 0 | 0 | 0 | 3
2 | liam sercombe | 1 | 0 | 0 | 0 | 1

Q: does pat or john have the highest total?
SQL: select name from T where name like '%pat%' or name like '%john%' order by total desc limit 1

SQLite table properties:

Table: The Harvest (Boondox album)(row_number, _, title, time, lyrics, music, producers, performers)

3 example rows: 
 select * from T limit 3;
row_number | _ | title | time | lyrics | music | producers | performers
0 | 1 | "intro" | 1:16 | none | none | none | none
1 | 2 | "7" | 3:30 | boondox | mike e. clark | boondox | boondox
2 | 3 | "out here" | 3:18 | boondox | mike e. clark; tino grosse | boondox | boondox

Q: how many song come after "rollin hard"?
SQL: select count(*) from T where row_number > (select row_number from T where title like '%rollin hard%')

SQLite table properties:

Table: GameStorm.org(row_number, iteration, dates, location, attendance, notes)

3 example rows: 
 select * from T limit 3;
row_number | iteration | dates | location | attendance | notes
0 | gamestorm 10 | 2008-3 | red lion - vancouver, wa | 750 | none
1 | gamestorm 11 | (2009-3-262009-3-29,p3d) | hilton - vancouver, wa | 736 | debut of video games, first-ever artist guest of honor, rob alexander
2 | gamestorm 12 | (2010-3-252010-3-28,p3d) | hilton - vancouver, wa | 802 | board games guest of honor: tom lehmann

Q: what's the total attendance for gamestorm 11?
SQL: select attendance from T where iteration = 'gamestorm 11'


SQLite table properties:

Table: 1981 Iowa Hawkeyes football team(row_number, date, opponent_, rank_, site, tv, result, attendance)

3 example rows: 
 select * from T limit 3;
row_number | date | opponent_ | rank_ | site | tv | result | attendance
0 | september 12 | #7 nebraska* | none | kinnick stadium • iowa city, ia | none | w 10-7 | 60160
1 | september 19 | at iowa state* | none | cyclone stadium • ames, ia (cy-hawk trophy) | none | l 12-23 | 53922
2 | september 26 | #6 ucla* | none | kinnick stadium • iowa city, ia | none | w 20-7 | 60004

Q: which date had the most attendance?
SQL: select date from T order by attendance desc limit 1

"""

p_rc_three_wtq = """Generate SQL for selecting the required rows and columns, given the question and table to answer the question correctly.
SQLite table properties:

Table: Marek Plawgo (row_number,year,competition,venue,position,event,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | competition | venue | position | event | notes
0 | 1999 | european junior championships | riga, latvia | 4th | 400 m hurdles | 52.17
1 | 2000 | world junior championships | santiago, chile | 1st | 400 m hurdles | 49.23
2 | 2001 | world championships | edmonton, canada | 18th (sf) | 400 m hurdles | 49.8

Q: when was his first 1st place record?
SQL: select year from T where position = '1st' order by year asc limit 1

SQLite table properties:

Table: 2013\u201314 Toros Mexico season(row_number,game,day,date,kickoff,opponent,results_score,results_record,location,attendance)

3 example rows: 
 select * from T limit 3;
row_number | game | day | date | kickoff | opponent | results_score | results_record | location | attendance
0 | 1 | sunday | november 10 | t15:5 | at las vegas legends | l 3–7 | 0–1 | orleans arena | 1836
1 | 2 | sunday | november 17 | t13:5 | monterrey flash | l 6–10 | 0–2 | unisantos park | 363
2 | 3 | saturday | november 23 | t19:5 | at bay area rosal | w 10–7 | 1–2 | cabernet indoor sports | 652

Q: what was the number of people attending the toros mexico vs. monterrey flash game?
SQL: select attendance from T where opponent like '%monterrey flash%'

SQLite table properties:

Table: Radhika Pandit(row_number,year,film,role,language,notes)

3 example rows: 
 select * from T limit 3;
row_number | year | film | role | language | notes
0 | 2008 | moggina manasu | chanchala | kannada | filmfare award for best actress - kannada; karnataka state film award for best actress
1 | 2009 | olave jeevana lekkachaara | rukmini | kannada | innovative film award for best actress
2 | 2009 | love guru | kushi | kannada | filmfare award for best actress - kannada

Q: what is the total number of films with the language of kannada listed?
SQL: select film, language from T where language like '%kannada%'

SQLite table properties:

Table: List of storms on the Great Lakes(row_number,ship,type_of_vessel,lake,location,lives_lost)

3 example rows: 
 select * from T limit 3;
row_number | ship | type_of_vessel | lake | location | lives_lost
0 | argus | steamer | lake huron | 25 miles off kincardine, ontario | 25 lost
1 | james carruthers | steamer | lake huron | near kincardine | 18 lost
2 | hydrus | steamer | lake huron | near lexington, michigan | 28 lost

Q: how many more ships were wrecked in lake huron than in erie?
SQL: select ship, lake from T where lake like '%lake huron%' or lake like '%lake erie%'

SQLite table properties:

Table: Vidant Bertie Hospital(row_number,name,city,hospital_beds,operating_rooms,total,trauma_designation,affiliation,notes)

3 example rows: 
 select * from T limit 3;
row_number | name | city | hospital_beds | operating_rooms | total | trauma_designation | affiliation | notes
0 | alamance regional medical center | burlington | 238 | 15 | 253 | none | cone | none
1 | albemarle hospital | elizabeth city | 182 | 13 | 195 | none | vidant | none
2 | alexander hospital | hickory | 25 | 3 | 28 | none | none | none

Q: what is the only hospital to have 6 hospital beds?
SQL: select name, hospital_beds from T where hospital_beds = 6

SQLite table properties:

Table: Churnet Valley Railway(row_number,number,name,type,livery,status,notes)

3 example rows: 
 select * from T limit 3;
row_number | number | name | type | livery | status | notes
0 | none | brightside | yorkshire engine company 0-4-0 | black | under repair | currently dismantled for overhaul
1 | 6 | roger h. bennett | yorkshire engine company "janus" 0-6-0 | ncb blue | operational | ~
2 | d2334 | none | class 4 | green | under repair | stopped at 2012-9 diesel gala after failure

Q: how many locomotives are currently operational?
SQL: select name, status from T where status = 'operational'

SQLite table properties:

Table: 2012\u201313 Exeter City F.C. season(row_number,name,league,fa_cup,league_cup,jp_trophy,total)

3 example rows: 
 select * from T limit 3;
row_number | name | league | fa_cup | league_cup | jp_trophy | total
0 | scot bennett | 5 | 0 | 0 | 0 | 5
1 | danny coles | 3 | 0 | 0 | 0 | 3
2 | liam sercombe | 1 | 0 | 0 | 0 | 1

Q: does pat or john have the highest total?
SQL: select name, total from T where name like '%pat%' or name like '%john%'

SQLite table properties:

Table: The Harvest (Boondox album)(row_number, _, title, time, lyrics, music, producers, performers)

3 example rows: 
 select * from T limit 3;
row_number | _ | title | time | lyrics | music | producers | performers
0 | 1 | "intro" | 1:16 | none | none | none | none
1 | 2 | "7" | 3:30 | boondox | mike e. clark | boondox | boondox
2 | 3 | "out here" | 3:18 | boondox | mike e. clark; tino grosse | boondox | boondox

Q: how many song come after "rollin hard"?
SQL: select count(*) from T where row_number > (select row_number from T where title like '%rollin hard%')

SQLite table properties:

Table: GameStorm.org(row_number, iteration, dates, location, attendance, notes)

3 example rows: 
 select * from T limit 3;
row_number | iteration | dates | location | attendance | notes
0 | gamestorm 10 | 2008-3 | red lion - vancouver, wa | 750 | none
1 | gamestorm 11 | (2009-3-262009-3-29,p3d) | hilton - vancouver, wa | 736 | debut of video games, first-ever artist guest of honor, rob alexander
2 | gamestorm 12 | (2010-3-252010-3-28,p3d) | hilton - vancouver, wa | 802 | board games guest of honor: tom lehmann

Q: what's the total attendance for gamestorm 11?
SQL: select attendance, iteration from T where iteration = 'gamestorm 11'


SQLite table properties:

Table: 1981 Iowa Hawkeyes football team(row_number, date, opponent_, rank_, site, tv, result, attendance)

3 example rows: 
 select * from T limit 3;
row_number | date | opponent_ | rank_ | site | tv | result | attendance
0 | september 12 | #7 nebraska* | none | kinnick stadium • iowa city, ia | none | w 10-7 | 60160
1 | september 19 | at iowa state* | none | cyclone stadium • ames, ia (cy-hawk trophy) | none | l 12-23 | 53922
2 | september 26 | #6 ucla* | none | kinnick stadium • iowa city, ia | none | w 20-7 | 60004

Q: which date had the most attendance?
SQL: select date, attendance from T order by attendance desc

"""

# ---------------------------------------------------------------

def truncate_tokens(prompt,  max_length) -> str:
    """Truncates a text string based on max number of tokens."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded_string = encoding.encode(prompt)
    num_tokens = len(encoded_string)

    if num_tokens > max_length:
        prompt = encoding.decode(encoded_string[:max_length])
        print('truncated -->  ', num_tokens)
    return prompt

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7, n=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
        stream=False,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Table:", "\n\n\n"]
    )
    return response.choices[0].message.content

# -------------------------------------------------------------------------
def gen_table_decom_prompt(title, tab_col, question, examples, selection='rc'):
    if selection == 'col':
        prompt = "" + p_col_three_wtq
    elif selection == 'row':
        prompt = "" + p_row_three_wtq
    elif selection == 'rc':
        prompt = "" + p_rc_three_wtq
    elif selection == 'sql':
        prompt = "" + p_sql_three_wtq
    prompt += "\nSQLite table properties:\n\n"
    prompt += "Table: " + title + " (" + str(tab_col) + ")" + "\n\n"
    prompt += "3 example rows: \n select * from T limit 3;\n"
    prompt += examples + "\n\n"
    prompt += "Q: " + question + "\n"
    prompt += "SQL:"
    return prompt

def generate_sql_answer_prompt(title, sql,  table, question):
    table = truncate_tokens(table, max_length=3000)

    prompt = p_sql_answer_wtq
    prompt += "\nTable_title: " + title
    prompt += "\nSQL: " + sql
    prompt += "\n\n" + table
    prompt += "\nQuestion: " + question
    prompt += "\nA: To find the answer to this question, let’s think step by step."

    return prompt

def get_sql_3(prompt):
    response = None
    while response is None:
        try:
            response = get_completion(prompt, temperature=0)
        except:
            time.sleep(2)
            pass
    return response

def gen_full_table_prompt(title, tab_col, table, question):
    table = truncate_tokens(table, max_length=2000)

    prompt = p_wtq_full
    prompt += "Table: " + title + " (" + str(tab_col) + ")" + "\n\n"
    prompt += table + "\nQuestion: " + question
    prompt += "\nA: To find the answer to this question, let’s think step by step."

    return prompt

def get_answer(promt):
    response = None
    while response is None:
        try:

            response = get_completion(promt, temperature=0.7)
            # print('Generated ans------>: ', response)
        except:
            # print('sleep')
            time.sleep(2)
            pass

    return response

# --------------------------------------------------------------------------