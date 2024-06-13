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

p_fetaqa_full = """
Read the following table regarding "Shagun Sharma" to answer the given question.

Year | Title | Role | Channel
2015 | Kuch Toh Hai Tere Mere Darmiyaan | Sanjana Kapoor | Star Plus
2016 | Kuch Rang Pyar Ke Aise Bhi | Khushi | Sony TV
2016 | Gangaa | Aashi Jhaa | &TV
2017 | Iss Pyaar Ko Kya Naam Doon 3 | Meghna Narayan Vashishth | Star Plus
2017–18 | Tu Aashiqui | Richa Dhanrajgir | Colors TV
2019 | Laal Ishq | Pernia | &TV
2019 | Vikram Betaal Ki Rahasya Gatha | Rukmani/Kashi | &TV
2019 | Shaadi Ke Siyape | Dua | &TV

Question: What TV shows was Shagun Sharma seen in 2019?
Answer: In 2019, Shagun Sharma played in the roles as Pernia in Laal Ishq, Vikram Betaal Ki Rahasya Gatha as Rukmani/Kashi and Shaadi Ke Siyape as Dua.

Read the following table regarding "German submarine U-438" to answer the given question.

 Date | Name | Nationality | Tonnage (GRT) | Fate
10 August 1942 | Condylis | Greece | 4,439 | Sunk
10 August 1942 | Oregon | United Kingdom | 6,008 | Sunk
25 August 1942 | Trolla | Norway | 1,598 | Sunk
2 November 1942 | Hartington | United Kingdom | 5,496 | Damaged

Question: How much overall damage did the German submarine U-438 cause?
Answer: The U-438 sank three ships, totalling 12,045 gross register tons (GRT) and damaged one ship totalling 5,496 GRT.

"""

p_answer_fetaqa = """Based on the table information bellow, find the answer to the given question correctly. 

Table_title: Shagun Sharma
Table:
Year | Title | Role | Channel
2015 | Kuch Toh Hai Tere Mere Darmiyaan | Sanjana Kapoor | Star Plus
2016 | Kuch Rang Pyar Ke Aise Bhi | Khushi | Sony TV
2016 | Gangaa | Aashi Jhaa | &TV
2017 | Iss Pyaar Ko Kya Naam Doon 3 | Meghna Narayan Vashishth | Star Plus
2017–18 | Tu Aashiqui | Richa Dhanrajgir | Colors TV
2019 | Laal Ishq | Pernia | &TV
2019 | Vikram Betaal Ki Rahasya Gatha | Rukmani/Kashi | &TV
2019 | Shaadi Ke Siyape | Dua | &TV

Question: What TV shows was Shagun Sharma seen in 2019?
Answer: In 2019, Shagun Sharma played in the roles as Pernia in Laal Ishq, Vikram Betaal Ki Rahasya Gatha as Rukmani/Kashi and Shaadi Ke Siyape as Dua.

Table_title: German submarine U-438
Table:
 Date | Name | Nationality | Tonnage (GRT) | Fate
10 August 1942 | Condylis | Greece | 4,439 | Sunk
10 August 1942 | Oregon | United Kingdom | 6,008 | Sunk
25 August 1942 | Trolla | Norway | 1,598 | Sunk
2 November 1942 | Hartington | United Kingdom | 5,496 | Damaged

Question: How much overall damage did the German submarine U-438 cause?
Answer: The U-438 sank three ships, totalling 12,045 gross register tons (GRT) and damaged one ship totalling 5,496 GRT.

Table_title: LVL IV
SQL: select chart, peak_position, year from T where chart = "billboard 200" or chart = "top heatseekers";

chart | peak_position | year
billboard 200 | 153 | 2004
top heatseekers | 4 | 2004

Question: How did LVL IV do in Billboard 200 and Top Heatseekers?
Answer: lvl iv peaked on the billboard 200 at #153 and reached #4 on top heatseekers.
"""

