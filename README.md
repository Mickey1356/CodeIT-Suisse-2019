# CodeIT-Suisse-2019

Contains competition solutions for CodeIT Suisse 2019, organised by Credit Suisse Hong Kong and Singapore. Submissions are made in the form of API requests to a backend server. Due to its simplicity in setting up and understanding, we used Python and the Flask library to create a simple web app that is able to respond to the required API requests.

# Problems
_The problems are listed in no particular order. The description of each problem is my own words._

1) Sentiment Analysis

> A classical machine learning problem. Given a set of movie reviews, classify them according to whether they are "positive" or "negative". No training data was given, so we had to source for our own set.

2) Defuse the bomb

> We were given an array of positive integers, with some of these integers being replaced with -1, as well as another positive integer K. If we are able to replace the -1s in the array with any integer from 1 to k, count how many such new arrays will have a palindromic subarray that is an odd length.

3) Gun Control

> You have a grid maze with each corridor being exactly one tile width and no loops. You start from the top-right tile. At the end of each dead-end of the maze is a number of guns, with the number being exactly the number of tiles needed to reach that end. If you start with K units of fuel, and each tile costs 1 unit of fuel to cross, what is the maximum number of guns you can reach?

4) Ready Player One

> Two numbers are given, N and T. Two players play a game with 1...N integers. Both players will choose an integer from 1 to N and add it to a cummulative sum across both players, with the winner being the first to equal or cross T. Once chosen, the same integer cannot be chosen again. Assuming both players play optimally, given N and T, which of the two players will always win the game.

5) Reverse Lottery

> Ten numbers from 1 to 100 are randomly generated every hour. You only need to submit a list of 10 integers. Scoring is based on how close each number is to the hidden ones. The numbers are counted as looping, so for a target of 100, a guess of 1 will score higher than 98.

6) Yin Yang

> There is a sequence of N Yin and Yang elements, as well as an integer K. For each iteration k from 1 to K, a random number r is generated from 1 to N-k+1. You can choose to remove the r-th element from either the left or right of the sequence. At the end of K iterations, what is the expected number of Yang elements removed?

7) Typing Contest

> Given a list of words with the same length. Determine the least cost and required operations to obtain all the words, assuming you only have the following operations:
>
> `INPUT X`: Writes down X. The cost is the length of X
>
> `COPY X`: Copies X, costs 1
>
> `EDIT X`: Changes the last word in the list into X. The cost is the hamming distance between the last word and X.

8) Chess

> Given a chessboard, count how many squares the queen on the chessboard can attack. There are obstacles on the board the blocks the queen.

9) Composition

> Given a string and a set of patterns of two letters, determine the minimum number of letters to remove from the string such that none of the patterns in the set match the string.

10) Dependency Manager

> Given a set of modules and its dependencies, determine a valid ordering of the modules.

11) Technical Analysis

> Given a set of training data, and the general formula used to generate the data, fit the formula to the training data in order to predict more sets of data. After which, determine the best times to buy and sell in order to make a profit.

12) Portfolio Manager

> Given a set of shares, their expected profit and cost, as well as initial capital, determine which shares to buy in order to maximise profit assuming
>
> a) Each share can only be bought once.
>
> b) Each share must be bought at least once.
>
> c) Each share can be bought however many times.
>
> d) There is some risk associated with each share, you cannot exceed the risk limit given.

13) Wedding Nightmare

> Given a list of friends and enemies, find a way to split them up into K groups (K given), such that no two enemies are in the same group and all the friends are together in the same group.

14) Secret Message

> A decoding method is described, thus, encode a given message.

15) Exponentiation

> Given a and b, for a^b, find the first digit, the last digit, and the total number of digits.

16) Bank Teller

> Given your position in line and the time taken for each counter to serve one customer, determine which counter you will be served by.

17) Prismo

> Given a 1D, 2D (4x4) and 3D (4x4x4) sliding puzzle (see 15-puzzle), determine a solution.

18) Bucket Fill

> Given a SVG with some lines representing "buckets" and other representing "pipes", determine how much volume of water can be held by the system given a single water source.
