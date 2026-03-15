# Database Schema for News Website

## Collections:
- **Users**  
  - `_id`: ObjectId
  - `username`: String
  - `email`: String
  - `password`: String

- **Articles**  
  - `_id`: ObjectId
  - `title`: String
  - `content`: String
  - `authorId`: ObjectId (reference to Users)
  - `publishedDate`: Date

- **Comments**  
  - `_id`: ObjectId
  - `articleId`: ObjectId (reference to Articles)
  - `authorId`: ObjectId (reference to Users)
  - `content`: String
  - `createdAt`: Date

## Relationships:
- One User can have multiple Articles (one-to-many).
- One Article can have multiple Comments (one-to-many).