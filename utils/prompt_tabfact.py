import time
import os
import openai
import tiktoken

API_KEY = ### 

os.environ['OPENAI_API_KEY'] = API_KEY
# openai.api_key = os.getenv("OPENAI_API_KEY")

# new
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

client = OpenAI()

p_tabfact_full = """
Read the table below regarding "2002 u.s. open (golf)" to verify whether the provided claims are true or false.

place | player | country | score | to par
1 | tiger woods | united states | 67 + 68 + 70 = 205 | - 5
2 | sergio garcía | spain | 68 + 74 + 67 = 209 | - 1
t3 | jeff maggert | united states | 69 + 73 + 68 = 210 | e
t3 | phil mickelson | united states | 70 + 73 + 67 = 210 | e
t5 | robert allenby | australia | 74 + 70 + 67 = 211 | + 1
t5 | pádraig harrington | ireland | 70 + 68 + 73 = 211 | + 1
t5 | billy mayfair | united states | 69 + 74 + 68 = 211 | + 1
t8 | nick faldo | england | 70 + 76 + 66 = 212 | + 2
t8 | justin leonard | united states | 73 + 71 + 68 = 212 | + 2
t10 | tom byrum | united states | 72 + 72 + 70 = 214 | + 4
t10 | davis love iii | united states | 71 + 71 + 72 = 214 | + 4
t10 | scott mccarron | united states | 72 + 72 + 70 = 214 | + 4

Claim: nick faldo is the only player from england.
Explanation: no other player is from england, therefore, the claim is true.

Claim: justin leonard score less than 212 which put him tied for the 8th place.
Explanation: justin leonard scored exactly 212, therefore, the claim is false.

Read the table below regarding "1919 in brazilian football" to verify whether the provided claims are true or false.

date | result | score | brazil scorers | competition
may 11 , 1919 | w | 6 - 0 | friedenreich (3) , neco (2) , haroldo | south american championship
may 18 , 1919 | w | 6 - 1 | heitor , amílcar (4), millon | south american championship
may 26 , 1919 | w | 5 - 2  | neco (5) | south american championship
may 30 , 1919 | l | 1 - 2 | jesus (1) | south american championship
june 2nd , 1919 | l | 0 - 2 | - | south american championship

Claim: neco has scored a total of 7 goals in south american championship.
Explanation: neco has scored 2 goals on may 11  and 5 goals on may 26. neco has scored a total of 7 goals, therefore, the claim is true.

Claim: jesus has scored in two games in south american championship.
Explanation: jesus only scored once on the may 30 game, but not in any other game, therefore, the claim is false.

Claim: brazilian football team has scored six goals twice in south american championship.
Explanation: brazilian football team scored six goals once on may 11 and once on may 18, twice in total, therefore, the claim is true.

"""

p_answer_tabfact = """Read the table below regarding "2002 u.s. open (golf)" to verify whether the provided claims are true or false. 
Check and double check your explanation to make the final decision. 

place | player | country | score | to par
1 | tiger woods | united states | 67 + 68 + 70 = 205 | - 5
2 | sergio garcía | spain | 68 + 74 + 67 = 209 | - 1
t3 | jeff maggert | united states | 69 + 73 + 68 = 210 | e
t3 | phil mickelson | united states | 70 + 73 + 67 = 210 | e
t5 | robert allenby | australia | 74 + 70 + 67 = 211 | + 1
t5 | pádraig harrington | ireland | 70 + 68 + 73 = 211 | + 1
t5 | billy mayfair | united states | 69 + 74 + 68 = 211 | + 1
t8 | nick faldo | england | 70 + 76 + 66 = 212 | + 2
t8 | justin leonard | united states | 73 + 71 + 68 = 212 | + 2
t10 | tom byrum | united states | 72 + 72 + 70 = 214 | + 4
t10 | davis love iii | united states | 71 + 71 + 72 = 214 | + 4
t10 | scott mccarron | united states | 72 + 72 + 70 = 214 | + 4

Claim: nick faldo is the only player from england.
Explanation: no other player is from england, therefore, the claim is true.

Claim: justin leonard score less than 212 which put him tied for the 8th place.
Explanation: justin leonard scored exactly 212, therefore, the claim is false.

Read the table below regarding "1919 in brazilian football" to verify whether the provided claims are true or false.

date | result | score | brazil scorers | competition
may 11 , 1919 | w | 6 - 0 | friedenreich (3) , neco (2) , haroldo | south american championship
may 18 , 1919 | w | 6 - 1 | heitor , amílcar (4), millon | south american championship
may 26 , 1919 | w | 5 - 2  | neco (5) | south american championship
may 30 , 1919 | l | 1 - 2 | jesus (1) | south american championship
june 2nd , 1919 | l | 0 - 2 | - | south american championship

Claim: neco has scored a total of 7 goals in south american championship.
Explanation: neco has scored 2 goals on may 11  and 5 goals on may 26. neco has scored a total of 7 goals, therefore, the claim is true.

Claim: jesus has scored in two games in south american championship.
Explanation: jesus only scored once on the may 30 game, but not in any other game, therefore, the claim is false.

Claim: brazilian football team has scored six goals twice in south american championship.
Explanation: brazilian football team scored six goals once on may 11 and once on may 18, twice in total, therefore, the claim is true.

"""