p_sql_answer_fetaqa = """Based on the table title and excecution result of the sql query bellow, find the answer to the given question correctly. 

Table_title: Shagun Sharma
SQL: select title, year from T where year = 2019

title | year
laal ishq | 2019
vikram betaal ki rahasya gatha | 2019
shaadi ke siyape | 2019

Question: What TV shows was Shagun Sharma seen in 2019?
Answer: in 2019, shagun sharma played in the roles as pernia in laal ishq, vikram betaal ki rahasya gatha as rukmani/kashi and shaadi ke siyape as dua.

Table_title: 1975 North Vietnamese legislative election
SQL: select party, seats from T

party | seats
vietnamese fatherland front | 424
invalid/blank votes | –
total | 424
source: ipu | source: ipu

Question: What were the voting results of the 1975 North Vietnamese legislative election with regards to seats?
Answer: in the 1975 north vietnamese legislative election, the vietnamese fatherland front won all 424 seats.

Table_title: List of 2009 World Games medal winners
SQL: select * from T where gold like '%Huang Yu-ting%' or silver like '%Huang Yu-ting%' or bronze like '%Huang Yu-ting%'

row_number | event | gold | silver | bronze
6 | women's 300 m time trial | huang yu-ting, chinese taipei | hsu chiao-jen, chinese taipei | lim jin-seon, south korea
7 | women's 500 m sprint | huang yu-ting, chinese taipei | lim jin-seon, south korea | jercy puello, colombia
8 | women's 1000 m sprint | huang yu-ting, chinese taipei | hsu chiao-jen, chinese taipei | nicole begg, new zealand

Question: How's Huang Yu-ting doing in the 2009 World Games?
Answer: as an inline speed skater, huang won three gold medals at the 2009 world games in chinese taipei: 300 m time trial, 500 m sprint, and 1000 m sprint.

Table_title: Khiranwali
SQL: select * from T

row_number | particulars | total | male | female
0 | total no. of houses | 206 | none | none
1 | population | 1041 | 530 | 511
2 | child (0-6) | 106 | 67 | 39
3 | schedule caste | 337 | 176 | 161
4 | schedule tribe | 0 | 0 | 0
5 | literacy | 73.58 % | 77.32 % | 69.92 %
6 | total workers | 303 | 285 | 18
7 | main worker | 253 | 0 | 0
8 | marginal worker | 50 | 46 | 4

Question: What is Khiranwali's total number of houses and populations including male and female?
Answer: khiranwali has total number of 206 houses and a population of 1,041 of which 530 are males and 511 are females.

Table_title: Delroy Poyser
SQL: select year, competition, venue from T where event = 'long jump' and position = '1st' and competition like '%central american and caribbean games%'

year | competition | venue
1982 | central american and caribbean games | havana, cuba

Question: When did Delroy Poyser earn his first Central American and Carribean Games gold medal in the Long Jump, and where did the competition take place?
Answer: delroy poyser, a jamaican, won the gold medal at the 1982 central american and caribbean games in havana, cuba.

Table_title: Tanc Sade
SQL: select title, year from T where year between 2007 and 2014

title | year
csi: miami | 2007
csi: ny | 2007
90210 | 2008
the strip | 2008
the mentalist | 2010
body of proof | 2012
sons of anarchy | 2014
matador | 2014

Question: What shows did Sade star in from 2007-2014?
Answer: sade starred in csi: miami (2007), sons of anarchy (2014), the mentalist (2010), body of proof (2012), 90210 (2008), and csi: ny (2007), and matador, the strip (2008).
"""

p_col_fetaqa = """Generate SQL given the question and table for selecting the required columns to answer the question correctly.

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

p_row_col_fetaqa = """Generate SQL given the question and table for selecting the required rows and columns to answer the question correctly. 

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

