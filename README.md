Candidates Emailer
==================

This project, using the oDesk API, emails an attachment of the list of
candidates for the client's open jobs.

Notice
------

There's an issue with the httplib2 module using it's own certificate
store, of which the CA certificates oDesk uses are not a part of. You're
going to have to add these to cacerts.txt file in the httplib2 module directory.