p_sql_answer_tabfact = """Based on the table title and execution result of the sql query bellow, to verify whether the provided claims are true or false. 
Check and double check your response.

Table_title: katsuya inoue
SQL: SELECT opponent, location, round FROM T WHERE location = 'tokyo , japan' AND round < 2

opponent | location | round
naoyuki kotani | tokyo , japan | 1
kota okazawa | tokyo , japan | 1
yoshiyuki yoshida | tokyo , japan | 1
akira kikuchi | tokyo , japan | 1
heath sims | tokyo , japan | 1
hikaru sato | tokyo , japan | 1

Claim: in tokyo , japan , hikaru sato 's match ended before round 2
Explanation: based on the table, in tokyo , japan , hikaru sato 's match ended in round 1, therefore, the claim is true.

Table_title: utah jazz all - time roster
SQL: SELECT player, position, years_for_jazz FROM T;

player | position | years_for_jazz
mehmet okur | forward - center | 2004-11
josã ortiz | center | 1988 - 90
greg ostertag | center | 1995 - 2004 , 2005-6
dan o 'sullivan | center | 1990 - 91
andre owens | guard | 2005-6

Claim: andre owens played center for the jazz from 2005 - 06
Explanation: andre owens played in guard position for the jazz from 2005 - 06, therefore, the the claim is false.

Table_title: whlp
SQL: SELECT call_sign, erp_w FROM T;

call_sign | erp_w
w221by | 38
w264bf | 2
w240bj | 10
w276bm | 19
w293al | 80
w223au | 10

Claim: w293al and w264bf share the same erp w
Explanation: w293al and w264bf share different erp w, therefore, the the claim is false.

Table_title: 1948 ashes series
SQL: SELECT player, matches, wickets FROM T;

player | matches | wickets
ray lindwall | 5 | 27
bill johnston | 5 | 27
alec bedser | 5 | 18
keith miller | 5 | 13
ernie toshack | 4 | 11
norman yardley | 5 | 9
jim laker | 3 | 9

Claim: the bowler with 13 wickets appeared in less matches than the bowler with 11 wickets
Explanation: based on the table, ernie toshack played 4 matches with 11 wickets, and keith miller got 13 wickets in 5  matches, therefore, the the claim is false.

"""

p_col_tabfact = """Generate SQL given the question and table for selecting the required columns to answer the question correctly.

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

p_row_col_tabfact = """Generate SQL given the question and table for selecting the required rows and columns to answer the question correctly. 

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

# -----------------------------------

