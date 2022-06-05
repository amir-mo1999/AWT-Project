var spec = {
  "openapi": "3.0.0",
  "info": {
    "description": "This is our AWT project server. You can query competencies and courses here.",
    "version": "1.0.0",
    "title": "Competency Extraction",
    "license": {
      "name": "Apache 2.0",
      "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    }
  },
  "tags": [
    {
      "name": "competency",
      "description": "Add and query competencies",
      "externalDocs": {
        "description": "EU ESCO",
        "url": "https://esco.ec.europa.eu/en/classification/skill?uri=http%3A%2F%2Fdata.europa.eu%2Fesco%2Fskill%2FA1.1.0"
      }
    },
    {
      "name": "course",
      "description": "Add and query courses"
    },
    {
      "name": "relation",
      "description": "Add relationships between courses and competencies"
    }
  ],
  "paths": {
    "/course": {
      "post": {
        "tags": [
          "course"
        ],
        "summary": "Add a new course",
        "description": "Add a new course",
        "operationId": "addCourse",
        "responses": {
          "200": {
            "description": "Course was added successfully.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Course"
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        },
        "requestBody": {
          "description": "Add a new course",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CourseBody"
              }
            }
          }
        }
      },
      "get": {
        "tags": [
          "course"
        ],
        "summary": "Query for courses",
        "description": "Query for courses",
        "operationId": "retrieveCourses",
        "responses": {
          "200": {
            "description": "Query result for courses.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Course"
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        }
      }
    },
    "/course/{competencyId}": {
      "get": {
        "tags": [
          "course"
        ],
        "summary": "Query for courses",
        "description": "Query for courses",
        "operationId": "retrieveCoursesByCompetency",
        "responses": {
          "200": {
            "description": "Query result for courses.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Course"
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        },
        "parameters": [
          {
            "in": "path",
            "name": "competencyId",
            "description": "Filter courses by competency",
            "required": true,
            "schema": {
              "$ref": "#/components/schemas/CompetencyId"
            }
          }
        ]
      }
    },
    "/competency": {
      "get": {
        "tags": [
          "competency"
        ],
        "summary": "Query for competencies",
        "description": "Query for competencies",
        "operationId": "retrieveCompetencies",
        "responses": {
          "200": {
            "description": "Query result for competencies.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Competency"
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        }
      }
    },
    "/competency/{courseId}": {
      "get": {
        "tags": [
          "competency"
        ],
        "summary": "Query for competencies",
        "description": "Query for competencies",
        "operationId": "retrieveCompetenciesByCourse",
        "responses": {
          "200": {
            "description": "Query result for competencies.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Competency"
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        },
        "parameters": [
          {
            "in": "path",
            "name": "courseId",
            "description": "Filter competencies by course",
            "required": true,
            "schema": {
              "$ref": "#/components/schemas/CourseId"
            }
          }
        ]
      }
    },
    "/initialize": {
      "post": {
        "tags": [
          "competency"
        ],
        "summary": "Initialize the database with EU-ESCO competencies",
        "description": "Initialize the database with EU-ESCO competencies",
        "operationId": "initialize",
        "responses": {
          "200": {
            "description": "Database and Store have been initialized successfully"
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Course": {
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          },
          "body": {
            "type": "string"
          }
        }
      },
      "CourseId": {
        "properties": {
          "course_id": {
            "type": "integer"
          }
        }
      },
      "CourseBody": {
        "properties": {
          "courseDescription": {
            "type": "string"
          }
        }
      },
      "Competency": {
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          },
          "body": {
            "type": "string"
          }
        }
      },
      "CompetencyId": {
        "properties": {
          "competency_id": {
            "type": "integer"
          }
        }
      }
    }
  }
}
