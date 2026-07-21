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
Date 2026-0718
Commit: 806f2de

## Added 

- Custom error handling for client-server interaction -> api_errors.py details the custom API exceptions to improve the response to clients. Since the token validation relies on Django Oauth Toolkit, these exceptions cover steps after access token is validated by DOT, for example, checking wheter the client is registered and active in the ClientRegistry model. Basic testing was performed with curl, changing token states on django admin panel. In further steps a more comprehensive set of tests will need to be developed.


