# Implementing 2FA 

## Introduction
I always wondered how the logic behind entity authentication works. After taking up the course Cryptography and Network Security,
[21IS6C03] I learnt hashing, salting, entity authentication techniques etc.

This motivated me to start using 2FA on many platforms that had personal and important information like Gmail, Heroku, Github etc.
On a random day I felt like trying to implement my own 2FA system. 

## Implementation
I have used Flask for web interface.
To generate 2FA code I have user pytop libraries.

MySql seemed the best choice for storing auth data persistently.
To store 2FA codes temporarily until expiration or its intended use, I have used Redis.
Since Redis provides faster caching and access times along with temporary storage, it seemed the best choice. 

## Technologies used
- Flask
- MySql
- Redis
- Pyotp
- Bcrypt

## Features of my 2FA system
1. User registration through unique username or user email.
2. User login with 2FA. (user choice to otp for 2FA or not)
3. Password Reset (Mail service or backup code)
4. Backup code generation and storage.

## Future Scope
I will try to include famous Auth services like Google Authenticator or Microsoft Authenticator for 2FA code generation.

## Conclusion
This whole project from thought to implementation to deployment was a good experience to learn about database, data handling,
data security and a bit of web development too.
Special thanks to Dr. Suhaas K P for teaching the course Cryptography and Network Security and making it very interesting.
