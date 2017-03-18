# py-find-home

The entry point is `find_home`

To verify algorithm:
  `python -m unittest src/test/test_find_home_location.py`
  
  The above test location discusses the the test strategy.
  
  The tests will run a version of the data which include a found case, and another version of the data which include an inconclusive case.
  
  The found case includes partial window boundaries.  eg 6pm to 12am will register 4 hours and 5am to 12pm will register 3 hours.
  
 ### Assumptions
 
  - No visit windows overlap
  - All visit json data are well formed per the data structure given (meaning no need to validate incoming data)
  - The input data is a list of dictionaries.
 
