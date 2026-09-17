import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import html

DATABASE = "library.db"


# =========================
# DATABASE
# =========================

def connect_database():
    return sqlite3.connect(DATABASE)


def create_database():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT NOT NULL,
            category TEXT NOT NULL,
            year INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# HTML HEADER
# =========================

def page_start(title):

    return f"""
    <!DOCTYPE html>
    <html>
    <head>

        <title>{title}</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #eef1f5;
                color: #333;
            }}

            .dashboard {{
                display: flex;
                min-height: 100vh;
            }}

            .sidebar {{
                width: 240px;
                background: #20252b;
                color: white;
                padding: 25px 15px;
            }}

            .sidebar h2 {{
                text-align: center;
                margin-bottom: 35px;
            }}

            .sidebar a {{
                display: block;
                color: white;
                text-decoration: none;
                padding: 14px;
                margin: 5px 0;
                border-radius: 6px;
            }}

            .sidebar a:hover {{
                background: #3d454e;
            }}

            .main {{
                flex: 1;
                padding: 30px;
            }}

            .topbar {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
            }}

            .cards {{
                display: grid;
                grid-template-columns:
                    repeat(4, 1fr);
                gap: 20px;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 8px;
                box-shadow:
                    0 2px 8px rgba(0,0,0,0.08);
            }}

            .card h3 {{
                margin-top: 0;
                color: #666;
            }}

            .card p {{
                font-size: 32px;
                font-weight: bold;
            }}

            .actions {{
                margin-top: 30px;
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}

            .button {{
                display: inline-block;
                padding: 12px 18px;
                background: #20252b;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}

            .page {{
                max-width: 1100px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: center;
            }}

            th {{
                background: #20252b;
                color: white;
            }}

            input, select {{
                width: 100%;
                padding: 12px;
                margin: 8px 0 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}

            button {{
                padding: 12px 20px;
                background: #20252b;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}

            .form {{
                max-width: 500px;
                margin: auto;
            }}

            .edit {{
                color: #333;
                margin-right: 10px;
            }}

            .delete {{
                color: #b00020;
            }}

            @media(max-width: 800px) {{
                .cards {{
                    grid-template-columns:
                        repeat(2, 1fr);
                }}

                .sidebar {{
                    width: 190px;
                }}
            }}

        </style>

    </head>

    <body>
    """


def page_end():

    return """
    </body>
    </html>
    """


# =========================
# DASHBOARD
# =========================

def dashboard_page():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(quantity),0) FROM books"
    )
    available_books = cursor.fetchone()[0]

    conn.close()

    return page_start("Library Dashboard") + f"""

    <div class="dashboard">

        <div class="sidebar">

            <h2>📚 Library</h2>

            <a href="/">🏠 Dashboard</a>

            <a href="/books">📖 Books</a>

            <a href="/add-book">➕ Add Book</a>

            <a href="/members">👥 Members</a>

            <a href="/add-member">➕ Add Member</a>

        </div>


        <div class="main">

            <div class="topbar">

                <h1>
                    Library Management System
                </h1>

                <p>
                    Welcome to the Library Dashboard
                </p>

            </div>


            <div class="cards">

                <div class="card">
                    <h3>Total Books</h3>
                    <p>{total_books}</p>
                </div>

                <div class="card">
                    <h3>Total Members</h3>
                    <p>{total_members}</p>
                </div>

                <div class="card">
                    <h3>Available Books</h3>
                    <p>{available_books}</p>
                </div>

                <div class="card">
                    <h3>Library Status</h3>
                    <p>Active</p>
                </div>

            </div>


            <h2>Quick Actions</h2>

            <div class="actions">

                <a class="button"
                   href="/add-book">
                    Add Book
                </a>

                <a class="button"
                   href="/books">
                    View Books
                </a>

                <a class="button"
                   href="/add-member">
                    Add Member
                </a>

                <a class="button"
                   href="/members">
                    View Members
                </a>

            </div>

        </div>

    </div>

    """ + page_end()


# =========================
# BOOK LIST
# =========================

