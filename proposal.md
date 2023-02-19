                                      PROJECT PROPOSAL
                'for yet to be titled boardgame collection management app'


    1) GOALS: The goal is to build an app for board game collectors and enthusiasts where they can store their collections, see detailed information of all their games, record gamelogs of play through sessions and get an estimated collection value by aggregating the average used sale price for each of their games.  


    2) DEMOGRAPHICS: Obviously the usefullness of this app would be limited to board game collectors and aficionados but while that is a realitively small group they are very passionate and dedicated. I've already talked to a few freinds who were like 'oh yeah I'd use that, I was just thinking about making an Excel sheet to track half that stuff' so there is an interest, it's just very targerted. 
    
    3) DATA: I will use the boardgameatlas API for the GET routes to retrieve information about a board game, including things like name, release year, genre, discription, player count, images, video links, price history etc. I've already sucessfully tested these endpoints and figured out how to retrieve the data I'll need. As for POST routes such as adding a user, adding or removing a game from a collection, posting a game log, leaving comments etc... I plan to handle all of that myself on the server side with a database.   


    4a) DATABASE SCHEMA: I've yet to fully think this through but there would certainly be a users table storing at the bare minimum a username and hashed password. There would be a collections table storing the games in a users collection. There would perhaps be a wish list table allowing users to add games they would like to acquire. There would be a table that would store gamelogs from playthroughs for each game (writing all of this makes me think that every game that has been added to a collection would need to be stored in a seperate games table). Anyways, these are things I will figure out along the way.

    4b) POTENTIAL ISSUES: The API could be down. Also, the API appears to be a small project built by two passionate boardgamers looking to provide a resource to the community which is double sided. On one hand it obviously creates a point of weakness, I mean if a key developer on the Spotify API suddenly abandons ship there is a level of robustness to where the user would never even know. However, if the same thing occured here the entire API may grind to a halt. On the other hand, I have personal access to the key developers and they seem to respond to any questions. 

    4c) SENSITIVE INFO: The only sensitive information would be the username and password required for login, passwords would be hashed with Bcrypt and stored in the database as encrypted sequences. 

    4d) FUNCTIONALITY: A user would be able to store a digital representation of their boardgame collection and display detailed information for each individual game. They would be able to sort their collection based on genre, player count, game length etc. They would be able to log play sessions for each game and get an estimated value for each game, or their collection as a whole.

    4e) USER FLOW: A user upon arrival to the site would be able to search the API for any information on any given game and it would be displayed. However, they would be prompted to create an account if they wished to enjoy any of the core features, such as storing a collection, wish list, gamelog, collection value etc... 

    4f) MORE THAN CRUD/STRETCH GOALS? Well hopefully it's all more than [crud](https://www.merriam-webster.com/dictionary/crud), but I would say already that the implementation of receiving a valuation for a collection and of logging play sessions is more than basic CRUD. Beyond that as a "STRETCH GOAL" I would like to implement a scoring calculator for each game. This is way harder than it sounds because each game has different variables, conditions, and formulas for scoring so it would need to be an adaptable calculator that could change it's format based on the game it was scoring. 
