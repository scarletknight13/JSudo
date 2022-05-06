# JSudo
## Project Description
Variant of a classic game called sudoku. In the original you have to fill non-empty 9 X 9 matrix with digits 1-9 without repeats in columns/rows/ or 3 X 3 submatrices. In this variant
you start with a empty 9 x 9 board and where each cell has an associated number. Whenever you fill a cell your score increases by the number you picked times the associated 
number for that cell. The game renders with a computer generated score and you must complete the board with a higher score within the time limit.
![image]()
## Layout
First You have the 9 x 9 matrix with the associated numbers in each cell. Then there's three labels one for the playerScore, time remaining, and computer score. 
Then you have a clear button that clears entire board.
## Technologies Used
- Python
- Pygame
- Beautiful Soap
## Major Hurdles
Having a precalculated score that the user can reasonably be able to beat was a challenge. After hours of brainstorming I found a website that generates a random a random sudoku board.
I used Beautiful Soup to webscrape this website and then manipulated the data according to the matrix of associated digits to maximize the score. 
## Future Implamentations
I would like to include different modes of diffuculties for the player to select from. I would also like to include a way for the player to see the associated digit for a specific 
cell after filling cell with digit.