p_col_three_tabfact = """Generate SQL for selecting the required columns, to verify the statement correctly. 
Do not use any where clause in the sql, simply select the correct columns to answer the question.

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats kept the opposing team scoreless in four games
SQL: SELECT game, opponent, opponents, record FROM T;

SQLite table properties:

Table: césar ramos(row_number, season, series, team, races, wins, poles, f___laps, podiums, points, position)

3 example rows: 
 select * from T limit 3;
row_number | season | series | team | races | wins | poles | f___laps | podiums | points | position
0 | 2007 | formula renault 2 italy | bvm minardi team | 14 | 0 | 0 | 0 | 1 | 106 | 14th
1 | 2007 | eurocup formula renault 2 | bvm minardi team | 6 | 0 | 0 | 0 | 0 | n / a | nc
2 | 2007 | formula renault 2 italy - wi series | bvm minardi team | 4 | 4 | 4 | 4 | 4 | 144 | 1st

Q: every team had several wins
SQL: SELECT * FROM T;

SQLite table properties:

Table: katsuya inoue(row_number, res, record, opponent, method, event, round, time, location)

3 example rows: 
 select * from T limit 3;
row_number | res | record | opponent | method | event | round | time | location
0 | loss | 19 - 9 - 4 | naoyuki kotani | submission (armbar) | pancrase - impressive tour 9 | 1 | 1:44 | tokyo , japan
1 | loss | 19 - 8 - 4 | kota okazawa | ko (punch) | pancrase - impressive tour 4 | 1 | 2:42 | tokyo , japan
2 | win | 19 - 7 - 4 | katsuhiko nagata | decision (unanimous) | gcm - cage force 17 | 3 | 5:0 | tokyo , japan

Q: in tokyo , japan , hikaru sato 's match ended before round 2
SQL: SELECT round, location FROM T;

SQLite table properties:

Table: 2010 vuelta a colombia(row_number, stage, winner, general_classification, points_classification, mountains_classification, sprints_classification, team_classification)

3 example rows: 
 select * from T limit 3;
row_number | stage | winner | general_classification | points_classification | mountains_classification | sprints_classification | team_classification
0 | 1 | ind ant - idea - fla - lot de medellín | sergio luis henao | no award | no award | no award | ind ant - idea - fla - lot de medellín
1 | 2 | jaime castañeda | óscar sevilla | jaime castañeda | jaime vergara | camilo gómez | ind ant - idea - fla - lot de medellín
2 | 3 | jairo pérez | jairo pérez | jaime castañeda | jaime vergara | julian lopez | ind ant - idea - fla - lot de medellín

Q: sergio luis henao was given the general classification award and the points classification award
SQL: SELECT general_classification, points_classification FROM T;

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats played two games in september , four games in october , and four games in november
SQL: SELECT game, date, opponent FROM T;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: mirielle dittmann was the opponent in the final on hard surface on 6 february 2000 in wellington new zealand
SQL: SELECT opponent_in_final, date, location  FROM T;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: on 2 may 1999 , the surface was hard
SQL: SELECT date, surface  FROM T;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: the opponent in final on 6 february 2000 in wellington new zealand on hard surface was katerina kramperová
SQL: SELECT opponent_in_final, date, location, surface  FROM T;

"""

p_row_three_tabfact = """Generate SQL for selecting the required rows, given the question and table to answer the question correctly.

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats kept the opposing team scoreless in four games
SQL: SELECT * FROM T WHERE opponents = 0;

SQLite table properties:

Table: césar ramos(row_number, season, series, team, races, wins, poles, f___laps, podiums, points, position)

3 example rows: 
 select * from T limit 3;
row_number | season | series | team | races | wins | poles | f___laps | podiums | points | position
0 | 2007 | formula renault 2 italy | bvm minardi team | 14 | 0 | 0 | 0 | 1 | 106 | 14th
1 | 2007 | eurocup formula renault 2 | bvm minardi team | 6 | 0 | 0 | 0 | 0 | n / a | nc
2 | 2007 | formula renault 2 italy - wi series | bvm minardi team | 4 | 4 | 4 | 4 | 4 | 144 | 1st

Q: every team had several wins
SQL: SELECT * FROM T;

SQLite table properties:

Table: katsuya inoue(row_number, res, record, opponent, method, event, round, time, location)

3 example rows: 
 select * from T limit 3;
row_number | res | record | opponent | method | event | round | time | location
0 | loss | 19 - 9 - 4 | naoyuki kotani | submission (armbar) | pancrase - impressive tour 9 | 1 | 1:44 | tokyo , japan
1 | loss | 19 - 8 - 4 | kota okazawa | ko (punch) | pancrase - impressive tour 4 | 1 | 2:42 | tokyo , japan
2 | win | 19 - 7 - 4 | katsuhiko nagata | decision (unanimous) | gcm - cage force 17 | 3 | 5:0 | tokyo , japan

Q: in tokyo , japan , hikaru sato 's match ended before round 2
SQL: SELECT * FROM T WHERE location = 'tokyo , japan';

SQLite table properties:

Table: 2010 vuelta a colombia(row_number, stage, winner, general_classification, points_classification, mountains_classification, sprints_classification, team_classification)

3 example rows: 
 select * from T limit 3;
row_number | stage | winner | general_classification | points_classification | mountains_classification | sprints_classification | team_classification
0 | 1 | ind ant - idea - fla - lot de medellín | sergio luis henao | no award | no award | no award | ind ant - idea - fla - lot de medellín
1 | 2 | jaime castañeda | óscar sevilla | jaime castañeda | jaime vergara | camilo gómez | ind ant - idea - fla - lot de medellín
2 | 3 | jairo pérez | jairo pérez | jaime castañeda | jaime vergara | julian lopez | ind ant - idea - fla - lot de medellín

Q: sergio luis henao was given the general classification award and the points classification award
SQL: SELECT * FROM T WHERE general_classification = 'sergio luis henao' AND points_classification = 'sergio luis henao';

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats played two games in september , four games in october , and four games in november
SQL: SELECT * FROM T WHERE date LIKE 'sept%' AND date LIKE 'oct%' AND date LIKE 'nov%';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: mirielle dittmann was the opponent in the final on hard surface on 6 february 2000 in wellington new zealand
SQL: SELECT * FROM T WHERE  date = '2000-2-6' AND location = 'wellington , new zealand';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: on 2 may 1999 , the surface was hard
SQL: SELECT * FROM T WHERE date = '1999-5-2';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: the opponent in final on 6 february 2000 in wellington new zealand on hard surface was katerina kramperová
SQL: SELECT * FROM T WHERE date = '2000-2-6' AND location = 'wellington , new zealand' AND surface = 'hard';


"""