def books_page():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, author,
               publisher, category,
               year, quantity
        FROM books
        ORDER BY id DESC
    """)

    books = cursor.fetchall()

    conn.close()

    rows = ""

    for book in books:

        rows += f"""
        <tr>

            <td>{book[0]}</td>
            <td>{html.escape(book[1])}</td>
            <td>{html.escape(book[2])}</td>
            <td>{html.escape(book[3])}</td>
            <td>{html.escape(book[4])}</td>
            <td>{book[5]}</td>
            <td>{book[6]}</td>

            <td>

                <a class="edit"
                   href="/edit-book?id={book[0]}">
                   Edit
                </a>

                <a class="delete"
                   href="/delete-book?id={book[0]}"
                   onclick="return confirm('Delete this book?')">
                   Delete
                </a>

            </td>

        </tr>
        """


    return page_start("Books") + f"""

    <div class="page">

        <h1>Book Management</h1>

        <a class="button"
           href="/add-book">
           + Add Book
        </a>

        <table>

            <tr>

                <th>ID</th>
                <th>Title</th>
                <th>Author</th>
                <th>Publisher</th>
                <th>Category</th>
                <th>Year</th>
                <th>Quantity</th>
                <th>Actions</th>

            </tr>

            {rows}

        </table>

        <br>

        <a class="button" href="/">
            ← Dashboard
        </a>

    </div>

    """ + page_end()


# =========================
# ADD BOOK
# =========================

def add_book_page():

    return page_start("Add Book") + """

    <div class="page">

        <div class="form">

            <h1>Add New Book</h1>

            <form method="POST"
                  action="/add-book">

                <label>Book Title</label>

                <input type="text"
                       name="title"
                       required>


                <label>Author</label>

                <input type="text"
                       name="author"
                       required>


                <label>Publisher</label>

                <input type="text"
                       name="publisher"
                       required>


                <label>Category</label>

                <input type="text"
                       name="category"
                       required>


                <label>Publication Year</label>

                <input type="number"
                       name="year"
                       required>


                <label>Quantity</label>

                <input type="number"
                       name="quantity"
                       min="1"
                       required>


                <button type="submit">
                    Add Book
                </button>

            </form>

            <br>

            <a class="button"
               href="/books">
               Back
            </a>

        </div>

    </div>

    """ + page_end()


# =========================
# EDIT BOOK
# =========================

def edit_book_page(book_id):

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    conn.close()

    if book is None:

        return "Book not found."


    return page_start("Edit Book") + f"""

    <div class="page">

        <div class="form">

            <h1>Edit Book</h1>

            <form method="POST"
                  action="/edit-book?id={book_id}">

                <label>Book Title</label>

                <input type="text"
                       name="title"
                       value="{html.escape(book[1])}"
                       required>


                <label>Author</label>

                <input type="text"
                       name="author"
                       value="{html.escape(book[2])}"
                       required>


                <label>Publisher</label>

                <input type="text"
                       name="publisher"
                       value="{html.escape(book[3])}"
                       required>


                <label>Category</label>

                <input type="text"
                       name="category"
                       value="{html.escape(book[4])}"
                       required>


                <label>Publication Year</label>

                <input type="number"
                       name="year"
                       value="{book[5]}"
                       required>


                <label>Quantity</label>

                <input type="number"
                       name="quantity"
                       value="{book[6]}"
                       required>


                <button type="submit">
                    Update Book
                </button>

            </form>

            <br>

            <a class="button"
               href="/books">
               Back
            </a>

        </div>

    </div>

    """ + page_end()


# =========================
# MEMBERS
# =========================

def members_page():

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, phone
        FROM members
        ORDER BY id DESC
    """)

    members = cursor.fetchall()

    conn.close()

    rows = ""

    for member in members:

        rows += f"""
        <tr>

            <td>{member[0]}</td>

            <td>
                {html.escape(member[1])}
            </td>

            <td>
                {html.escape(member[2])}
            </td>

            <td>
                {html.escape(member[3])}
            </td>

            <td>

                <a class="delete"
                   href="/delete-member?id={member[0]}"
                   onclick="return confirm('Delete this member?')">
                   Delete
                </a>

            </td>

        </tr>
        """


    return page_start("Members") + f"""

    <div class="page">

        <h1>Member Management</h1>

        <a class="button"
           href="/add-member">
           + Add Member
        </a>

        <table>

            <tr>

                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Action</th>

            </tr>

            {rows}

        </table>

        <br>

        <a class="button" href="/">
            ← Dashboard
        </a>

    </div>

    """ + page_end()


