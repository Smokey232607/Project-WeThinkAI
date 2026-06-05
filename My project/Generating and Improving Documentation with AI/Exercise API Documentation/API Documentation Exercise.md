# API Documentation Exercise — My Submission

---

For this exercise, I chose **Option C: Python/Flask User Registration API** because I have been learning Python lately and I wanted to practice documenting something I actually understand. I also picked **Markdown** for Prompt 2 because it is the format I see most often on GitHub and it just feels natural to me.

---

# Part 1: Original API Endpoint Code (What I Started With)

This is the Python/Flask code from the exercise that I decided to document:

```python
@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': f'{field} is required'
            }), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'error': 'Username taken',
            'message': 'Username is already in use'
        }), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'Email exists',
            'message': 'An account with this email already exists'
        }), 409

    # Validate email format
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data['email']):
        return jsonify({
            'error': 'Invalid email',
            'message': 'Please provide a valid email address'
        }), 400

    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({
            'error': 'Weak password',
            'message': 'Password must be at least 8 characters long'
        }), 400

    # Create new user
    try:
        # Hash password
        password_hash = generate_password_hash(data['password'])

        # Create user object
        new_user = User(
            username=data['username'],
            email=data['email'].lower(),
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            role='user'
        )

        # Add user to database
        db.session.add(new_user)
        db.session.commit()

        # Generate confirmation token
        confirmation_token = generate_confirmation_token(new_user.id)

        # Send confirmation email
        try:
            send_confirmation_email(new_user.email, confirmation_token)
        except Exception as e:
            # Log email error but continue
            app.logger.error(f"Failed to send confirmation email: {str(e)}")

        # Create response without password
        user_data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_at': new_user.created_at.isoformat(),
            'role': new_user.role
        }

        return jsonify({
            'message': 'User registered successfully',
            'user': user_data
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error registering user: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'Failed to register user'
        }), 500
```

---

# Part 2: Prompt 1 — My Comprehensive Endpoint Documentation

## User Registration API

### Endpoint
`POST /api/users/register`

### What It Does
This endpoint lets someone create a new user account. When you send it a username, email, and password, it checks if everything is valid, makes sure nobody else already has that username or email, hashes the password so it is secure, saves the user to the database, sends a confirmation email, and then sends back the new user's info (but not the password).

### Authentication
You do not need to log in or have any special key to use this. It is completely public because it is for brand new users who do not have accounts yet.

### Request Parameters

#### Body Parameters (JSON)

| Parameter  | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `username` | String | Yes      | A unique username for the account    |
| `email`    | String | Yes      | A real email address                 |
| `password` | String | Yes      | Password, must be 8+ characters      |

#### Request Headers

| Header         | Required | Description                |
|----------------|----------|----------------------------|
| `Content-Type` | Yes      | Must be `application/json` |

### Response Format

#### Success Response — 201 Created

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2023-06-15T14:32:10Z",
    "role": "user"
  }
}
```

What each field means:
- `message` — just tells you it worked
- `user.id` — the unique ID number for this user
- `user.username` — the name they picked
- `user.email` — their email (stored in lowercase)
- `user.created_at` — when the account was made (ISO 8601 format)
- `user.role` — they start as a regular `"user"`

### Error Responses

I noticed there are a lot of ways this can fail, so I tried to document all of them:

#### 400 Bad Request — Missing Required Field

This happens when you forget to send one of the three required fields.

```json
{
  "error": "Missing required field",
  "message": "email is required"
}
```

#### 400 Bad Request — Invalid Email Format

The email has to look like a real email. The code checks with a regex pattern.

```json
{
  "error": "Invalid email",
  "message": "Please provide a valid email address"
}
```

#### 400 Bad Request — Weak Password

Password has to be at least 8 characters or the API says no.

```json
{
  "error": "Weak password",
  "message": "Password must be at least 8 characters long"
}
```

#### 409 Conflict — Username Taken

Someone already has that username, so you need to pick a different one.

```json
{
  "error": "Username taken",
  "message": "Username is already in use"
}
```

#### 409 Conflict — Email Exists

That email is already in the database.

```json
{
  "error": "Email exists",
  "message": "An account with this email already exists"
}
```

#### 500 Internal Server Error

Something broke on the server side, like a database problem.

```json
{
  "error": "Server error",
  "message": "Failed to register user"
}
```

### Example Requests with Responses

#### Example 1: Successful Registration

**Request:**

```http
POST /api/users/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePass123"
}
```

**Response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2023-06-15T14:32:10Z",
    "role": "user"
  }
}
```

#### Example 2: Duplicate Username Error

**Request:**

```http
POST /api/users/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "newemail@example.com",
  "password": "securePass123"
}
```

