# site-library
This repository was created to store a website that will demonstrate my work using the Django framework.

The site conditionally belongs to a library containing paper books.
At the moment, the main page of the site displays only a list of registered books (the list items are links).
Books that are currently in the readers possession are marked "out of stock".
The page contains a search form by title and author.
Clicking on the link opens a page with a more detailed description of the book.

The website has added functionality for user registration, authorization (login and password) and 
password recovery by email (configured for the console backend).

Three user groups have been created: the recruter for registration of library staff (рекрутер), the registrar 
for registration of readers (регистратор), and the librarian for registration of books (библиотекарь).
After authorization, recruiters can register new employees on the site.
Registrars can register new readers on the site after authorization.
Librarians can register: new books on the site and the date of issue of books to people.

Superuser (only he has access to the admin-panel) login: "super", password: "12345".