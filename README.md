# flexifind
Automatically get the price for all Flixbus departures from your city

This is a Python script to find the cheapest return ticket from your city to any other city with Flixbus. It uses Selenium webdriver with Chrome to automatically fill out and make the querys.

It is quite slow and currently the destination citys it searches for are hardcoded 

TODO: Make it general, so that it will generate a dest_list for any valid origin city.
How can it be made faster? Can we circumvent the webdriver and make pure http requests?