**Response:**

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "Username taken",
  "message": "Username is already in use"
}
```

### Special Considerations

| Consideration       | What I Noticed                                                                 |
|---------------------|--------------------------------------------------------------------------------|
| **Password Storage**| Passwords get hashed before saving. You never store the real password.         |
| **Email Lowercasing**| The code does `.lower()` on emails so you do not get duplicates like `John@Example.com` and `john@example.com`. |
| **Confirmation Email**| It tries to send an email but if that fails, the user still gets created. The error just gets logged. |
| **Database Transaction**| There is a `try/except` block and if something fails, it does `db.session.rollback()` so you do not get half-made users. |
| **Default Role**    | Everyone starts as role `"user"`. There is no admin option in this endpoint.    |
| **Rate Limiting**   | The code does NOT have rate limiting. In a real app, you would want to add that so people cannot spam registrations. |

---

# Part 3: Prompt 2 — My Markdown API Reference

I converted everything above into a cleaner Markdown format. I like Markdown because I use it for GitHub README files and it is easy to read.

```markdown
# User Registration API Reference

## Overview

The User Registration endpoint creates new user accounts with validation, duplicate checking, password hashing, and confirmation email delivery.

---

## Endpoint

`POST /api/users/register`

---

## Authentication

No authentication required. Public endpoint.

---

## Request

### Headers

| Header       | Value              | Required |
|--------------|--------------------|----------|
| Content-Type | `application/json` | Yes      |

### Body Schema

```json
{
  "username": "string (required, unique)",
  "email": "string (required, valid email format)",
  "password": "string (required, min 8 characters)"
}
```

### Field Details

| Field      | Type   | Required | Constraints                          |
|------------|--------|----------|--------------------------------------|
| `username` | String | Yes      | Must be unique across all users      |
| `email`    | String | Yes      | Must match basic regex; must be unique |
| `password` | String | Yes      | Minimum 8 characters               |

---

## Responses

### 201 Created — Success

```json
{
  "message": "User registered successfully",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "created_at": "string (ISO 8601)",
    "role": "string"
  }
}
```

### 400 Bad Request — Missing Field

```json
{
  "error": "Missing required field",
  "message": "{field} is required"
}
```

### 400 Bad Request — Invalid Email

```json
{
  "error": "Invalid email",
  "message": "Please provide a valid email address"
}
```

### 400 Bad Request — Weak Password

```json
{
  "error": "Weak password",
  "message": "Password must be at least 8 characters long"
}
```

### 409 Conflict — Duplicate Username

```json
{
  "error": "Username taken",
  "message": "Username is already in use"
}
```

### 409 Conflict — Duplicate Email

```json
{
  "error": "Email exists",
  "message": "An account with this email already exists"
}
```

### 500 Internal Server Error

```json
{
  "error": "Server error",
  "message": "Failed to register user"
}
```

---

## Example Usage

### cURL Request

```bash
curl -X POST https://api.example.com/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securePass123"
  }'
```

### Response

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2023-06-15T14:32:10Z",
    "role": "user"
  }
}
```

---

## Error Handling Summary

| Error Code | Cause                    | What To Do                          |
|------------|--------------------------|--------------------------------------|
| 400        | Missing/invalid field    | Fix the request body and try again   |
| 409        | Duplicate username/email | Ask the user to pick something else  |
| 500        | Server/database error    | Wait and retry, or contact support   |

---

## Notes

- Passwords are hashed with `generate_password_hash()` before storage
- Emails are saved in lowercase to prevent duplicates
- Confirmation emails are sent in the background; if they fail, the user still gets created
- The database transaction rolls back if anything goes wrong during creation
- You should add rate limiting if you use this in production
```

---

# Part 4: Prompt 3 — My Developer Usage Guide

I wrote this for developers who know basic HTTP and JSON but might be new to this specific API. I tried to keep it friendly and practical.

## Developer Guide: Using the User Registration API

**Target Audience:** Developers who know how APIs work but are new to this one  
**Tone:** Friendly and practical

---

## 1. How to Authenticate

You do not need an API key or login token. Just send your request with the `Content-Type: application/json` header and you are good to go.

---

## 2. How to Format Your Request

### Required Headers

Always include:

```
Content-Type: application/json
```

### Request Body

Send a JSON object with these three fields:

| Field      | Rules                                   |
|------------|-----------------------------------------|
| `username` | Unique name (e.g., `"johndoe"`)         |
| `email`    | Valid email (e.g., `"john@example.com"`) |
| `password` | At least 8 characters                   |

### Example Request Body

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePass123"
}
```

---

## 3. How to Handle the Response

### If Everything Works (201 Created)

You get back a success message and the new user's profile:

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2023-06-15T14:32:10Z",
    "role": "user"
  }
}
```

**What to do:** Save the `user.id` if you need it. Let the user know their account is ready. A confirmation email will be sent automatically.

---

## 4. How to Deal with Common Errors

### 400 Bad Request — Missing or Invalid Data

You forgot a field, the email looks wrong, or the password is too short.

**Fix:** Read the `message` field to see exactly what is wrong, then fix your request.

```json
{
  "error": "Weak password",
  "message": "Password must be at least 8 characters long"
}
```

### 409 Conflict — Username or Email Already Taken

Someone else already has that username or email.

**Fix:** Ask the user to pick a different username or use a different email.

```json
{
  "error": "Username taken",
  "message": "Username is already in use"
}
```

### 500 Internal Server Error

