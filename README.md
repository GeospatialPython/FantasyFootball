# Fantasy Football Lineup Recommendation Tool
A python fantasy football recommendation tool based on Boris Chen's weekly ranking model which takes select expert ranking data from Fantasypros.com and passes it into a statistical clustering algorithm called a Gaussian mixture model.  The algorithm finds players who are ranked similarly and discovers natural tiers within the data. 

This script takes your team roster and prints out your optimal lineup for the week based on Chen's model.

This script requires the Python requests library:
```pip install requests```

Download the script and populate your roster for each position in the ```roster_dict``` variable. Then just run the script:
```python FFLineup.py```

If a player on your roster is so terrible that he's not in the rankings, or you spelled his name differently than the Chen model does, you'll receive a warning:
```UserWarning: Player Christian Watson not found in real-time data.```

Then you should see a recommended lineup for the week that looks kind of like this, but hopefully with better producers overall:

```
RECOMMENDED LINEUP
------------------
QB:   Joe Burrow
WR1:  Jaylen Waddle
WR2:  Garrett Wilson
RB1:  Christian McCaffrey
RB2:  Derrick Henry
TE:   T.J. Hockenson
FLEX: Chris Godwin
K:    Tyler Bass
DEF:  Dallas Cowboys
```

In the function, ```recommended_lineup```, you have the option of setting the ```flex_first``` argument to ```True``` which will choose your best FLEX player from your WR,RB, and TE pool before it fills those positions. It's set to false by default.

Since 2014, I've been able to credit two 1st place league tropies to this model. It's a great help in the draft, but it really shines as the season wears on and you have to make tough choices on the waiver wire. 