p_col_three_fetaqa = """Generate SQL for selecting the required columns, given the question and table to answer the question correctly.
Do not use any where clause in the sql, simply select the correct columns to answer the question. 

SQLite table properties:

Table: Tanc Sade(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | young lions | steve | "the city and the taxi driver"
1 | 2002 | don't blame me | nigel | "liar liar"
2 | 2003 | white collar blue | karl baumann | "1.18"

Q: What shows did Sade star in from 2007-2014?
SQL: select title, year from T;

SQLite table properties:

Table: Rodney Crowell(row_number, Year, Nominated_work, Award, Result)

3 example rows: 
 select * from T limit 3;
row_number | year | nominated_work | award | result
0 | 1986 | "i don't know why you don't want me" (with rosanne cash) | best country song | nominated
1 | 1989 | "i couldn't leave you if i tried" | best country song | nominated
2 | 1990 | "after all this time" | best country song | won

Q: What awards did Rodney Crowell win in his career?
SQL: select year, award, nominated_work, result from T; 

SQLite table properties:

Table: Kristian Schmid(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | scooby-doo | brad | none
1 | 2002 | blurred | danny | none
2 | 2005 | the great raid | cpl. lee | none

Q: What roles did Schmid play in 2002?
SQL: select title, role, year from T; 

SQLite table properties:

Table: LVL IV(row_number, Chart, Peak_position, Year)

3 example rows: 
 select * from T limit 3;
row_number | chart | peak_position | year
0 | billboard 200 | 153 | 2004
1 | top heatseekers | 4 | 2004

Q: How did LVL IV do in Billboard 200 and Top Heatseekers?
SQL: select chart, peak_position, year from T;

SQLite table properties:

Table: Sandy Dennis(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 1961 | splendor in the grass | kay | none
1 | 1966 | who's afraid of virginia woolf? | honey | academy award
2 | 1966 | the 3 sisters | irina | none

Q: What roles did Sandy Dennis have in 1986, 1988, and 1989?
SQL: select title, role, year from T; 
"""

p_row_three_fetaqa = """Generate SQL for selecting the required rows, given the question and table to answer the question correctly.

SQLite table properties:

Table: Tanc Sade(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | young lions | steve | "the city and the taxi driver"
1 | 2002 | don't blame me | nigel | "liar liar"
2 | 2003 | white collar blue | karl baumann | "1.18"

Q: What shows did Sade star in from 2007-2014?
SQL: select * from T where year between 2007 and 2014;

SQLite table properties:

Table: Rodney Crowell(row_number, Year, Nominated_work, Award, Result)

3 example rows: 
 select * from T limit 3;
row_number | year | nominated_work | award | result
0 | 1986 | "i don't know why you don't want me" (with rosanne cash) | best country song | nominated
1 | 1989 | "i couldn't leave you if i tried" | best country song | nominated
2 | 1990 | "after all this time" | best country song | won

Q: What awards did Rodney Crowell win in his career?
SQL: select * from T where result = "won"; 

SQLite table properties:

Table: Kristian Schmid(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | scooby-doo | brad | none
1 | 2002 | blurred | danny | none
2 | 2005 | the great raid | cpl. lee | none

Q: What roles did Schmid play in 2002?
SQL: select * from T where year = 2002; 

SQLite table properties:

Table: LVL IV(row_number, Chart, Peak_position, Year)

3 example rows: 
 select * from T limit 3;
row_number | chart | peak_position | year
0 | billboard 200 | 153 | 2004
1 | top heatseekers | 4 | 2004

Q: How did LVL IV do in Billboard 200 and Top Heatseekers?
SQL: select * from T where chart = "billboard 200" or chart = "top heatseekers";

SQLite table properties:

Table: Sandy Dennis(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 1961 | splendor in the grass | kay | none
1 | 1966 | who's afraid of virginia woolf? | honey | academy award 
2 | 1966 | the 3 sisters | irina | none

Q: What roles did Sandy Dennis have in 1986, 1988, and 1989?
SQL: select * from T where year in (1986, 1988, 1989); 
"""

