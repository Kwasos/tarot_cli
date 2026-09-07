# tarot_cli
A CLI for selecting Tarot cards. Supports deck manipulation.

## Usage
While in project folder:

`python3 main.py`

## Instalation
`git clone https://github.com/Kwasos/tarot_cli`

`cd tarot_cli`

## Functionality

### Deck commands:
                                                        
> draw (X) --- draw the specified number of cards, if no number is given, draw a single card from the deck

> shuffle --- return all cards to the deck

> deck --- display the current number of cards in the deck

> drawn --- display drawn cards, currently not in the deck

> inspect --- display all card details for the specified card

> meaning --- display the meaning of a card

### Spreads:
                                                           
> daily --- deterministic selection of a random card based on the current date, always uses a fresh deck and draws the card
upright

> reading (X) --- draw the specified number of cards, creating a reading for each, with no number provided, draw and read a
single card

### System commands:
                                                       
> help | h --- print a list of avaiable commands

> quit | q --- closes the program


## License
[MIT](https://opensource.org/license/MIT)

Cards data in tarot.json is based on public domain works:

Pictorial Key to the Tarot by A. E. Waite (1911)

Oracle of the Tarot by Paul Foster Case (1933)

Book T by MacGregor Mathers and Harriet Felkin (1888)

