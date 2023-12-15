# Bee Inkspired 

Bee Inkspired is the homepage for Olivia Harpers tattoo business, it showcases her work and allows her and her customers a place to manage appointment bookings and deal with enquires. The website is themed around her brand and logo.

## Features

As a B2C site the final aim is to impress customers to book a tattoo or make an enquiry. The site needs to be easy to navigate and comprehensive in the information given on Olivia, her skills and the studio. The booking system needs to be straight forward and simple.

#### Goals for the user

- Learn about the artist and view previous work
- Easy to locate the studio 
- Simple link to artists social media
- Register and log in with authentication
- View a personalised dashboard to see user details and upcoming bookings
- Send an enquiry with a reference image


#### Goals for the Artist

- Separate dashboard to show upcoming bookings and enquiries


## Future features

- Users will need to pay a deposit to secure their booking.
- Times slots added to bookings so there can be multiple flash tattoos in a day if the artist has no other tattoos scheduled for that day.



## Bugs

The form to create a booking is made with a custom date field to only display the upcoming 2 weeks, therefore this data then had to be modified and saved onto the booking model.



## Creating the website

The project was created on Gitpod and pushed to GitHub, the Data is stored with ElephantSQL and media is stored in Cloudinary, both linked with API's to the project. The website is then deployed to create the app using Heroku.

### Languages

HTML
CSS
PYTHON
DJANGO
JAVA
BOOTSTRAP



## Installing

Steps to configure and deploy the application.

- Clone the Repository
- Fork the Repository
- Create Application and Postgres DB on Heroku
- Connect the Heroku app to the GitHub repository
- Final Deployment steps:
    - Set DEBUG flag to False in settings.py
    - Ensure this line exists in settings.py to make summernote work on the deployed environment (CORS security feature): X_FRAME_OPTIONS = 'SAMEORIGIN'
    - Ensure requirements.txt is up to date using the command : pip3 freeze --local > requirements.txt
    - Push files to GitHub
    - In the Heroku Config Vars for the application delete this environment variable : DISABLE_COLLECTSTATIC
    - On the Heroku dashboard go to the Deploy tab for the application and click on deploy branch

## Credits

### Media 

A big thank you to Olivia Harper for sending all the original material for me to create this project.

### Code

Thank you to [Dennis Ivy](https://www.youtube.com/watch?v=xv_bwpA_aEA&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO) on Youtube for his in depth walk through of a booking project.
Also thank you to Code Institute's tutor support team for helping me out with the date issue in my booking form as mentioned in the above bugs section.