# =========================
# ADD MEMBER
# =========================

def add_member_page():

    return page_start("Add Member") + """

    <div class="page">

        <div class="form">

            <h1>Add Member</h1>

            <form method="POST"
                  action="/add-member">

                <label>Name</label>

                <input type="text"
                       name="name"
                       required>


                <label>Email</label>

                <input type="email"
                       name="email"
                       required>


                <label>Phone</label>

                <input type="text"
                       name="phone"
                       required>


                <button type="submit">
                    Add Member
                </button>

            </form>

            <br>

            <a class="button"
               href="/members">
               Back
            </a>

        </div>

    </div>

    """ + page_end()


# =========================
# REQUEST HANDLER
# =========================

class LibraryServer(BaseHTTPRequestHandler):


    def send_html(self, content):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            content.encode("utf-8")
        )


    def redirect(self, location):

        self.send_response(302)

        self.send_header(
            "Location",
            location
        )

        self.end_headers()


    def get_data(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )

        body = self.rfile.read(length).decode()

        return parse_qs(body)


    def do_GET(self):

        path = self.path.split("?")[0]

        query = {}

        if "?" in self.path:

            query_string = self.path.split("?")[1]

            query = parse_qs(query_string)


        if path == "/":

            self.send_html(
                dashboard_page()
            )


        elif path == "/books":

            self.send_html(
                books_page()
            )


        elif path == "/add-book":

            self.send_html(
                add_book_page()
            )


        elif path == "/edit-book":

            book_id = int(
                query["id"][0]
            )

            self.send_html(
                edit_book_page(book_id)
            )


        elif path == "/delete-book":

            book_id = int(
                query["id"][0]
            )

            conn = connect_database()

            conn.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,)
            )

            conn.commit()
            conn.close()

            self.redirect("/books")


        elif path == "/members":

            self.send_html(
                members_page()
            )


        elif path == "/add-member":

            self.send_html(
                add_member_page()
            )


        elif path == "/delete-member":

            member_id = int(
                query["id"][0]
            )

            conn = connect_database()

            conn.execute(
                "DELETE FROM members WHERE id = ?",
                (member_id,)
            )

            conn.commit()
            conn.close()

            self.redirect("/members")


        else:

            self.send_response(404)

            self.end_headers()

            self.wfile.write(
                b"404 - Page Not Found"
            )


    def do_POST(self):

        path = self.path.split("?")[0]

        data = self.get_data()


        if path == "/add-book":

            title = data["title"][0]
            author = data["author"][0]
            publisher = data["publisher"][0]
            category = data["category"][0]
            year = data["year"][0]
            quantity = data["quantity"][0]

            conn = connect_database()

            conn.execute("""
                INSERT INTO books
                (title, author, publisher,
                 category, year, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                title,
                author,
                publisher,
                category,
                year,
                quantity
            ))

            conn.commit()
            conn.close()

            self.redirect("/books")


        elif path == "/edit-book":

            query_string = self.path.split("?")[1]

            query = parse_qs(query_string)

            book_id = int(
                query["id"][0]
            )

            title = data["title"][0]
            author = data["author"][0]
            publisher = data["publisher"][0]
            category = data["category"][0]
            year = data["year"][0]
            quantity = data["quantity"][0]

            conn = connect_database()

            conn.execute("""
                UPDATE books

                SET title = ?,
                    author = ?,
                    publisher = ?,
                    category = ?,
                    year = ?,
                    quantity = ?

                WHERE id = ?
            """, (
                title,
                author,
                publisher,
                category,
                year,
                quantity,
                book_id
            ))

            conn.commit()
            conn.close()

            self.redirect("/books")


        elif path == "/add-member":

            name = data["name"][0]
            email = data["email"][0]
            phone = data["phone"][0]

            conn = connect_database()

            conn.execute("""
                INSERT INTO members
                (name, email, phone)
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                phone
            ))

            conn.commit()
            conn.close()

            self.redirect("/members")


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    create_database()

    server = HTTPServer(
        ("localhost", 8000),
        LibraryServer
    )

    print("----------------------------------")
    print(" Library Management System")
    print("----------------------------------")
    print("Server started successfully!")
    print("Open: http://localhost:8000")
    print("----------------------------------")

    server.serve_forever()