Something broke on the server side.

**Fix:** Wait a moment and try again. If it keeps happening, check server logs or contact the API maintainer.

---

## 5. Example Code

### Python (using `requests`)

```python
import requests

url = "https://api.example.com/api/users/register"

payload = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securePass123"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:
    data = response.json()
    print(f"Success! User ID: {data['user']['id']}")
elif response.status_code == 400:
    print(f"Bad request: {response.json()['message']}")
elif response.status_code == 409:
    print(f"Conflict: {response.json()['message']}")
else:
    print(f"Error: {response.status_code}")
```

### JavaScript (using `fetch`)

```javascript
async function registerUser(username, email, password) {
  const response = await fetch('https://api.example.com/api/users/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, email, password })
  });

  const data = await response.json();

  if (response.status === 201) {
    console.log('User created:', data.user);
    return data.user;
  } else {
    console.error('Registration failed:', data.message);
    throw new Error(data.message);
  }
}

// Usage
registerUser('johndoe', 'john@example.com', 'securePass123')
  .then(user => console.log('Welcome!', user))
  .catch(err => console.error('Oops:', err));
```

### cURL

```bash
curl -X POST https://api.example.com/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","email":"john@example.com","password":"securePass123"}'
```

---

## Quick Checklist Before Calling the API

- [ ] All three fields (`username`, `email`, `password`) are included
- [ ] Email looks like a real email address
- [ ] Password is at least 8 characters long
- [ ] `Content-Type: application/json` header is set
- [ ] Body is sent as raw JSON (not form data)

---

## Pro Tips

- **Emails are case-insensitive:** The API stores emails in lowercase, so `John@Example.com` becomes `john@example.com`.
- **Confirmation emails are best-effort:** If the email server is down, the user still gets created — just without the confirmation email. Check server logs if you suspect email issues.
- **Passwords are hashed:** You can never retrieve the original password through the API. If a user forgets it, you will need a separate password reset flow.
- **Consider rate limiting:** In production, add rate limiting (e.g., 5 requests per IP per hour) to prevent spam or brute-force registration attempts.

---

## Summary

| What You Need   | Value                              |
|-----------------|------------------------------------|
| Endpoint        | `POST /api/users/register`         |
| Auth            | None                               |
| Content-Type    | `application/json`                   |
| Required Fields | `username`, `email`, `password`    |
| Success Code    | `201`                              |
| Common Errors   | `400` (bad input), `409` (duplicate), `500` (server error) |

---

# My Reflection & What I Learned

## Which parts of the API were most challenging to document?

For me, the **error handling** was the hardest part to document properly. There are so many different ways the request can fail:
- Missing fields (400)
- Bad email format (400)
- Weak password (400)
- Duplicate username (409)
- Duplicate email (409)
- Server crash (500)

I had to read the code carefully to make sure I caught every possible error path. At first I missed the `CastError` check that was in the Express example, but then I realized the Flask code does not have that — it just has a general 500 catch. So I had to pay attention to what THIS specific code does, not just copy from the example.

The **database transaction behavior** was also tricky. The `try/except` block with `db.session.rollback()` is invisible to the API user but important for developers to understand. I was not sure if I should document internal details like that, but I decided to include it in the "Special Considerations" section because it affects how the API behaves.

## How did you adjust your prompts to get better results?

I learned that being specific really helps. Here is what I tried:

- **Be specific about formats:** When I asked for "Markdown" instead of just "documentation," the output was much more structured and useful.
- **Ask for examples:** Including "at least 2 example requests with responses" forced me (and the AI) to think about real-world usage instead of just theory.
- **Define the audience:** Saying "for developers with basic API experience" helped keep the tone right — not too simple, not too complex.
- **List requirements explicitly:** Numbered lists (1, 2, 3...) made sure I did not forget anything the exercise asked for.

I also learned that iterating helps. My first draft of Prompt 1 was missing the rate limiting note, so I went back and added it after re-reading the code more carefully.

## Which documentation format did you find most effective?

I think **Markdown** was the most effective for me because:
- It is **readable** in any text editor or browser
- It is **portable** — works on GitHub, Notion, Confluence, etc.
- It is **easy to convert** to OpenAPI/Swagger later if needed
- You can **scan tables quickly** to find parameters and error codes

I also liked that Markdown is what I already use for README files, so it feels natural. OpenAPI is more formal and machine-readable, but for a human reading the docs, Markdown just feels friendlier.

## How would you incorporate this into your development workflow?

Here is what I would do in a real project:

1. **Write the code first** — Build and test the endpoint to make sure it actually works
2. **Generate docs immediately** — Use AI prompts right after coding while the logic is still fresh in my head
3. **Review and refine** — Check that the examples actually work with the real API (I would test the cURL command myself)
4. **Store in version control** — Keep the docs in the same repo as the code, maybe in a `/docs` folder
5. **Update together** — When the code changes, update the docs in the same pull request so they never get out of sync

I think the biggest lesson is that documentation should not be an afterthought. If you write it right after coding, it is way easier than trying to remember what you did two weeks later.
