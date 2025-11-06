"""
Mock database for demo purposes - stores data in memory
"""
from datetime import datetime
from uuid import uuid4

# In-memory storage
mock_data = {
    "users": [],
    "resources": [],
    "assignments": [],
    "student_assignments": [],
    "attendance": [],
    "marks": [],
    "notifications": [],
}

class MockResponse:
    def __init__(self, data):
        self.data = data

class MockTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.query_filters = []
        self.query_data = None
    
    def select(self, columns="*"):
        self.query_data = mock_data[self.table_name].copy()
        return self
    
    def insert(self, data):
        if isinstance(data, list):
            new_records = []
            for item in data:
                item["id"] = str(uuid4())
                if "created_at" not in item:
                    item["created_at"] = datetime.now().isoformat()
                new_records.append(item)
                mock_data[self.table_name].append(item)
            return MockResponse(new_records)
        else:
            data["id"] = str(uuid4())
            if "created_at" not in data:
                data["created_at"] = datetime.now().isoformat()
            mock_data[self.table_name].append(data)
            return MockResponse([data])
    
    def update(self, data):
        updated = []
        for record in mock_data[self.table_name]:
            matches = all(record.get(k) == v for k, v in self.query_filters)
            if matches:
                record.update(data)
                updated.append(record)
        return MockResponse(updated)
    
    def delete(self):
        deleted = []
        remaining = []
        for record in mock_data[self.table_name]:
            matches = all(record.get(k) == v for k, v in self.query_filters)
            if matches:
                deleted.append(record)
            else:
                remaining.append(record)
        mock_data[self.table_name] = remaining
        return MockResponse(deleted)
    
    def eq(self, column, value):
        self.query_filters.append((column, value))
        if self.query_data is not None:
            self.query_data = [r for r in self.query_data if r.get(column) == value]
        return self
    
    def in_(self, column, values):
        if self.query_data is not None:
            self.query_data = [r for r in self.query_data if r.get(column) in values]
        return self
    
    def gte(self, column, value):
        if self.query_data is not None:
            self.query_data = [r for r in self.query_data if r.get(column, "") >= value]
        return self
    
    def lte(self, column, value):
        if self.query_data is not None:
            self.query_data = [r for r in self.query_data if r.get(column, "") <= value]
        return self
    
    def execute(self):
        if self.query_data is not None:
            result = self.query_data
            self.query_data = None
            self.query_filters = []
            return MockResponse(result)
        return MockResponse([])

class MockSupabase:
    def table(self, table_name):
        return MockTable(table_name)

# Create mock instances
supabase = MockSupabase()
supabase_admin = MockSupabase()

# Use plaintext passwords for demo mode
DEMO_PASSWORD = "admin123"

# Add demo admin user
demo_admin = {
    "id": str(uuid4()),
    "email": "admin@demo.com",
    "password": DEMO_PASSWORD,
    "role": "admin",
    "name": "Demo Admin",
    "department": "Administration",
    "created_at": datetime.now().isoformat()
}
mock_data["users"].append(demo_admin)

# Add demo student
demo_student = {
    "id": str(uuid4()),
    "email": "student@demo.com",
    "password": DEMO_PASSWORD,
    "role": "student",
    "name": "Demo Student",
    "department": "Computer Science",
    "created_at": datetime.now().isoformat()
}
mock_data["users"].append(demo_student)

# Add demo teacher
demo_teacher = {
    "id": str(uuid4()),
    "email": "teacher@demo.com",
    "password": DEMO_PASSWORD,
    "role": "teacher",
    "name": "Demo Teacher",
    "department": "Computer Science",
    "created_at": datetime.now().isoformat()
}
mock_data["users"].append(demo_teacher)

print("✅ Mock database initialized with demo users:")
print(f"  • Admin: admin@demo.com / admin123")
print(f"  • Teacher: teacher@demo.com / admin123")
print(f"  • Student: student@demo.com / admin123")
