-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description
FROM crime_scene_reports
WHERE day=28 AND month=7 AND year=2021 AND street = "Humphrey Street";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
-- | Littering took place at 16:36. No known witnesses.
-- Work with the description

SELECT * FROM interviews
WHERE transcript LIKE '%bakery%' AND day=28 AND month=7 AND year=2021;

-- Raymond tell that the thief called someone to buy the earliest flight out of Fiftyville at the next day
-- The thief drive away with a car that was at bakery parking lot in about 10 minutes after the theft
-- The thief stayed 30 minutes at the bakery
-- The thief withdraw money at Leggett Street

SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year =2021 AND month=7 AND day=28 AND hour=10 AND minute>=15 AND minute<=25 AND activity='exit';

-- Bakery entries suspects: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year=2021 AND month=7 AND day=28 AND atm_location='Leggett Street' AND transaction_type='withdraw';

-- Account withdraw suspects: Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

SELECT name FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = (
SELECT id FROM flights
WHERE day=29
ORDER BY hour,minute ASC
LIMIT 1);

-- Flight Suspects: Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE year=2021 AND month=7 AND day=28 AND duration < 60;

-- Call Suspects: Sofia, Kelsey, Bruce, Taylor, Diana, Carina, Kenny, Benista

-- The only that matches all the suspects is: Bruce

SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM flights
WHERE year=2021 AND month=7 AND day=29 AND origin_airport_id = (
SELECT id FROM airports WHERE city="Fiftyville")
ORDER BY hour, minute
LIMIT 1);

-- And he is going to New York City

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE day = "28" AND month = "7" AND year = "2021" AND duration < "60" AND caller = (
    SELECT phone_number
    FROM people
    WHERE name = "Bruce");

-- Her accompliance is: Robin
