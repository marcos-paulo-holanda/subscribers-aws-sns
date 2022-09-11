# subscribers-aws-sns
In this simple project a created a program which sends sms and emails messages to some contacts subscribed in aws sns reporting problems in a city.

To run the program is necessary to have a user id and secret key created with the IAM tool of AWS.

So with the boto3 library is created a client and a bucket where will be deployed the contacts file and the final report which contains some city problems.

If the quantity of the respectively problems exceed some limits it is sent sms and emails messages to the subscribers who may be the mayor or representatives of the city.
