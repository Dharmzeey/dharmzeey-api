---
title: Abuad Farm
slug: abuad-farm
category: Web Application
intro: Web Application for manufacturing company.
url: https://abuadfarm.up.railway.app
github: https://github.com/Dharmzeey/ABUADFarm
image: /images/abuadfarm/Admin-home.png
stack: ["Django", "Django REST", "Tailwind CSS", "AmCharts JS"]
youtubeLink: https://www.youtube.com/embed/m7tt7HRKY-4
fullVideo: https://www.youtube.com/embed/ZQgALAhBvow
summary: ABUAD Farm is a web application built using Django and Django template, designed to mock a manufacturing company need. It also features vanilla JavaScript and Tailwind CSS for the frontend. The application provides role-based access control, offering distinct functionalities for Admins, Staff, and Users. Admins have full control over the system, including managing units, customers, and messages through the Django Admin Panel. Staff members have limited access, focusing on unit-specific data and customer interactions, while Users can access personal dashboards, notifications, and purchase history. The platform includes various pages such as a Home Page, Units Page, About Page, Blog Page, and dashboards with intuitive chart. Technologies like Django-Allauth, AmCharts JS, and Tailwind CSS are utilized, with charts powered by AmCharts JS. Demo credentials are available for testing the User Panel.
---


Website: [Visit Web Page](https://abuadfarm.up.railway.app/)

**I removed all pictures(and replaced it with same dummy images) and painted the names because of some reasons**

# ABUAD Farm

The Idea is as a result of where I was posted to do my IT, so the organization is a Farm and also a manufacturing company, they make different products from their farm produce.

They have different units and they produce different products at each units I then decided to build something channeling my focus to the mode of operation.

I designed this web Application on the foundation of a Manufacturing Company.
It is a Django Project, which I also used djangorestframework for some serialization.
I used vanilla Js and Tailwind CSS(django-tailwind)
Django-Allauth was used for the authentication 

It has different Apps that handled different functionalities

![image](/images/abuadfarm/Home-page.png)
## **Home Page**
![image](/images/abuadfarm/units.png)
## **Units Page**
![image](/images/abuadfarm/about.png)
## **About Page**
![image](/images/abuadfarm/blog.png)
## **Blog Page**


# ADMIN
**The Admin is a Django superuser who has full access to the Django Admin Panel and also to all the units and products and all customers both in the Django Admin Panel and the other Admin Page** 
## The Admin can:
- Can view all the Units.
- Can view all the customers on the Database, regardless of the unit they have made purchase from 
- Can see all messages sent to all customers 
![image](/images/abuadfarm/Admin-home.png)
## **Admin Home Page**


- Ultimately, can have access to all the features, models and everything of the Django Admin panel and also perform CRUD operations on everything in the Django Admin Panel 

![image](/images/abuadfarm/Admin-customers.png)
## **Customers**

# STAFFS
**The Staffs is also Django Staff, they only have restricted access to the models and customers concerning their units alone and has restricted access to the Django Admin panel.**
![image](/images/abuadfarm/staff-home.png)
## **Staff Homepage**
- These are the users that have been assigned to each units in the company 
### Their Staffs status was created by the superuser (Admin) in the Admin panel 
## Staffs Can:
- View all the customers that made purchase from their units 
- Send message to each customers who has made purchase from their units 
- Add customers product purchase for each customer who made purchase from their units 

# USERS

**Customers only have access to their accounts alone(which contains all the units they made purchases)**
**All accounts created have user and  profiles model**
**But they are later given different statuses**
- Users are customers who created account and made purchase from any unit 
## Users can:
- Have access to their Dashboard, Messages, Notifications and Profiles 
![image](/images/abuadfarm/user-dashboard.png)
## **User Dashboard**

All the charts on the webpage (Admin Home, Customer Details and User Dashboard) are accomplished with [Amcharts js](https://www.amcharts.com/) and the data passed are serialized with [Djangorestframework](https://www.django-rest-framework.org/) Serializer

***
## Frameworks
- Django
* Django-allauth 
+ DjangorestFramwork
- Django-Tailwind 
***
## Lbraries
- Amcharts js 
- Tailwind
- Font awesome
- Google fonts

**If you want to gain access to the User (Customer) Panel**
**Click Account and login with this details**

 ( Username: Testing, 
  Password: Herokuapp )