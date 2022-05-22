from typing import List, Optional, Dict
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError


class CompetencyInsertionFailed(Exception):
    """Raised when competency couldn't be inserted into the DB"""

    pass


class CourseInsertionFailed(Exception):
    """Raised when course couldn't be inserted into the DB"""

    pass


class RetrievingCourseFailed(Exception):
    """Raised when course(s) couldn't be retrieved"""

    pass


class RetrievingCompetencyFailed(Exception):
    """Raised when competency(ies) couldn't be retrieved"""

    pass


class CompetencyAndCourseInsertionFailed(Exception):
    """Raised when relationship between competency and course could not be created"""

    pass


class GraphDatabaseConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://db:7687", auth=("neo4j", "password")
        )

    def close(self):
        self.driver.close()

    def create_competency(
        self, competencyName: str, competencyBody: str
    ) -> str:
        """
        Create competency

        Insert competeny with its name and body into the db

        Parameters:
            competencyName: Competency name as string
            competencyBody: Competency body as string

        Raises: CompetencyInsertionFailed if insertion into DB failed

        Returns:
        Competency name and node as string

        """
        if self.retrieve_competency_by_name(competencyName):
            raise CompetencyInsertionFailed(
                f"Competancy with name '{competencyName}' already exists"
            )

        with self.driver.session() as session:
            competency = session.write_transaction(
                self._create_competency_transaction,
                competencyName,
                competencyBody,
            )
            return competency

    @staticmethod
    def _create_competency_transaction(
        tx, competencyName: str, competencyBody: str
    ) -> str:
        query = "CREATE (c:Competency) SET c.name = $name SET c.body = $body RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(
                query,
                name=competencyName,
                body=competencyBody,
            )
        except ClientError as e:
            raise CompetencyInsertionFailed(f"{query} raised an error: \n {e}")

        result = result.single()["result"]
        competency = {"id": result[0], "name": result[1], "body": result[2]}
        return competency

    def create_course(self, courseName: str, courseBody: str) -> str:
        """
        Create course

        Insert competeny with its name and body into the db

        Parameters:
            courseName: course name as string
            courseBody: course body as string

        Raises: CourseInsertionFailed if insertion into DB failed

        Returns:
        course name and node as string

        """
        if self.retrieve_course_by_name(courseName):
            raise CourseInsertionFailed(
                f"Course with name '{courseName}' already exists"
            )

        with self.driver.session() as session:
            course = session.write_transaction(
                self._create_course_transaction, courseName, courseBody
            )
            return course

    @staticmethod
    def _create_course_transaction(
        tx, courseName: str, courseBody: str
    ) -> str:
        query = "CREATE (c:Course) SET c.name = $name SET c.body = $body RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(
                query,
                name=courseName,
                body=courseBody,
            )
        except ClientError as e:
            raise CourseInsertionFailed(f"{query} raised an error: \n {e}")

        result = result.single()["result"]
        course = {"id": result[0], "name": result[1], "body": result[2]}
        return course

    def retrieve_all_courses(self) -> List[Optional[Dict]]:
        """
        Retrieve all courses

        Queries all nodes from the DB with the label course

        Raises: RetrievingCourseFailed if retrieving courses failed

        Returns:
        List of courses as dict

        """
        with self.driver.session() as session:
            course = session.write_transaction(self._retrieve_all_courses)
            return course

    @staticmethod
    def _retrieve_all_courses(tx) -> List[Optional[Dict]]:
        query = "MATCH (c:Course) RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(
                query,
            )
        except ClientError as e:
            raise RetrievingCourseFailed(f"{query} raised an error: \n {e}")

        if not result.data():
            return None

        courses = [
            {
                "id": c["result"][0],
                "name": c["result"][1],
                "body": c["result"][2],
            }
            for c in result.data()
        ]
        return courses

    def retrieve_all_competencies(self) -> List[Optional[Dict]]:
        """
        Retrieve all competencies

        Queries all nodes from the DB with the label competency

        Raises: RetrievingCompetencyFailed if retrieving competencies failed

        Returns:
        List of competencies as dict

        """
        with self.driver.session() as session:
            competencies = session.write_transaction(
                self._retrieve_all_competencies
            )
            return competencies

    @staticmethod
    def _retrieve_all_competencies(tx) -> List[Optional[Dict]]:
        query = "MATCH (c:Competency) RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(
                query,
            )
        except ClientError as e:
            raise RetrievingCompetencyFailed(
                f"{query} raised an error: \n {e}"
            )

        if not result:
            return None

        competencies = [
            {
                "id": c["result"][0],
                "name": c["result"][1],
                "body": c["result"][2],
            }
            for c in result.data()
        ]
        return competencies

    @staticmethod
    def _retrieve_competency_by_name(tx, competencyName) -> Optional[Dict]:
        query = "MATCH (c:Competency) WHERE c.name=$name RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(query, name=competencyName)
        except ClientError as e:
            raise RetrievingCompetencyFailed(
                f"{query} raised an error: \n {e}"
            )
        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        competency = {"id": result[0], "name": result[1], "body": result[2]}

        return competency

    def retrieve_competency_by_name(self, competencyName) -> Optional[Dict]:
        """
        Retrieve competency by name

        Query nodes with label Competency that have name competencyName

        Parameters:
            competencyName: competency name as string

        Raises:
            RetrievingCompetencyFailed if retrieving competency failed

        Returns:
            Competency as dict or None
        """
        with self.driver.session() as session:
            competency = session.write_transaction(
                self._retrieve_competency_by_name, competencyName
            )
            return competency

    @staticmethod
    def _retrieve_course_by_name(tx, courseName) -> Optional[Dict]:
        query = "MATCH (c:Course) WHERE c.name=$name RETURN [id(c), c.name, c.body] AS result"
        try:
            result = tx.run(query, name=courseName)
        except ClientError as e:
            raise RetrievingCourseFailed(f"{query} raised an error: \n {e}")
        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course = {"id": result[0], "name": result[1], "body": result[2]}

        return course

    def retrieve_course_by_name(self, courseName) -> Optional[Dict]:
        """
        Retrieve course by name

        Query nodes with label Course that have name courseName

        Parameters:
            courseName: course name as string

        Raises:
            RetrievingCourseFailed if retrieving course failed

        Returns:
            Course as dict or None
        """
        with self.driver.session() as session:
            competency = session.write_transaction(
                self._retrieve_course_by_name, courseName
            )
            return competency

    @staticmethod
    def _insert_course_with_nonexisting_competency(
        tx, competencyName, competencyBody, courseName, courseBody
    ) -> Dict:
        query = "CREATE (cou:Course {name:$courseName, body:$courseBody})-[r:HAS]->(com:Competency {name:$competencyName, body:$competencyBody}) RETURN [id(cou), cou.name, cou.body, id(com), com.name, com.body] AS result"
        try:
            result = tx.run(
                query,
                competencyName=competencyName,
                competencyBody=competencyBody,
                courseName=courseName,
                courseBody=courseBody,
            )
        except ClientError as e:
            raise CompetencyAndCourseInsertionFailed(
                f"{query} raised an error: \n {e}"
            )

        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course_and_competency = {
            "course_id": result[0],
            "course_name": result[1],
            "course_body": result[2],
            "competency_id": result[3],
            "competency_name": result[4],
            "competency_body": result[5],
        }
        return course_and_competency

    def insert_course_with_nonexisting_competency(
        self, competencyName, competencyBody, courseName, courseBody
    ) -> Dict:
        """
        Insert course with nonexisting competency

        Create a new course and HAS relationship to a new competency

        Parameters:
            competencyName: competency name as string
            competencyBody: competency body as string
            courseName: course name as string
            courseBody: course body as string

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        with self.driver.session() as session:
            competency_and_course = session.write_transaction(
                self._insert_course_with_nonexisting_competency,
                competencyName,
                competencyBody,
                courseName,
                courseBody,
            )
            return competency_and_course

    @staticmethod
    def _insert_course_with_existing_competency(
        tx, competencyId, courseName, courseBody
    ) -> Dict:
        query = "MATCH (com:Competency) WHERE id(com)=$competencyId CREATE (cou:Course {name:$courseName, body:$courseBody})-[r:HAS]->(com) RETURN [id(cou), cou.name, cou.body, id(com), com.name, com.body] AS result"
        try:
            result = tx.run(
                query,
                competencyId=competencyId,
                courseName=courseName,
                courseBody=courseBody,
            )
        except ClientError as e:
            raise CompetencyAndCourseInsertionFailed(
                f"{query} raised an error: \n {e}"
            )
        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course_and_competency = {
            "course_id": result[0],
            "course_name": result[1],
            "course_body": result[2],
            "competency_id": result[3],
            "competency_name": result[4],
            "competency_body": result[5],
        }
        return course_and_competency

    def insert_course_with_existing_competency(
        self, competencyId, courseName, courseBody
    ) -> Dict:
        """Insert course with existing competency

        Create a new course and HAS relationship to an existing competency

        Parameters:
            competencyId: id of the existing competency
            courseName: course name as string
            courseBody: course body as string

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        with self.driver.session() as session:
            competency_and_course = session.write_transaction(
                self._insert_course_with_existing_competency,
                competencyId,
                courseName,
                courseBody,
            )
            return competency_and_course

    @staticmethod
    def _insert_competency_with_existing_course(
        tx, competencyName, competencyBody, courseId
    ) -> Dict:
        query = "MATCH (cou:Course) WHERE id(cou)=$courseId CREATE (cou)-[r:HAS]->(com:Competency {name:$competencyName, body:$competencyBody}) RETURN [id(cou), cou.name, cou.body, id(com), com.name, com.body] AS result"
        try:
            result = tx.run(
                query,
                courseId=courseId,
                competencyName=competencyName,
                competencyBody=competencyBody,
            )
        except ClientError as e:
            raise CompetencyAndCourseInsertionFailed(
                f"{query} raised an error: \n {e}"
            )
        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course_and_competency = {
            "course_id": result[0],
            "course_name": result[1],
            "course_body": result[2],
            "competency_id": result[3],
            "competency_name": result[4],
            "competency_body": result[5],
        }
        return course_and_competency

    def insert_competency_with_existing_course(
        self, competencyName, competencyBody, courseId
    ) -> Dict:
        """Insert competency with existing course

        Create a new competency and HAS relationship from an existing course

        Parameters:
            competencyName: competency name as string
            competencyBody: competency body as string
            courseId: id of the existing course

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        with self.driver.session() as session:
            competency_and_course = session.write_transaction(
                self._insert_competency_with_existing_course,
                competencyName,
                competencyBody,
                courseId,
            )
            return competency_and_course

    @staticmethod
    def _retrieve_existing_relationship(tx, competencyId, courseId) -> Dict:
        query = "MATCH (cou:Course), (com: Competency) WHERE id(cou)=$courseId AND id(com)=$competencyId AND (cou)-[:HAS]->(com) RETURN [id(cou), cou.name, cou.body, id(com), com.name, com.body] AS result"
        try:
            result = tx.run(
                query,
                competencyId=competencyId,
                courseId=courseId,
            )
        except ClientError as e:
            raise CompetencyAndCourseInsertionFailed(
                f"{query} raised an error: \n {e}"
            )

        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course_and_competency = {
            "course_id": result[0],
            "course_name": result[1],
            "course_body": result[2],
            "competency_id": result[3],
            "competency_name": result[4],
            "competency_body": result[5],
        }
        return course_and_competency

    def retrieve_existing_relationship(
        self, courseId, competencyId
    ) -> List[Optional[Dict]]:
        """Retrieve existing relationship

        Retrieve HAS relationship between given competency and course

        Parameters:
            competencyId: Id of the existing competency
            courseId: id of the existing course

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        with self.driver.session() as session:
            relationship = session.write_transaction(
                self._retrieve_existing_relationship,
                competencyId,
                courseId,
            )
            return relationship

    @staticmethod
    def _insert_relationship_for_existing(tx, competencyId, courseId) -> Dict:
        query = "MATCH (cou:Course) WHERE id(cou)=$courseId MATCH (com:Competency) WHERE id(com)=$competencyId CREATE (cou)-[r:HAS]->(com) RETURN [id(cou), cou.name, cou.body, id(com), com.name, com.body] AS result"
        try:
            result = tx.run(
                query,
                competencyId=competencyId,
                courseId=courseId,
            )
        except ClientError as e:
            raise CompetencyAndCourseInsertionFailed(
                f"{query} raised an error: \n {e}"
            )

        if not result:
            return None
        result = result.single()
        if not result:
            return None
        result = result["result"]
        course_and_competency = {
            "course_id": result[0],
            "course_name": result[1],
            "course_body": result[2],
            "competency_id": result[3],
            "competency_name": result[4],
            "competency_body": result[5],
        }
        return course_and_competency

    def insert_relationship_for_existing(self, competencyId, courseId) -> Dict:
        """Insert relationship for existing

        Create a new HAS relationship between existing course and competency

        Parameters:
            competencyId: Id of existing competency
            courseId: id of the existing course

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        if self.retrieve_existing_relationship(courseId, competencyId):
            raise CompetencyAndCourseInsertionFailed(
                f"Competency {competencyId} and course {courseId} already have a relationship."
            )
        with self.driver.session() as session:
            competency_and_course = session.write_transaction(
                self._insert_relationship_for_existing,
                competencyId,
                courseId,
            )
            return competency_and_course

    def create_competecy_course_connection(
        self, courseName, courseBody, competencyName, competecyBody
    ) -> Dict:
        """Create competency course connection

        Create a new HAS relationship between course and competency avoiding duplicates

        Parameters:
            competencyName: competency name as string
            competencyBody: competency body as string
            courseName: course name as string
            courseBody: course body as string

        Raises:
            CompetencyAndCourseInsertionFailed if creating failed

        Returns:
            Course and competency as dict
        """
        existing_competency = self.retrieve_competency_by_name(competencyName)
        existing_course = self.retrieve_course_by_name(courseName)

        if existing_course and existing_competency:
            return self.insert_relationship_for_existing(
                existing_competency.get("id"), existing_course.get("id")
            )

        if existing_course and not existing_competency:
            return self.insert_competency_with_existing_course(
                competencyName, competecyBody, existing_course.get("id")
            )
        if not existing_course and existing_competency:
            return self.insert_course_with_existing_competency(
                existing_competency["id"], courseName, courseBody
            )

        # competency and course both don't exist yet
        return self.insert_course_with_nonexisting_competency(
            competencyName, competecyBody, courseName, courseBody
        )
