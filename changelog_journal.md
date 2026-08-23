# UNIVERSITY OF LONDON

# BCs Computer Science

# CM3070 - Final Project

## Template 
# IL-Hub Changelog

All notable changes to the project are documented in this file, following an incremental implementation process where each milestone introduces a functional component of the architecture.

---

# v0.1.0 - Initial Project Structure
Date: 2026-06-28
Commit: c18553b - "first w10 prototype"

## Added
- Django basic project skeleton.
- Development environment configuration.
- Custom User model replacing Django's default username authentication.
- Email-based authentication.
- Initial IL-Hub application structure.
- Initial Client (simulated).
- Basic URL routing.
- Basic HTML templates.
- Basic OAuth 2.0 implementation.

## Notes

First release for Week 10 midterm prototype. The goal is to test the basic communication between IL-Hub and clients. 
Both apps live in the same Django's project and also sharing the database. However, the authorization flow is strictly using Django Oauth Toolikt library,
and user's data are shared through the API.
User's data is hardcoded inside the API (context_profile function).
Custom User model is implemented so that Authentication now uses email as the unique identifier. 
The project models identity using email as the primary identifier, which better reflects modern Identity Providers and simplifies OAuth integration. Since email address will be managed by the system (see Section Scope of Work), it is a reliable identifier.
The prototype is working well, tokens are well generated and using SESSION_COOKIE_AGE = 90 allows to test whether the system is revoking bearer tokens properly.

---

# v0.2.0
Date: 2026-07-06
Commit: f8899d1 - feature: il-hub data model created

## Added

- IL-Hub data model tables:
    - LibraryContext -> User's data that IL-Hub will be send to Library client
    - LibraryInterestTopics -> Many to many relationship with LibraryContext so that arbitrary topics can be created
    - BlogContext -> User's data that IL-Hub will be send to Blog client
    - BlogTopics -> Many to many relationship with BlogContext so that arbitrary topics can be created
- Admin panel to manage topics 

## Notes

The rationale behind this design, is to keep isolated tables for each client, seeking for a simple design. LibraryInterestTopics and BlogTopics are tables that must be matched with expected data payload expected by clients. This create a strong coupling between the IL-Hub and clients, but it is acceptable due to it is a federated ecosystem and all apps belong to the institution.
UUID registry is used as unique user identifier. Each client receives the uuid that they must store to track their users in their own user table. This approach share to all clients the same user identifier. This could be a issue that can be improved implementing some pairwise identifiers registry.

# v0.2.1
Date: 2026-07-16
Commit: c04d83c

## Added

- Client Registry ->  Each client has a register where is indicated the tables and attributes that should be fetched. The idea is to avoid traversing tables dinamically, instead, detailing all the (previously agreed between client and hub) data expected by the client. This is part of the coupling detailed before, but also a secure way to interact between applications.
The implementation is done through a client registration dictionary where the data and attributes to be obtained come from (also the model and serializer). This approach avoid using the database to register the data for differente reasons. First, because the amount of clients expected should mantain relatively stable over the time. Second, the registry contains models and serializers that must be executed, therefore storing in a database implies that some form of conversion between database and code must be implemented, which is ultimately inconvenient and hard to mantain. The dictionary structure can be modified, read and shared with clients in a consistent way. 
A possible mitigation could be creating a json filed in the database as a back-up.

- Serializers -> all contextual data is serialized before sending through the api.
- Data model -> uuid as a shared identifier. 

---

# v0.2.2
Date 2026-07-18
Commit: 806f2de

## Added 

- Custom error handling for client-server interaction -> api_errors.py details the custom API exceptions to improve the response to clients. Since the token validation relies on Django Oauth Toolkit, these exceptions cover steps after access token is validated by DOT, for example, checking wheter the client is registered and active in the ClientRegistry model. Basic testing was performed with curl, changing token states on django admin panel. In further steps a more comprehensive set of tests will need to be developed.

---

# v0.2.3
Date: 2026-07-22
Commit: 7565d37

## Added

- Looking for improving security aspect, I've implemented changes in ContextProfileView. there are four specifications: 
    1. Explicitly declaration of http method. GET method is the only allowed. 
    2. Enforcing authentication through OAuth2, because the endpoint is specifically to be reached by apps (clients)
    3. Permission is granted only using tokens and scope (checks that the token has the endpoint's required permissions)
    4. Scope has a strict definition: Only read.


# V0.2.4
Date: 2026-07-26
Commit: 12f7749

## Added

- A custom logging system implemented to, initially, register the most important events related to GDPR compliance:
    1. LOGIN_SUCCEEDED --> Resource Owner accessing to IL-Hub
    2. PROFILE_ACCESSED --> Client requesting user's data
    3. PROFILE_UPDATED --> Resource Owner modifying personal data
  
  Custom log payload is an effort to be a nice to read JSON file.
  Actors and outcome types were defined with the aim of achieving a simple logging structure.

# V0.2.5
Date: 2026-08-05
Commit: 00b2b2b (social-login branch)

## Added:

- Social login implemented using django-allauth. Aligned with the requirements:
    1. New users cannot register using Google social login or the classic Django email/password
    2. Users can sign in using either social login or Django email/password

- The recommended configuration was used since it is not the core part of the project.
- Allauth templates were overrided

# V0.2.6
Date: 2026-08-18
Commit: a6f5de0 (frontend branch)

## Added:

- Full IL-Hub dashboard frontend 
- Profile update forms.
- Implementation with Django templates and HTMX.

# V0.2.7
Date: 2026-08-18
Commit: 4dc6540

## Added:

- A set of tests implemented for system assesment. It includes three main aspects:
    1. API profile retrieval
    2. user interface, using Selenium
    3. user authentication (Google social auth excluded)

# V0.2.8
Date: 2026-08-22
Commit: 7c62384

## Added:

- script traceability_parser.py that helps to test the traceability of audit logs. 

