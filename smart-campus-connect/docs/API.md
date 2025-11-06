# API Documentation

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### POST /auth/signup
Register a new user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "student",
  "name": "John Doe",
  "department": "Computer Science"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "student",
    "name": "John Doe",
    "department": "Computer Science"
  }
}
```

### POST /auth/login
Authenticate user and get token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response**: Same as signup

## Admin Endpoints

### POST /admin/resources
Create a new resource (PDF or video).

**Auth**: Required (Admin only)

**Request Body**:
```json
{
  "title": "Python Tutorial",
  "resource_type": "video",
  "link": "https://youtube.com/watch?v=xxx"
}
```

### GET /admin/resources
Get all resources.

**Auth**: Required (Admin only)

### PUT /admin/resources/{resource_id}
Update a resource.

**Auth**: Required (Admin only)

### DELETE /admin/resources/{resource_id}
Delete a resource.

**Auth**: Required (Admin only)

### POST /admin/grant-access
Grant access to a class teacher.

**Auth**: Required (Admin only)

**Request Body**:
```json
{
  "class_teacher_id": "uuid",
  "class_name": "CS 101"
}
```

## Teacher Endpoints

### POST /teacher/assignments
Create a new assignment.

**Auth**: Required (Teacher only)

**Request Body**:
```json
{
  "title": "Python Basics Assignment",
  "description": "Complete exercises 1-10",
  "due_date": "2024-12-31",
  "meet_link": "https://meet.google.com/xxx"
}
```

### GET /teacher/assignments
Get all assignments created by the teacher.

**Auth**: Required (Teacher only)

### GET /teacher/assignments/{assignment_id}
Get a specific assignment.

**Auth**: Required (Teacher only)

### PUT /teacher/assignments/{assignment_id}
Update an assignment.

**Auth**: Required (Teacher only)

### DELETE /teacher/assignments/{assignment_id}
Delete an assignment.

**Auth**: Required (Teacher only)

### POST /teacher/attendance
Record student attendance.

**Auth**: Required (Teacher only)

**Request Body**:
```json
{
  "student_id": "uuid",
  "subject": "Python Programming",
  "present_days": 18,
  "total_days": 20
}
```

### POST /teacher/marks
Record student marks.

**Auth**: Required (Teacher only)

**Request Body**:
```json
{
  "student_id": "uuid",
  "subject": "Python Programming",
  "marks_obtained": 85,
  "total_marks": 100
}
```

## Class Teacher Endpoints

### POST /class-teacher/teachers
Assign a teacher to a subject.

**Auth**: Required (Class Teacher only)

**Request Body**:
```json
{
  "teacher_id": "uuid",
  "subject": "Mathematics"
}
```

### GET /class-teacher/marks
Get all student marks.

**Auth**: Required (Class Teacher only)

### GET /class-teacher/marks/{student_id}
Get marks for a specific student.

**Auth**: Required (Class Teacher only)

### GET /class-teacher/attendance
Get all student attendance.

**Auth**: Required (Class Teacher only)

### GET /class-teacher/attendance/{student_id}
Get attendance for a specific student.

**Auth**: Required (Class Teacher only)

## Student Endpoints

### GET /student/assignments
Get all assignments for the student.

**Auth**: Required (Student only)

### GET /student/assignments/upcoming
Get assignments due in the next 2 days.

**Auth**: Required (Student only)

### POST /student/assignments/{assignment_id}/submit
Submit an assignment.

**Auth**: Required (Student only)

### GET /student/resources
Get all available resources.

**Auth**: Required (Student only)

### GET /student/attendance
Get personal attendance records.

**Auth**: Required (Student only)

### GET /student/marks
Get personal marks.

**Auth**: Required (Student only)

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Error Response Format

```json
{
  "detail": "Error message here"
}
```
