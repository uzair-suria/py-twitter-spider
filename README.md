# Python Twitter Spider
A python script to that retrieves screen names upon input of an initial screen name. Upon getting an initial screen name, the program connects with twitter api and retrieves account information. If it is successful, the program then proceeds to retrieve at most 100 friend's screen name and enters them in the database. A unique ID is assignned to each entered and retrieved account and accounts followed by the current accounts are mapped in another table using `from_id` and `to_id`, where `from_id` is the current account and `to_id` is the retrieved account. Finally, the program marks the entered screen name as *retrieved*. 

Once the data has been stored (after the very first program execution) in database, the program prompts the user to enter another twitter screen name. Now, the user has the option to either enter a screen name again or just press enter. If a screen name is entered, the program checks the database if the name already exists or not. If the name does not exist, then the program creates a new entry in the database with the name. The program then retrieves at most 100 friends of the current account and creates a new entry for these screen names if they do not previously exist. It also performs the mapping of `from_id` to `to_id` to keep track of who follows who.

## Usage
For this program to run successfully, Following things must ensured:

* sqlite browser should be installed for viewing the stored data

* sqlite library should be installed for python

* tweepy library should be installed for python

* the user needs have a [Twitter Developer](https://developer.twitter.com/en) account. 

<blockquote>
  From the developer account, the user must retrieve following keys:
  <code>
    
    API key

    API key secret

    Bearer token

    Access token

    Access token secret

  </code>
  The above codes/keys are required to be entered in the text file <code>./Keys/keys.txt</code>
</blockquote>



