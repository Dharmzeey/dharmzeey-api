---
title: Tree Database
slug: tree-database
category: Web Application
intro: Documentation of trees arround, providing identification and taxonomic details through a web application.
url: https://tree-database.dharmzeey.com/
github: https://github.com/Dharmzeey/phytolog
image: /images/uitrees/homepage.jpg
stack: ["Django", "PostgreSQL", "JavaScript", "Tailwind CSS"]
youtubeLink: https://www.youtube.com/embed/nzRS95f5WOU
fullVideo: https://www.youtube.com/embed/VGAk1o3rU2I
summary: The project is a web application designed to document trees within areas. It aims to help identify trees and provide their taxonomic details, addressing the challenge of limited expertise in this field. Only authorized users with taxonomic knowledge can upload tree information. The process involves taking a picture of the tree, selecting its scientific name, filling in details, and automatically capturing its coordinates using JavaScript. For general users, the application provides search functionality. Users can perform a general search, which matches keywords across scientific, common, or local names, or a specific search, which allows filtering by criteria such as common name, local name, scientific name, location, or coordinates. If a tree is not found, users can request its identification, and authorized individuals will handle the request. The application is built using Django and related extensions.
---
Website: [Visit Web Page](https://tree-database.dharmzeey.com//)

Source Code: [GitHub](https://github.com/Dharmzeey/phytolog)

![image](/images/uitrees/homepage.jpg)
## **Home Page**

+ This is a web Application which is used to document trees in the vivinity of University of Ibadan. 

+ This was inspired by the need to identify trees, their taxonomic details but with limited people versed with the knowledge

- Only authorized users(Individuals with taxonomic knowledge) can upload trees and tree details
It works in a way that when a tree is located, 
- The picture of the tree is taken 
- The authorized user then proceed to upload 
![upload tree](/images/uitrees/upload.png)
## **Upload Page**
- Choses the tree scientific name and fills the information
- The coordinates gets atomatically filled with js
- Then Uploads the information

When a user (anyone) wants to search for tree name, they can general search or specify search
![general search](/images/uitrees/general-search.png)
## **General Search**
The general search returns any tree name that contains the search keyword, either from the scientific name, common name or local name
![specify search](/images/uitrees/specify-search.png)
## **Specify Search**
The specific search can either be 
- Common Name
- Local Name
- Scientific Name
- Location Name
- Coordinates (This field is has its input element attribute editable = false, so it will be auto filled by the javascript geolocation)

These will return result strictly based on the search restriction

- They get results depending on what they search
- If they do not see the result, they can request for the tree name of that location and the authorized individual recieve the request and do the necessary
![Tree Request](/images/uitrees/request-tree.png)
## **Request Tree Name**

Check out the web page [HERE](https://uitrees.up.railway.app)

## Frameworks
- Django
- Django Extension
- Django Cleanup

## Lbraries
- Font awesome
- Google fonts