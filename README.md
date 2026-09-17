# Librarymanagementsystem# Library Management System

## Project Overview

The Library Management System is a web-based application developed using Python and Flask. It is designed to manage books and library members in a simple and efficient way.

The system allows the user to add, view, edit, and delete book records. It also provides features for managing members, issuing books, and returning books.

## Objectives

- To manage library books digitally.
- To add and view book records.
- To update and delete book details.
- To manage library members.
- To issue books to members.
- To record returned books.
- To reduce manual work in library management.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Visual Studio Code
- Git and GitHub

## Features

### Dashboard
Provides an overview of the library system.

### Book Management
- Add books
- <img width="1098" height="358" alt="image" src="https://github.com/user-attachments/assets/bc6ecdd0-691a-42f7-b578-89c9e16c2ad7" />
- View books
- Edit book details
- Delete books

### Member Management
- Add members
- View members
- Edit member details
- Delete members

### Book Issue
Allows books to be issued to library members.

### Book Return
Allows issued books to be returned and records to be updated.

## CRUD Operations

| Operation | Description |
|---|---|
| Create | Add books and members |
| Read | View books and members |
| Update | Edit existing records |
| Delete | Delete records |

## Project Structure

```text
Library-Management-System/
│
├── app.py
├── library.db
│
├── templates/
│   ├── dashboard.html
│   ├── books.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── members.html
│   ├── add_members.html
│   ├── issue_book.html
│   └── return_book.html
│
├── static/
│   └── style.css
│
└── README.md