p_rc_three_fetaqa = """Generate SQL for selecting the required rows and columns, given the question and table to answer the question correctly.

SQLite table properties:

Table: Tanc Sade(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | young lions | steve | "the city and the taxi driver"
1 | 2002 | don't blame me | nigel | "liar liar"
2 | 2003 | white collar blue | karl baumann | "1.18"

Q: What shows did Sade star in from 2007-2014?
SQL: select title, year from T where year between 2007 and 2014;

SQLite table properties:

Table: Rodney Crowell(row_number, Year, Nominated_work, Award, Result)

3 example rows: 
 select * from T limit 3;
row_number | year | nominated_work | award | result
0 | 1986 | "i don't know why you don't want me" (with rosanne cash) | best country song | nominated
1 | 1989 | "i couldn't leave you if i tried" | best country song | nominated
2 | 1990 | "after all this time" | best country song | won

Q: What awards did Rodney Crowell win in his career?
SQL: select year, award, nominated_work from T where result = "won"; 

SQLite table properties:

Table: Kristian Schmid(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 2002 | scooby-doo | brad | none
1 | 2002 | blurred | danny | none
2 | 2005 | the great raid | cpl. lee | none

Q: What roles did Schmid play in 2002?
SQL: select title, role from T where year = 2002; 

SQLite table properties:

Table: LVL IV(row_number, Chart, Peak_position, Year)

3 example rows: 
 select * from T limit 3;
row_number | chart | peak_position | year
0 | billboard 200 | 153 | 2004
1 | top heatseekers | 4 | 2004

Q: How did LVL IV do in Billboard 200 and Top Heatseekers?
SQL: select chart, peak_position, year from T where chart = "billboard 200" or chart = "top heatseekers"; 

SQLite table properties:

Table: Sandy Dennis(row_number, Year, Title, Role, Notes)

3 example rows: 
 select * from T limit 3;
row_number | year | title | role | notes
0 | 1961 | splendor in the grass | kay | none
1 | 1966 | who's afraid of virginia woolf? | honey | academy award 
2 | 1966 | the 3 sisters | irina | none

Q: What roles did Sandy Dennis have in 1986, 1988, and 1989?
SQL: select title, role, year from T where year in (1986, 1988, 1989); 
"""

p_sql_three_fetaqa = """Generate SQL with no explanation given the question and table to answer the question correctly.

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


def truncate_tokens(prompt,  max_length) -> str:
    """Truncates a text string based on max number of tokens."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded_string = encoding.encode(prompt)
    num_tokens = len(encoded_string)

    if num_tokens > max_length:
        prompt = encoding.decode(encoded_string[:max_length])
        print('truncated -->  \nnum_tokens: ', num_tokens)
    return prompt

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7, n=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
        stream=False,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Table:", "\n\n"]
    )
    return response.choices[0].message.content

# --------------------------------------------------------------------------
def gen_table_decom_prompt(title, tab_coll, question, examples, selection='rc'):
    if selection == 'col':
        prompt = "" + p_col_three_fetaqa
    elif selection == 'row':
        prompt = "" + p_row_three_fetaqa
    elif selection == 'rc':
        prompt = "" + p_rc_three_fetaqa
    elif selection == 'sql':
        prompt = "" + p_sql_three_fetaqa
    prompt += "\nSQLite table properties:\n\n"
    prompt += "Table: " + title + "(" + str(tab_coll) + ")" + "\n\n"
    prompt += "3 example rows: \n select * from T limit 3;\n"
    prompt += examples + "\n\n"
    prompt += "Q: " + question + "\n"
    prompt += "SQL:"
    return prompt

def generate_sql_answer_prompt(title, sql,  table, question):
    table = truncate_tokens(table, max_length=600)

    prompt = p_sql_answer_fetaqa
    prompt += "\nTable_title: " + title
    prompt += "\nSQL: " + sql
    prompt += "\n\n" + table
    prompt += "\n\nQuestion: " + question
    prompt += "\nAnswer:"

    return prompt

def generate_answer_prompt(title, table, question):
    prompt = p_answer_fetaqa
    prompt += "\nTable_title: " + title
    prompt += "\nTable:\n" + table
    prompt += "\nQuestion: " + question
    prompt += "\nAnswer:"

    return prompt

def get_sql_3(prompt):
    response = None
    while response is None:
        try:
            response = get_completion(prompt, temperature=0)
        except:
            time.sleep(3)
            pass
    return response

def get_full_table_prompt(title, table, question):
    table = truncate_tokens(table, max_length=3000)

    prompt = p_fetaqa_full + '\n'
    prompt += f'Read the following table regarding "{title}" to answer the given question.'
    prompt += table + '\n\n'
    prompt += 'Question: ' + question + '\nAnswer:'

    return prompt

def get_answer(promt):
    response = None
    while response is None:
        try:
            response = get_completion(promt, temperature=0.7)
            # print('Generated ans------: ', output_ans)
        except:
            time.sleep(3)
            pass
    return response

# --------------------------------------------------------------------------