p_rc_three_tabfact = """Generate SQL for selecting the required rows and columns, given the question and table to answer the question correctly.

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats kept the opposing team scoreless in four games
SQL: SELECT game, opponent, opponents, record FROM T WHERE opponents = 0;

SQLite table properties:

Table: césar ramos(row_number, season, series, team, races, wins, poles, f___laps, podiums, points, position)

3 example rows: 
 select * from T limit 3;
row_number | season | series | team | races | wins | poles | f___laps | podiums | points | position
0 | 2007 | formula renault 2 italy | bvm minardi team | 14 | 0 | 0 | 0 | 1 | 106 | 14th
1 | 2007 | eurocup formula renault 2 | bvm minardi team | 6 | 0 | 0 | 0 | 0 | n / a | nc
2 | 2007 | formula renault 2 italy - wi series | bvm minardi team | 4 | 4 | 4 | 4 | 4 | 144 | 1st

Q: every team had several wins
SQL: SELECT * FROM T;

SQLite table properties:

Table: katsuya inoue(row_number, res, record, opponent, method, event, round, time, location)

3 example rows: 
 select * from T limit 3;
row_number | res | record | opponent | method | event | round | time | location
0 | loss | 19 - 9 - 4 | naoyuki kotani | submission (armbar) | pancrase - impressive tour 9 | 1 | 1:44 | tokyo , japan
1 | loss | 19 - 8 - 4 | kota okazawa | ko (punch) | pancrase - impressive tour 4 | 1 | 2:42 | tokyo , japan
2 | win | 19 - 7 - 4 | katsuhiko nagata | decision (unanimous) | gcm - cage force 17 | 3 | 5:0 | tokyo , japan

Q: in tokyo , japan , hikaru sato 's match ended before round 2
SQL: SELECT round, location FROM T WHERE location = 'tokyo , japan';

SQLite table properties:

Table: 2010 vuelta a colombia(row_number, stage, winner, general_classification, points_classification, mountains_classification, sprints_classification, team_classification)

3 example rows: 
 select * from T limit 3;
row_number | stage | winner | general_classification | points_classification | mountains_classification | sprints_classification | team_classification
0 | 1 | ind ant - idea - fla - lot de medellín | sergio luis henao | no award | no award | no award | ind ant - idea - fla - lot de medellín
1 | 2 | jaime castañeda | óscar sevilla | jaime castañeda | jaime vergara | camilo gómez | ind ant - idea - fla - lot de medellín
2 | 3 | jairo pérez | jairo pérez | jaime castañeda | jaime vergara | julian lopez | ind ant - idea - fla - lot de medellín

Q: sergio luis henao was given the general classification award and the points classification award
SQL: SELECT general_classification, points_classification FROM T WHERE general_classification = 'sergio luis henao' AND points_classification = 'sergio luis henao';

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats played two games in september , four games in october , and four games in november
SQL: SELECT game, date, opponent FROM T WHERE date LIKE 'sept%' AND date LIKE 'oct%' AND date LIKE 'nov%';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: mirielle dittmann was the opponent in the final on hard surface on 6 february 2000 in wellington new zealand
SQL: SELECT opponent_in_final, date, location  FROM T WHERE  date = '2000-2-6' AND location = 'wellington , new zealand';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: on 2 may 1999 , the surface was hard
SQL: SELECT date, surface  FROM T WHERE date = '1999-5-2';

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: the opponent in final on 6 february 2000 in wellington new zealand on hard surface was katerina kramperová
SQL: SELECT opponent_in_final, date, location, surface  FROM T WHERE date = '2000-2-6' AND location = 'wellington , new zealand' AND surface = 'hard';

"""

