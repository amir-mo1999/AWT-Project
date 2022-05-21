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
    }
  ],
  "paths": {
    "/competency/{competencyName}": {
      "post": {
        "tags": [
          "competency"
        ],
        "summary": "Add a new competency",
        "description": "Add a new competency",
        "operationId": "addCompetency",
        "parameters": [
          {
            "in": "path",
            "name": "competencyName",
            "description": "Name of competency to be added",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Competency was added successfully.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          }
        },
        "requestBody": {
          "description": "Add a new competency",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "string"
              }
            }
          }
        }
      }
    },
    "/course/{courseName}": {
      "post": {
        "tags": [
          "course"
        ],
        "summary": "Add a new course",
        "description": "Add a new course",
        "operationId": "addCourse",
        "parameters": [
          {
            "in": "path",
            "name": "courseName",
            "description": "Name of course to be added",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Course was added successfully.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
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
                "type": "string"
              }
            }
          }
        }
      }
    },
    "/courses": {
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
    "/competencies": {
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
    }
  },
  "components": {
    "schemas": {
      "Course": {
        "properties": {
          "name": {
            "type": "string"
          },
          "body": {
            "type": "string"
          }
        }
      },
      "Competency": {
        "properties": {
          "name": {
            "type": "string"
          },
          "body": {
            "type": "string"
          }
        }
      }
    }
  }
}