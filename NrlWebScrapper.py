# testing commits
import requests
from bs4 import BeautifulSoup
import re
from _datetime import datetime

def formatTeamName(team):
    i = 0
    j = 0
    while i < len(team):
        team[j] = str(team[i]) + str(team[i + 1]) + str(team[i + 2])
        i += 3
        j += 1
    team = team[0:8]
    return team

def nrl_scraper():
    url_round = 1354 # 1354 is Round 1 2016, 1379 is Round 26, 2016
    gameSeasonData = []
    postGame = True
    while postGame == True:
        # scrape and store data from url
        url = 'http://www.nrl.com/Draw/TelstraPremiership/Draw/tabid/11180/s/44/r/' + str(url_round) + '/sc/cWOFGg40w000/default.aspx'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        # search the html and store data into variables
        # initialise arrays to store the data
        round = []
        matchID = []
        matchDate = []
        matchCode = []
        venueName = []
        homeTeam = []
        homeScore = []
        awayTeam = []
        awayScore = []
        # Finding the first of each data in the soup html
        remainingGames = len(soup.find_all('div', {'class': 'drawGame drawGame--post'}))
        matchData = soup.find('div', {'class': 'drawGame drawGame--post'})
        venueData = soup.find('h2', {'class': 'drawGame__timeLocation'})
        roundData = soup.find(string=re.compile('^Rnd '))
        homeTeamData = soup.find('div', {'class': 'drawGame__name drawGame__name--home'})
        awayTeamData = soup.find('div', {'class': 'drawGame__name drawGame__name--away'})
        homeScoreData = soup.find('div', {'class': 'drawGame__score--home--score'})
        awayScoreData = soup.find('div', {'class': 'drawGame__score--away--score'})
        while remainingGames > 0:
            if remainingGames != len(soup.find_all('div', {'class': 'drawGame drawGame--post'})):
                matchData = matchData.find_next('div', {'class': 'drawGame drawGame--post'})
                venueData = venueData.find_next('h2', {'class': 'drawGame__timeLocation'})
                roundData = roundData.find_next(string=re.compile('^Rnd '))
                homeTeamData = homeTeamData.find_next('div', {'class': 'drawGame__name drawGame__name--home'})
                awayTeamData = awayTeamData.find_next('div', {'class': 'drawGame__name drawGame__name--away'})
                homeScoreData = homeScoreData.find_next('div', {'class': 'drawGame__score--home--score'})
                awayScoreData = awayScoreData.find_next('div', {'class': 'drawGame__score--away--score'})

            # Get match ID, Date and Code
            matchID.append(matchData.get('matchid'))
            matchDate.append(matchData.get('matchdate'))
            matchCode.append(matchData.get('matchcode'))
            # Venue
            venueName.append(venueData.get('venuename'))
            # Round
            round.append(roundData.string)
            # Home Team
            for x in homeTeamData.children:
                homeTeam.append(x.string)
            # Away Team
            for x in awayTeamData.children:
                awayTeam.append(x.string)
            # Scores - Home and Away
            for x in homeScoreData.children:
                print(homeScoreData)
                homeScore.append(x.string)

            for x in awayScoreData.children:
                awayScore.append(x.string)
            remainingGames -= 1

        # Format team names properly
        homeTeam = formatTeamName(homeTeam)
        awayTeam = formatTeamName(awayTeam)

        gameRoundData = list(zip(round, matchID, matchDate, matchCode, venueName, homeTeam, homeScore, awayTeam, awayScore))
        gameSeasonData.append(gameRoundData)
        url_round += 1

        if len(soup.find_all('div', {'class': 'drawGame drawGame--pre'})) > 0:
            postGame = False

    # Writes the data in gameData to a .csv format file for importing into Excel
    gameDataFile = open('NRL_gameData_' + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.csv', 'w')
    gameDataFile.write('Round,MatchID,MatchDate,MatchCode,Venue,HomeTeam,HomeScore,AwayTeam,AwayScore' + '\n')
    for x in gameSeasonData:
        for y in x:
            for z in y:
                gameDataFile.write(str(z) + ',')
            gameDataFile.write('\n')
        gameDataFile.write('\n')
    gameDataFile.close()

nrl_scraper()