p_sql_three_tabfact = """Generate SQL given the statement and table to verify the statement correctly.

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats kept the opposing team scoreless in four games
SQL: SELECT (SELECT COUNT(*) FROM T WHERE opponents = 0) = 4

SQLite table properties:

Table: césar ramos(row_number, season, series, team, races, wins, poles, f___laps, podiums, points, position)

3 example rows: 
 select * from T limit 3;
row_number | season | series | team | races | wins | poles | f___laps | podiums | points | position
0 | 2007 | formula renault 2 italy | bvm minardi team | 14 | 0 | 0 | 0 | 1 | 106 | 14th
1 | 2007 | eurocup formula renault 2 | bvm minardi team | 6 | 0 | 0 | 0 | 0 | n / a | nc
2 | 2007 | formula renault 2 italy - wi series | bvm minardi team | 4 | 4 | 4 | 4 | 4 | 144 | 1st

Q: every team had several wins
SQL: SELECT (SELECT COUNT(*) FROM T WHERE wins > 0) = (SELECT COUNT(DISTINCT team) FROM T);

SQLite table properties:

Table: katsuya inoue(row_number, res, record, opponent, method, event, round, time, location)

3 example rows: 
 select * from T limit 3;
row_number | res | record | opponent | method | event | round | time | location
0 | loss | 19 - 9 - 4 | naoyuki kotani | submission (armbar) | pancrase - impressive tour 9 | 1 | 1:44 | tokyo , japan
1 | loss | 19 - 8 - 4 | kota okazawa | ko (punch) | pancrase - impressive tour 4 | 1 | 2:42 | tokyo , japan
2 | win | 19 - 7 - 4 | katsuhiko nagata | decision (unanimous) | gcm - cage force 17 | 3 | 5:0 | tokyo , japan

Q: in tokyo , japan , hikaru sato 's match ended before round 2
SQL: SELECT (SELECT COUNT(*) FROM T WHERE location = 'tokyo , japan' AND round < 2) > 0;

SQLite table properties:

Table: 2010 vuelta a colombia(row_number, stage, winner, general_classification, points_classification, mountains_classification, sprints_classification, team_classification)

3 example rows: 
 select * from T limit 3;
row_number | stage | winner | general_classification | points_classification | mountains_classification | sprints_classification | team_classification
0 | 1 | ind ant - idea - fla - lot de medellín | sergio luis henao | no award | no award | no award | ind ant - idea - fla - lot de medellín
1 | 2 | jaime castañeda | óscar sevilla | jaime castañeda | jaime vergara | camilo gómez | ind ant - idea - fla - lot de medellín
2 | 3 | jairo pérez | jairo pérez | jaime castañeda | jaime vergara | julian lopez | ind ant - idea - fla - lot de medellín

Q: sergio luis henao was given the general classification award and the points classification award
SQL: SELECT (SELECT COUNT(*) FROM T WHERE general_classification = 'sergio luis henao' AND points_classification = 'sergio luis henao') > 0;

SQLite table properties:

Table: 1947 kentucky wildcats football team(row_number, game, date, opponent, result, wildcats_points, opponents, record)

3 example rows: 
 select * from T limit 3;
row_number | game | date | opponent | result | wildcats_points | opponents | record
0 | 1 | sept 20 | ole miss | loss | 7 | 14 | 0 - 1
1 | 2 | sept 27 | cincinnati | win | 20 | 0 | 1 - 1
2 | 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1

Q: the wildcats played two games in september , four games in october , and four games in november
SQL: SELECT (SELECT COUNT(*) FROM T WHERE date LIKE 'sept%') = 2 AND (SELECT COUNT(*) FROM T WHERE date LIKE 'oct%') = 4 AND (SELECT COUNT(*) FROM T WHERE date LIKE 'nov%') = 4;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: mirielle dittmann was the opponent in the final on hard surface on 6 february 2000 in wellington new zealand
SQL: SELECT (SELECT COUNT(*) FROM T WHERE opponent_in_final = 'mirielle dittmann' AND surface = 'hard' AND date = '2000-2-6' AND location = 'wellington , new zealand') > 0;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: on 2 may 1999 , the surface was hard
SQL: SELECT (SELECT COUNT(*) FROM T WHERE date = '1999-5-2' AND surface = 'hard') > 0;

SQLite table properties:

Table: leanne baker(row_number, outcome, date, location, surface, opponent_in_final, score)

3 example rows: 
 select * from T limit 3;
row_number | outcome | date | location | surface | opponent_in_final | score
0 | winner | 1999-5-2 | coatzacoalcos , mexico | hard | candice jairala | 3 - 6 6 - 3 7 - 5
1 | winner | 1999-7-11 | felixstowe , england | grass | karen nugent | 6 - 4 6 - 4
2 | runner - up | 2000-2-6 | wellington , new zealand | hard | mirielle dittmann | 6 - 7 (5) 6 - 1 6 - 7 (5)

Q: the opponent in final on 6 february 2000 in wellington new zealand on hard surface was katerina kramperová
SQL: SELECT (SELECT COUNT(*) FROM T WHERE date = '2000-2-6' AND location = 'wellington , new zealand' AND surface = 'hard' AND opponent_in_final = 'katerina kramperová') > 0;

"""

