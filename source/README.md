# Features
New RESTful endpoints:
* **GET /users** returns a list of all users and their informations
* **GET /users/email** get the information of a single user
* **PUT /users/email** Update a user, taking a "total" argument (an order total), converting it to points, and adding it to the user's total points. Note that this operation is not idempotent.

This solution fulfills the basic goals of the project. I added two new rewards tiers to simplify the process of going out of bounds on tiers, and my design generally tries to make no assumptions about future restructuring of the tiers. If the tiers are ever modified, all that would be necessary to do to update each user would be to call a PUT request on each one with 0 as the total.

As requested, this is a "story branch", and if this were a real project I would consolidate my commit history into logical pieces with close commit times.

# Hacks
* Unfortunately I had a problem with my new tiers occasionally disappearing from MongoDB. I didn't find the cause of this, but I put in a temporary hack to restore these tiers if they're missing (in the users handler in PUT)
* the UsersHandler is manually setting the "Access-Control-Allow-Methods" because I kept having problems with this in chrome. I imagine a better implementation of a 'def options' in the same file should take care of this automatically.

# Looking ahead
* If I'd had more time, I would have downloaded the icons I used for ongoing and unsucessful searches and put them in a static assets folder, along with separate files for the CSS and javascript.
* While the server is somewhat descriminating about the data it takes in, itcould be more picky about input, it would be nice to have client side form validation, and more gracefull error responses from the server.
* An error notification could be shown on the update box the same way that an error is shown on the search box-- Right now failures are silent.
* The page could be prettier
