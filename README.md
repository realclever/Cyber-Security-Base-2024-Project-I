## Cyber Security Base 2024 course Project I

## Project description 

This project is a simple implementation of the [Django starter website](https://docs.djangoproject.com/en/5.1/intro/tutorial01/). The application includes Django’s built-in registration for new users and a few other QOL improvements. Only admins can create polls and authenticated users can view and vote them. The application has five security flaws from the OWASP 2021 Top Ten list. This applications sole purpose is to demonstrate security flaws and shouldn’t be used for other purposes. 

## Installing project

*text here*

## Flaws

### FLAW 1: A00:2021 - Cross-Site Request Forgery (CSRF)

In short, CSRF is a web security vulnerability that allows an attacker to trick a user into performing unintended actions on a web application where they are authenticated. Fortunately, Django provides robust built-in CSRF protection. According to Django’s documentation, the primary protective measure is a middleware module that is activated by default. This module creates a unique token for each user session, which must be included in every form submission or POST request. The token is then cross-verified before processing the request.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/7c4ae590de6a69e90f6db6152835c673dd74ec9c/mysite/mysite/settings.py#L76

I've included ```{% csrf_token %}``` decorator to all my ```.html``` files found on [```templates```](https://github.com/realclever/Cyber-Security-Base-2024-Project-I/tree/main/mysite/polls/templates) folder.


As mentioned earlier, CSRF protection is enabled by default. Preventing or addressing this vulnerability is straightforward: first, ensure that ```django.middleware.csrf.CsrfViewMiddleware``` is included in your ```settings.py``` file. Next, add the ```{% csrf_token %}``` tag to all templates that use POST forms. If the middleware is present but the POST form is missing the ```{% csrf_token %}``` tag, you will encounter an HTTP 403 error with the message: “CSRF verification failed. Request aborted.”

Even though the default method for HTML forms is GET, it is good practice to include CSRF tokens in all forms, including GET and POST forms. If necessary, you can mark views with the ```@csrf_exempt``` decorator, but this is not recommended.

### FLAW 2: A02:2021 - Broken Access Control

Broken access control is defined as “a critical security vulnerability that allows unauthorized users to access, modify, or delete data they should not have access to.” For example, consider a simple web application where unauthorized users can access polls and modify them without permission, even though the application is designed so only logged-in users can vote on polls created by the admin.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/7c4ae590de6a69e90f6db6152835c673dd74ec9c/mysite/polls/templates/polls/detail.html#L20

The vulnerability lies in URL manipulation. For example, navigating to a URL such as ```http://127.0.0.1:8000/polls/6/``` allows user to access the voting page, even if they are not logged in. This can be prevented by adding the ```@login_required(login_url='/polls/login/')``` decorator to the ```views.py``` file. This decorator redirects unauthorized users to the login page if they attempt to manipulate polls (e.g., vote without permission).

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/7c4ae590de6a69e90f6db6152835c673dd74ec9c/mysite/polls/views.py#L30

However, while the user may still be able to access the URL, a more robust solution involves adding user authentication checks in the template. For instance, in the ```polls/detail.html``` file, you can include the condition ```{% if user.is_authenticated %}```. If the user is not authenticated, they cannot access the URL, and an error message will be displayed.

### FLAW 3: A03:2021 - Injection

in XSS attacks, an attacker injects malicious scripts into web pages viewed by other users. These scripts can execute various actions, such as stealing cookies, session tokens, or performing actions on behalf of the user. Although Django is widely recognized as a secure framework with built-in security measures against most common vulnerabilities, preventing XSS attacks is always tricky, and a more layered defense is always better.
Content Security Policy (CSP) adds an extra layer of defense by helping to prevent XSS and data injection attacks by controlling what content is allowed to load on a website.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/beae2c8da81175041b41db604226ccde6582a6b4/mysite/mysite/settings.py#L171

Installing and configuring CSP was fairly straightforward. I went with the most basic configuration that only allows sources from the same origin as the page ```(CSP_DEFAULT_SRC = ("'self'",))``` and applied the same setting for styles, scripts, images, and fonts. These are the most basic settings and can be tailored for the needs of any site and the protection level you want to achieve. After doing more research on CSP, I learned that it is so robust that Django is considering making it a built-in feature in the future.

### FLAW 4: A05:2021 - Security Misconfiguration

Security misconfiguration is one of the most common vulnerabilities. Critical settings such as ```SECRET_KEY``` and ```DEBUG``` should be properly managed to prevent security risks.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/beae2c8da81175041b41db604226ccde6582a6b4/mysite/mysite/settings.py#L25

- The ```SECRET_KEY``` parameter in settings.py is used for cryptographic signing and should always remain confidential. Avoid hardcoding the value directly in ```settings.py```. Instead, store the parameter in environment variables as a best practice.

- Similarly, the ```DEBUG``` setting (default value: False) should always be turned off when deploying a site to production. Leaving it enabled could expose detailed error messages that reveal vulnerabilities in the application.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/beae2c8da81175041b41db604226ccde6582a6b4/mysite/.env#L1

To simplify managing these settings, I used the ```Python-decouple``` library. This library allows you to store critical configuration values in a separate file, ensuring they remain confidential. Many developers are familiar with the ```Python-dotenv``` library, which reads key-value pairs from a ```.env``` file and sets them as environment variables. I adopted a similar approach here using Decouple. Storing the ```SECRET_KEY``` and the ```DEBUG``` setting in a ```.env``` file, rather than directly in ```settings.py```, is considered good practice.


### FLAW 5: A09:2021 - Security Logging and Monitoring Failures

Security logging and monitoring failures are described as "vulnerabilities that occur when a system or application fails to log or monitor security events properly. This can allow attackers to gain unauthorized access to systems and data without detection." In this application, by default, admins or unauthorized users can perform any action without leaving traces, such as manipulating data or attempting to hack the system.

To address this, I added three different, but similar, packages to mitigate some of the issues: ```Django-axes, Django-admin-logs, and Django-user-visit```. All of these provide security monitoring via the admin panel at ```127.0.0.1:8000/admin/```, along with countermeasures such as locking accounts after a certain number of failed login attempts.

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/beae2c8da81175041b41db604226ccde6582a6b4/mysite/mysite/settings.py#L37

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/623808a9b2e889ffabb6be9d1e758d4abcc3a939/mysite/mysite/settings.py#L48

- ```Django-admin-logs``` automatically logs entries whenever a user adds, changes, or deletes objects through the admin interface.
- ```Django-user-visit``` logs all successful logins and displays information such as the username, hash, timestamp, session key, remote address, and OS.
- ```Django-axes``` is similar to ```Django-user-visit```, but it also tracks suspicious login attempts and includes features like cooldown periods, IP address allowlisting and blocklisting, and user account allowlisting.

While ```Django-user-visit``` and ```Django-axes``` function similarly, ```Django-axes``` includes the same features as ```Django-user-visit```, but with additional functionality and more detailed tracking.