p_sql_three_tabfact_1 = """Generate SQL given the statement and table to verify the statement correctly.

CREATE TABLE turkish cup(
	row_id int,
	round text,
	clubs remaining int,
	clubs involved int,
	winners from previous round real,
	new entries this round real,
	leagues entering at this round text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	round	clubs remaining	clubs involved	winners from previous round	new entries this round	leagues entering at this round
0	first round	156	86	nan	86.0	tff third league & turkish regional amateur league
1	second round	113	108	43.0	65.0	süper lig & tff first league & tff second league
2	third round	59	54	54.0	nan	none
*/
Q: during the 3rd round of the turkish cup , there be no new entry during that stage
SQL: SELECT (SELECT `new entries this round` FROM T WHERE round = 'third round') IS NULL


CREATE TABLE turkish cup(
	row_id int,
	round text,
	clubs remaining int,
	clubs involved int,
	winners from previous round real,
	new entries this round real,
	leagues entering at this round text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	round	clubs remaining	clubs involved	winners from previous round	new entries this round	leagues entering at this round
0	first round	156	86	nan	86.0	tff third league
1	second round	113	108	43.0	65.0	süper ligs
2	third round	59	54	54.0	nan	none
*/
Q: süper lig be the league to win a round in the turkish cup with 110 clubs
SQL: SELECT (SELECT clubs FROM T WHERE `leagues entering at this round` = 'süper ligs') = 110


CREATE TABLE turkish cup(
	row_id int,
	round text,
	clubs remaining int,
	clubs involved int,
	winners from previous round real,
	new entries this round real,
	leagues entering at this round text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	round	clubs remaining	clubs involved	winners from previous round	new entries this round	leagues entering at this round
0	first round	156	86	nan	86.0	tff third league & turkish regional amateur league
1	second round	113	108	43.0	65.0	süper lig & tff first league & tff second league
2	third round	59	54	54.0	nan	none
*/
Q: the lowest number of new entry conclude a round in the turkish cup be 5
SQL: SELECT (SELECT MIN(`new entries this round`) FROM T) = 5


CREATE TABLE cultural interest fraternities and sororities(
	row_id int,
	letters text,
	organization text,
	nickname text,
	founding time text,
	founding university text,
	type text)
/*
3 example rows:
SELECT * FROM w LIMIT 3;
row_id	letters	organization	nickname	founding time	founding university	type
0	αεπ	alpha epsilon pi 1	aepi	1913-11-07 00:00:00	new york university	fraternity
1	αεφ	alpha epsilon phi 2	aephi	1909-10-24 00:00:00	barnard college	sorority
2	σαεπ	sigma alpha epsilon pi 3	sigma	1998-10-01 00:00:00	university of california , davis	sorority
*/
Q: 4 of the cultural interest fraternity and sorority be fraternity while 3 be a sorority
SQL: SELECT (SELECT (SELECT COUNT(*) FROM T WHERE type = 'fraternity') = 4) AND (SELECT (SELECT COUNT(*) FROM T WHERE type = 'sorority') = 3)


CREATE TABLE british records in athletics(
	row_id int,
	event text,
	data text,
	athlete text,
	date text,
	place text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	event	data	athlete	date	place
0	5 km	t19:29	andi drake	1990-05-27 00:00:00	norway
1	5 miles	32:38 +	ian mccombie	1985-03-23 00:00:00	united kingdom
2	10 km	40:17	chris maddocks	1989-04-30 00:00:00	united kingdom
*/
Q: there be 8 different event that take place within the united kingdom
SQL: SELECT (SELECT COUNT(place) FROM T WHERE place = 'united kingdom') = 8


CREATE TABLE jeev milkha singh(
	row_id int,
	tournament text,
	wins int,
	top - 10 int,
	top - 25 int,
	events int,
	cuts made int)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	tournament	wins	top - 10	top - 25	events	cuts made
0	masters tournament	0	0	1	3	2
1	us open	0	0	0	4	3
2	the open championship	0	0	0	2	1
*/
Q: the number of cut made in the pga championship tournament be smaller than the number of event
SQL: SELECT (SELECT `cuts made` FROM T WHERE tournament = 'pga championship') < (SELECT events FROM T WHERE tournament = 'pga championship')


CREATE TABLE 2008 women 's british open(
	row_id int,
	place text,
	player text,
	country text,
	score int,
	to par int)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	place	player	country	score	to par
0	1	juli inkster	united states	65	7
1	t2	momoko ueda	japan	66	6
2	t2	laura diaz	united states	66	6
*/
Q: the 3 player from japan have the same score
SQL: SELECT (SELECT COUNT(DISTINCT score) FROM T WHERE country = 'japan' GROUP BY score) = 1


CREATE TABLE espn sunday night football results (1987 - 2005)(
	row_id int,
	date text,
	visiting team text,
	final score text,
	host team text,
	stadium text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	date	visiting team	final score	host team	stadium
0	new year eve	indianapolis colts	24 - 7	baltimore ravens	m&t bank stadium
1	new year eve	kansas city chiefs	23 - 17	oakland raiders	mcafee coliseum
2	new year's day	new york giants	23 - 45	san diego chargers	qualcomm stadium
*/
Q: the hosting team be the new york giant on new year even and the st louis ram on new year 's day
SQL: SELECT (SELECT (SELECT `host team` FROM T WHERE date = 'new year eve') = 'new york giant') AND (SELECT (SELECT `host team` FROM T WHERE date = 'new year's day') = 'st louis ram')


CREATE TABLE 2008 women 's british open(
	row_id int,
	place text,
	player text,
	country text,
	score text,
	to par int)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	place	player	country	score	to par
0	t1	yuri fudoh	japan	134	10
1	t1	jiyai shin	south korea	134	10
2	3	juli inkster	united states 135	9
*/
Q: kristie kerr , tie for 4th place , finish the round 1 stroke under lorena ochoa of mexico
SQL: SELECT (SELECT (SELECT score FROM T WHERE player = 'cristie kerr') < (SELECT score FROM T WHERE player = 'lorena ochoa' AND country = 'mexico')) AND (SELECT (SELECT place FROM T WHERE player = 'cristie kerr') = "t4")


CREATE TABLE connecticut public radio(
	row_id int,
	call sign text,
	frequency text,
	city of license text,
	facility id int,
	erp / power w int,
	height m ( ft ) real,
	class text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	call sign	frequency	city of license	facility id	erp / power w	height m ( ft )	class
0	waic	91.9 fm	springfield , ma	1749	230	nan	b1
1	wedw - fm	88.5 fm	stamford , ct	13619	2000	nan	a
2	wnpr	90.5 fm ( hd ) connecticut public radio	meriden , ct	13627	18500	nan	b
*/
Q: there be 3 station with a call sign number in the 90s
SQL: SELECT (SELECT COUNT(*) FROM T WHERE frequency > 90 GROUP BY `call sign`) = 3


CREATE TABLE 2003 chicago white sox season(
	row_id int,
	date text,
	opponent text,
	score text,
	loss text,
	time text,
	att int,
	record text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	date	opponent	score	loss	time	att	record
0	august 1	mariners	12 - 1	garcía (9 - 11)	2:52	39337	58 - 51
1	august 2	mariners	0 - 10	wright (0 - 5)	2:22	45719	58 - 52
2	august 3	mariners	2 - 8	buehrle (9 - 11)	2:57	45632	58 - 53
*/
Q: the 2003 chicago white sox game play on 26th august be longer than the game play on 24th august
SQL: SELECT (SELECT time FROM T WHERE date = 'august 26') > (SELECT time FROM T WHERE date = 'august 24')


CREATE TABLE 1987 masters tournament(
	row_id int,
	place text,
	player text,
	country text,
	score text,
	to par text,
	money text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	place	player	country	score	to par	money
0	t1	larry mize	united states	70 + 72 + 72 + 71 = 285	-3	playoff
1	t1	bernhard langer	spain	73 + 71 + 70 + 71 = 285	-3	playoff
2	t1	greg norman	australia	73 + 74 + 66 + 72 = 285	-3	playoff
*/
Q: bernhard m. langer have more point than roger maltbie during the 1987 master tournament
SQL: SELECT (SELECT score FROM T WHERE player = 'bernhard langer') > (SELECT score FROM T WHERE player = 'roger maltbie')


CREATE TABLE 1987 masters tournament(
	row_id int,
	place text,
	player text,
	country text,
	score text,
	to par text,
	money text)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	place	player	country	score	to par	money
0	t1	larry mize	united states	70 + 72 + 72 + 71 = 285	-3	playoff
1	t1	seve ballesteros	spain	73 + 71 + 70 + 71 = 285	-3	playoff
2	t1	greg norman	australia	73 + 74 + 66 + 72 = 285	-3	playoff
*/
Q: most of the people who play for the 1987 master tournament be spanish
SQL: SELECT (SELECT(SELECT COUNT(*) FROM T WHERE country = 'spain') / (SELECT COUNT(*) FROM T)) > 0.5


CREATE TABLE 1976 world junior figure skating championships(
	row_id int,
	rank int,
	name text,
	nation text,
	points real,
	places int)
/*
3 example rows:
SELECT * FROM T LIMIT 3;
row_id	rank	name	nation	points	places
0	1	sherri baier / robin cowan	canada	128.39	9
1	2	lorene mitchell / donald mitchell	united states	124.94	16
2	3	elizabeth cain / peter cain	australia	116.67	33
*/
Q: 2 of the 7 top - ranked figure skate team be from france
SQL: SELECT (SELECT (SELECT COUNT(*) FROM T) = 7) AND (SELECT (SELECT COUNT(*) FROM T WHERE nation = 'france') = 2)
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

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.6, n=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        n=n,
        stream=False,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Table:", "\n\n\n"]
    )
    return response.choices[0].message.content

def generate_answer_prompt(title, table, statement):
    prompt = p_answer_tabfact + '\n'
    prompt += f'Read the table below regarding "{title}" to verify whether the provided claim is true or false.\n'
    prompt += 'Check and double check your explanation to make the final decision.\n\n'
    prompt += table + '\n\n'
    # prompt += 'Please verify whether following claim is true or false.\n\n'
    prompt += 'Claim: ' + statement + '\n' + 'Explanation:'

    return prompt

def gen_table_decom_prompt(title, tab_coll, question, examples, selection='sql'):
    if selection == 'col':
        prompt = "" + p_col_three_tabfact
    elif selection == 'row':
        prompt = "" + p_row_three_tabfact
    elif selection == 'rc':
        prompt = "" + p_rc_three_tabfact
    elif selection == 'sql':
        prompt = "" + p_sql_three_tabfact_1
    prompt += "\nSQLite table properties:\n\n"
    prompt += "Table: " + title + "(" + str(tab_coll) + ")" + "\n\n"
    prompt += "3 example rows: \nselect * from T limit 3;\n"
    prompt += examples + "\n\n"
    prompt += "Q: " + question + "\n"
    prompt += "SQL:"
    return prompt

def generate_sql_answer_prompt(title, sql,  table, statement):
    table = truncate_tokens(table, max_length=3000)

    prompt = p_sql_answer_tabfact
    prompt += "\nTable_title: " + title
    prompt += "\nSQL: " + sql
    prompt += "\n\n" + table +'\n\n'
    prompt += 'Claim: ' + statement + '\n' + 'Explanation:'

    return prompt

def get_sql_3(prompt):
    response = None
    while response is None:
        try:
            response = get_completion(prompt, temperature=0.3)
        except:
            time.sleep(2)
            pass
    return response

def gen_full_table_prompt(title, table, statement):
    table = truncate_tokens(table, max_length=600)

    prompt = p_tabfact_full + '\n'
    prompt += f'Read the table below regarding "{title}" to verify whether the provided claim is true or false.\n\n'
    # prompt += f'Title: {entry["title"]}:\n'
    prompt += table + '\n'
    # prompt += 'Please verify whether following claim is true or false.\n\n'
    prompt += 'Claim: ' + statement + '\n' + 'Explanation:'

    return prompt

def get_answer(promt):
    response = None
    while response is None:
        try:

            response = get_completion(promt, temperature=0.6)
            # print('Generated ans------>: ', response)
        except:
            # print('sleep')
            time.sleep(2)
            pass

    return response

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------