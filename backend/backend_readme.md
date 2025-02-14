# servEase Backend

This repository contains the backend for **servEase**, a community-driven app connecting consumers with local service providers. Built using Flask, this backend manages the core functionalities of the platform, including user authentication, service requests, quotes, and provider-consumer interactions.

---

##  Tech Stack

- **Framework:** Flask  
- **Database:** Firebase Firestore  
- **Authentication:** Firebase Authentication (JWT-based secure login for users).  
- **Hosting:** Flask server hosted on Railway.  
- **Python Version:** 3.13

---

##  Features

1. **User Authentication**  
   - Secure login and registration using Firebase Authentication.  
   - Role-based access for Consumers and Service Providers.

2. **Service Request Management**  
   - APIs for creating, updating, and deleting service requests.  
   - Fetch open service requests for service providers.

3. **Dynamic Quoting System**  
   - Service providers can submit quotes for a consumer's request.  
   - Consumers can view and accept quotes.

4. **Review and Rating System**  
   - Consumers can rate and review service providers after a job is completed.

5. **Real-Time Updates**  
   - Firebase Firestore ensures instant updates to requests, quotes, and statuses.



