# A Python script for a parallel Blind-SQL Injection 
**Disclaimer:** This is for educational purposes only.

## Summary
Parallel Blind-SQL Injection done in ~30 lines of code that I'm really proud of. Why? It has a Timing based control Structure that does not contain any `if else` statement. I think it's just really neat. It's also super fast. 

**Usage:** `python3 natas17.py `

# How it works:
The code has two parts.
1. HTTP-Request for Blind-SQL Injection
2. Timing-Based Control structure
## 1. HTTP-Request for Blind-SQL Injection
This code solves Natas Level 17, part of the Overthewire wargame: http://natas17.natas.labs.overthewire.org/

![image](https://user-images.githubusercontent.com/90871590/153772920-b3a8f093-ec29-4e31-9d05-01c61206a513.png)

The challenge is to get the Password for the next level using a Blind SQL-Injection. Blind SQL-Injection means that we get no output, we can only know based on the timing of the Request, if our request returned `True` or `False`.

### The server runs the following SQL-Queries
`SELECT * from users where username="` Your Query `" `

### Here is one of the Requests:
`http://natas17.natas.labs.overthewire.org/?username=natas18" and ASCII(Right(password,32)) = "120" and sleep(5) or "`

### The server will therefore execute:
`SELECT * from users where username="`natas18" and ASCII(Right(password,32)) = "65" and sleep(5) or "`"`

This query checks if the first letter of the Query is has the Ascii Value of 65 (`"A"`). If it is true, it will sleep 5 seconds, otherwise it does nothing.

## 2. Timing-Based Control structure
_It's not a Race Condition if you know who will lose the race!_

1. Create a query for all `32` Passwords positions and the possible ASCII characters. 
2. Create a password Buffer to store the result.
3. Create Threads: Their job is to run every query
4. Each Thread stores the corresponding Ascii-Character in the respective position of the password buffer.
5. After every Thread finishes, print out the Password buffer

### Wait! I see no `IF time < 5 seconds` to check if the request should write something!
**Remember:** _It's not a Race Condition if you know who will lose the race!_

32 Threads will have to wait for 5 seconds until the server replies. It's the ones that found the right Password Character! 
During that time the other Threads will have gone though all the other requests. 

The other Threads will fill the Buffer with Garbage but it does not matter!

The last 32 Threads will overwrite the Buffer with the right password.
No `If` statement needed!

# Notes
* This Parallel Solution will find the password in approximately 10 Seconds.
* Since it is a Timing Based algorithm, it is susceptible to Network problems, if that is the case, increase the `sleep`. 
* The Sequential Solution needs on average `7` Request per Password index --> `7`* `32` * `5` Seconds = 1.120 Seconds = 18.7 Minutes
* The Sequential Solution can be very unreliable, it needs to check how much time the request took, which is hard to measure.

## Usefulness
* Any real target will ban your 1000 Request per second.
* Use <a href=https://sqlmap.org/>SQL-Map </a> instead.
