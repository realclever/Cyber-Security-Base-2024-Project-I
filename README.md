## Cyber Security Base 2024 course Project I

## Project description 

This project is a simple implementation of the [Django starter website](https://docs.djangoproject.com/en/5.1/intro/tutorial01/). The application includes Django’s built-in registration for new users and a few other QoL improvements. The main focus is on finding and patching security issues rather than building and polishing the application itself.

The application has five security flaws from the OWASP 2021 Top Ten list. This application’s sole purpose is to demonstrate security flaws and it should not be used for other purposes.

## Installation

Clone the project

```
git clone https://github.com/realclever/Cyber-Security-Base-2024-Project-I.git
```

Move to the project folder

```
cd Cyber-Security-Base-2024-Project-I/mysite
```

Install requirements

```
python3 -m pip install -r requirements.txt
```

Apply migrations

```
python3 manage.py migrate
```

Start project

```
python3 manage.py runserver
```

Users

```Username: admin pw: adminpassword```

```Username: user pw: userpassword```


## Flaws

### FLAW 1: A00:2021 - Cross-Site Request Forgery (CSRF)

In short, CSRF is a web security vulnerability that allows an attacker to trick a user into performing unintended actions on a web application where they are authenticated. Fortunately, Django provides robust built-in CSRF protection. According to Django’s documentation, the primary protective measure is a middleware module that is activated by default. This module creates a unique token for each user session, which must be included in every form submission or POST request. The token is then cross-verified before processing the request.

In this project, the CSRF middleware is still included in ```settings.py```, but the voting view is made vulnerable by using the ```@csrf_exempt``` decorator. In addition, the ```{% csrf_token %}``` tag has been removed from the POST form in ```detail.html```.

CSRF middleware is included in ```settings.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L103

The vulnerable ```@csrf_exempt``` decorator in ```views.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/polls/views.py#L40

CSRF token in ```detail.html```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/polls/templates/polls/detail.html#L11


Preventing or addressing this vulnerability is straightforward: first, ensure that ```django.middleware.csrf.CsrfViewMiddleware``` is included in your ```settings.py``` file. Next, add the ```{% csrf_token %}``` tag to all templates that use POST forms. In this project, the intended fix is also commented in the vulnerable files: remove ```@csrf_exempt``` from the vote view and add ```{% csrf_token %}``` inside the POST form.

If absolutely necessary, you can mark views with the ```@csrf_exempt``` decorator, but this is not recommended.

### FLAW 2: A02:2021 - Broken Access Control

Broken access control is defined as “a critical security vulnerability that allows unauthorized users to access, modify, or delete data they should not have access to.” For example, here unauthorized users can access polls and modify them without permission, even though the application is designed so that only authenticated users can vote on polls created by the admin.

The vulnerable voting view and its fix in ```views.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/polls/views.py#L36

The vulnerability lies in URL manipulation. For example, navigating to a URL such as ```http://127.0.0.1:8000/polls/7/``` allows a user to access the voting page, even if they are not logged in. This can be prevented by adding the ```@login_required(login_url='/polls/login/')``` decorator to the ```views.py``` file. This decorator redirects unauthorized users to the login page if they attempt to manipulate polls (for example by voting without permission).

A more robust solution can also include user authentication checks in the template. For instance, in the ```polls/detail.html``` file, the condition ```{% if user.is_authenticated %}``` can be used to show the voting form only to authenticated users. However, this should only be used as an additional template level check. The main access control must be enforced in the view.

### FLAW 3: A03:2021 - Injection

In XSS attacks, an attacker injects malicious scripts into web pages viewed by other users. These scripts can execute various actions, such as stealing cookies, session tokens, or performing actions on behalf of the user. Although Django is widely recognized as a secure framework with built-in security measures against most common vulnerabilities, preventing XSS attacks is always tricky, and a more layered defense is always better.

In this project, the application is made vulnerable by rendering poll choice with the ```safe``` filter in ```detail.html```. This treats the content as trusted HTML instead of displaying it as plain text. As a result, if malicious script content is stored as a poll choice, it can be rendered and executed in the browser.

The vulnerable ```safe``` filter and its fix in ```detail.html```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/polls/templates/polls/detail.html#L16-L19

Content Security Policy (CSP) adds an extra layer of defense by helping to prevent XSS and data injection attacks by controlling what content is allowed to load on a website. In this project, CSP is included as an additional fix, but the main fix is to remove the ```safe``` filter so malicious scripts are shown as plain text instead of being executed.

CSP application/middleware in ```settings.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L84-L86

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L94-L96

CSP settings in ```settings.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L197-L206

Installing and configuring CSP was fairly straightforward. I went with the basic configuration that only allows sources from the same origin as the page ```(CSP_DEFAULT_SRC = ("'self'",))``` and applied the same setting for styles, scripts, images, and fonts. These are the most basic settings and can be configured according to the needs of any site and the required protection level.

### FLAW 4: A05:2021 - Security Misconfiguration

Security misconfiguration is one of the most common vulnerabilities. Critical settings such as ```SECRET_KEY```, ```DEBUG```, and ```ALLOWED_HOSTS``` should be properly managed to prevent security risks.

The vulnerable ```SECRET_KEY```, ```DEBUG```, and ```ALLOWED_HOSTS``` settings and their fixes in ```settings.py```

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L25-L40

- The ```SECRET_KEY``` parameter in ```settings.py``` is used for cryptographic signing and should always remain confidential. Avoid hardcoding the value directly in ```settings.py```. Instead, store the parameter in environment variables.

- The ```DEBUG``` setting should always be turned off when deploying a site to production. Leaving it enabled could expose detailed error messages that reveal vulnerabilities in the application.

- The ```ALLOWED_HOSTS``` setting should also be restricted in production. Leaving it empty or incorrectly configured can cause deployment issues or weaken host header validation. In production, it should contain only the hostnames or domains that are allowed to serve the application.

To simplify managing these settings, the fix uses the ```Python-decouple``` library. This library allows you to store critical configuration values in a separate file, ensuring they remain confidential. Many developers are familiar with the ```Python-dotenv``` library, which reads key-value pairs from a ```.env``` file and sets them as environment variables. The fix adopts a similar approach here using Decouple. Storing the ```SECRET_KEY``` and the ```DEBUG``` setting in a ```.env``` file, rather than directly in ```settings.py```, is considered good practice.

### FLAW 5: A09:2021 - Security Logging and Monitoring Failures

Security logging and monitoring failures are described as "vulnerabilities that occur when a system or application fails to log or monitor security events properly. This can allow attackers to gain unauthorized access to systems and data without detection." In this application, by default, admins or unauthorized users can perform any action without leaving traces, such as manipulating data or attempting to hack the system.

The disabled logging and monitoring settings and their fixes in ```settings.py```

```Admin-logs``` and ```django-axes``` configuration

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L46-L65

Logging and monitoring applications/middleware

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L78-L82

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L108-L115

```Django-axes``` authentication backend

https://github.com/realclever/Cyber-Security-Base-2024-Project-I/blob/main/mysite/mysite/settings.py#L148-L153


To address this, the fix uses three different, but similar, packages to mitigate some of the issues ```Django-axes```, ```Django-admin-logs```, and ```Django-user-visit```. All of these provide security monitoring via the admin panel at ```127.0.0.1:8000/admin/```, along with countermeasures such as locking accounts after a certain number of failed login attempts.

- ```Django-admin-logs``` automatically logs entries whenever a user adds, changes, or deletes objects through the admin interface.
- ```Django-user-visit``` logs all successful logins and displays information such as the username, hash, timestamp, session key, remote address, and OS.
- ```Django-axes``` is similar to ```Django-user-visit```, but it also tracks suspicious login attempts and includes features like cooldown periods, IP address allowlisting and blocklisting, and user account allowlisting.

While ```Django-user-visit``` and ```Django-axes``` function similarly, ```Django-axes``` includes the same features as ```Django-user-visit```, but with additional functionality and more detailed tracking.