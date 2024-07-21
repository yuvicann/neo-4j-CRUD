from neo4j import GraphDatabase, basic_auth

class Neo4jWrapper:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        self.driver.close()

    def create_student(self, student_id, name, age, grade):
        with self.driver.session() as session:
            result = session.run(
                "CREATE (s:Student {id: $id, name: $name, age: $age, grade: $grade}) RETURN s",
                id=student_id, name=name, age=age, grade=grade)
            return result.single()

    def get_student(self, student_id):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Student {id: $id}) RETURN s", id=student_id)
            return result.single()

    def update_student(self, student_id, name, age, grade):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (s:Student {id: $id}) "
                "SET s.name = $name, s.age = $age, s.grade = $grade "
                "RETURN s",
                id=student_id, name=name, age=age, grade=grade)
            return result.single()

    def delete_student(self, student_id):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Student {id: $id}) DELETE s RETURN s", id=student_id)
            return result.single()
        
    def get_all_students(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Student) RETURN s;")
            return [record["s"] for record in result]
